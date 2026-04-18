package jenkins

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"strconv"
	"strings"
	"time"
)

// JenkinsClient wraps Jenkins REST API.
type JenkinsClient struct {
	baseURL    string
	username   string
	apiToken   string
	httpClient *http.Client

	// CSRF crumb cache
	crumbField string
	crumbValue string
}

func NewJenkinsClient(baseURL, username, token string) *JenkinsClient {
	jar, _ := cookiejar.New(nil)
	return &JenkinsClient{
		baseURL:  strings.TrimRight(baseURL, "/"),
		username: username,
		apiToken: token,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
			Jar:     jar,
		},
	}
}

// fetchCrumb retrieves the CSRF crumb from Jenkins.
func (c *JenkinsClient) fetchCrumb(ctx context.Context) error {
	reqURL := c.baseURL + "/crumbIssuer/api/json"
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, reqURL, nil)
	if err != nil {
		return err
	}
	req.SetBasicAuth(c.username, c.apiToken)

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		// crumb issuer not available — skip (e.g. CSRF disabled)
		return nil
	}

	var result struct {
		Crumb             string `json:"crumb"`
		CrumbRequestField string `json:"crumbRequestField"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return err
	}
	c.crumbField = result.CrumbRequestField
	c.crumbValue = result.Crumb
	return nil
}

func (c *JenkinsClient) doRequest(ctx context.Context, method, path string, body io.Reader) (*http.Response, error) {
	// Fetch crumb once for POST requests
	if method == http.MethodPost && c.crumbValue == "" {
		if err := c.fetchCrumb(ctx); err != nil {
			// log but continue — crumb may not be required
			fmt.Printf("jenkins: crumb fetch warning: %v\n", err)
		}
	}

	reqURL := c.baseURL + path
	req, err := http.NewRequestWithContext(ctx, method, reqURL, body)
	if err != nil {
		return nil, fmt.Errorf("create request: %w", err)
	}
	req.SetBasicAuth(c.username, c.apiToken)
	req.Header.Set("Content-Type", "application/json")

	// Add CSRF crumb header if available
	if c.crumbField != "" && c.crumbValue != "" {
		req.Header.Set(c.crumbField, c.crumbValue)
	}

	resp, err := c.httpClient.Do(req)
	if err != nil {
		return nil, fmt.Errorf("execute request: %w", err)
	}
	return resp, nil
}

// BuildInfo represents Jenkins build JSON response.
type BuildInfo struct {
	Number            int    `json:"number"`
	URL               string `json:"url"`
	Result            string `json:"result"`            // SUCCESS, FAILURE, ABORTED, null (running)
	Building          bool   `json:"building"`
	Duration          int64  `json:"duration"`          // ms
	EstimatedDuration int64  `json:"estimatedDuration"` // ms
	Timestamp         int64  `json:"timestamp"`         // epoch ms
}

// QueueItem represents Jenkins queue item JSON response.
type QueueItem struct {
	ID         int `json:"id"`
	Executable *struct {
		Number int    `json:"number"`
		URL    string `json:"url"`
	} `json:"executable"`
	Blocked bool   `json:"blocked"`
	Why     string `json:"why"`
}

// JobInfo represents Jenkins job JSON response (for listing builds).
type JobInfo struct {
	Name   string      `json:"name"`
	URL    string      `json:"url"`
	Builds []BuildInfo `json:"builds"`
}

// TriggerBuild triggers a Jenkins job and returns the queue item ID.
// If params is non-empty, buildWithParameters is used; otherwise build is used.
func (c *JenkinsClient) TriggerBuild(ctx context.Context, jobName string, params map[string]string) (int64, error) {
	var path string
	var body io.Reader

	if len(params) > 0 {
		form := url.Values{}
		for k, v := range params {
			form.Set(k, v)
		}
		path = fmt.Sprintf("/job/%s/buildWithParameters?%s", jobName, form.Encode())
	} else {
		path = fmt.Sprintf("/job/%s/build", jobName)
	}

	resp, err := c.doRequest(ctx, http.MethodPost, path, body)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return 0, fmt.Errorf("trigger build: unexpected status %d: %s", resp.StatusCode, string(bodyBytes))
	}

	location := resp.Header.Get("Location")
	if location == "" {
		return 0, fmt.Errorf("trigger build: missing Location header in response")
	}

	// Location format: http://jenkins/queue/item/{id}/
	location = strings.TrimRight(location, "/")
	parts := strings.Split(location, "/")
	if len(parts) == 0 {
		return 0, fmt.Errorf("trigger build: cannot parse queue item ID from Location: %s", location)
	}
	idStr := parts[len(parts)-1]
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		return 0, fmt.Errorf("trigger build: invalid queue item ID %q in Location %s: %w", idStr, location, err)
	}

	return id, nil
}

// GetBuild retrieves information about a specific build.
func (c *JenkinsClient) GetBuild(ctx context.Context, jobName string, number int) (*BuildInfo, error) {
	path := fmt.Sprintf("/job/%s/%d/api/json", jobName, number)

	resp, err := c.doRequest(ctx, http.MethodGet, path, nil)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("get build %s#%d: unexpected status %d: %s", jobName, number, resp.StatusCode, string(bodyBytes))
	}

	var info BuildInfo
	if err := json.NewDecoder(resp.Body).Decode(&info); err != nil {
		return nil, fmt.Errorf("get build %s#%d: decode response: %w", jobName, number, err)
	}

	return &info, nil
}

// GetBuildLog retrieves the console text log for a specific build.
func (c *JenkinsClient) GetBuildLog(ctx context.Context, jobName string, number int) (string, error) {
	path := fmt.Sprintf("/job/%s/%d/consoleText", jobName, number)

	resp, err := c.doRequest(ctx, http.MethodGet, path, nil)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return "", fmt.Errorf("get build log %s#%d: unexpected status %d: %s", jobName, number, resp.StatusCode, string(bodyBytes))
	}

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("get build log %s#%d: read response: %w", jobName, number, err)
	}

	return string(bodyBytes), nil
}

// ListBuilds retrieves the most recent builds for a job up to limit.
func (c *JenkinsClient) ListBuilds(ctx context.Context, jobName string, limit int) ([]BuildInfo, error) {
	path := fmt.Sprintf(
		"/job/%s/api/json?tree=builds[number,url,result,building,duration,timestamp]{0,%d}",
		jobName, limit,
	)

	resp, err := c.doRequest(ctx, http.MethodGet, path, nil)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("list builds %s: unexpected status %d: %s", jobName, resp.StatusCode, string(bodyBytes))
	}

	var jobInfo JobInfo
	if err := json.NewDecoder(resp.Body).Decode(&jobInfo); err != nil {
		return nil, fmt.Errorf("list builds %s: decode response: %w", jobName, err)
	}

	return jobInfo.Builds, nil
}

// GetQueueItem retrieves information about a Jenkins queue item by ID.
func (c *JenkinsClient) GetQueueItem(ctx context.Context, id int64) (*QueueItem, error) {
	path := fmt.Sprintf("/queue/item/%d/api/json", id)

	resp, err := c.doRequest(ctx, http.MethodGet, path, nil)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("get queue item %d: unexpected status %d: %s", id, resp.StatusCode, string(bodyBytes))
	}

	var item QueueItem
	if err := json.NewDecoder(resp.Body).Decode(&item); err != nil {
		return nil, fmt.Errorf("get queue item %d: decode response: %w", id, err)
	}

	return &item, nil
}
