package pipeline

import (
	"fmt"
	"path"
	"sync"
	"time"

	pbv1 "github.com/runners-high/git-provider/pkg/pb/v1"
)

type Store struct {
	mu        sync.RWMutex
	pipelines map[string]*pbv1.Pipeline // id -> Pipeline
	builds    map[string][]*pbv1.Build  // pipeline_id -> []Build
	nextID    int
}

func NewStore() *Store {
	return &Store{
		pipelines: make(map[string]*pbv1.Pipeline),
		builds:    make(map[string][]*pbv1.Build),
		nextID:    0,
	}
}

// CreatePipeline creates a new pipeline and stores it. Generates ID like "pipe-1".
func (s *Store) CreatePipeline(name, repository, branchPattern, jenkinsJobName string, stages []*pbv1.PipelineStage, ciConfig *pbv1.CIConfig) *pbv1.Pipeline {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.nextID++
	id := fmt.Sprintf("pipe-%d", s.nextID)
	now := time.Now().UTC().Format(time.RFC3339)

	p := &pbv1.Pipeline{
		Id:             id,
		Name:           name,
		Repository:     repository,
		BranchPattern:  branchPattern,
		Stages:         stages,
		CiConfig:       ciConfig,
		JenkinsJobName: jenkinsJobName,
		CreatedAt:      now,
		UpdatedAt:      now,
	}

	s.pipelines[id] = p
	return p
}

// GetPipeline returns the pipeline with the given id, or an error if not found.
func (s *Store) GetPipeline(id string) (*pbv1.Pipeline, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	p, ok := s.pipelines[id]
	if !ok {
		return nil, fmt.Errorf("pipeline %q not found", id)
	}
	return p, nil
}

// ListPipelines returns all pipelines, or only those matching the given repository if non-empty.
func (s *Store) ListPipelines(repository string) []*pbv1.Pipeline {
	s.mu.RLock()
	defer s.mu.RUnlock()

	result := make([]*pbv1.Pipeline, 0, len(s.pipelines))
	for _, p := range s.pipelines {
		if repository == "" || p.Repository == repository {
			result = append(result, p)
		}
	}
	return result
}

// DeletePipeline removes the pipeline with the given id. Returns an error if not found.
func (s *Store) DeletePipeline(id string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, ok := s.pipelines[id]; !ok {
		return fmt.Errorf("pipeline %q not found", id)
	}
	delete(s.pipelines, id)
	delete(s.builds, id)
	return nil
}

// AddBuild adds a new build for the given pipeline. Generates ID like "build-1",
// auto-increments build_number per pipeline, and sets status to QUEUED.
func (s *Store) AddBuild(pipelineID, trigger, branch, commitSHA string) (*pbv1.Build, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if _, ok := s.pipelines[pipelineID]; !ok {
		return nil, fmt.Errorf("pipeline %q not found", pipelineID)
	}

	s.nextID++
	id := fmt.Sprintf("build-%d", s.nextID)
	buildNumber := int32(len(s.builds[pipelineID]) + 1)
	now := time.Now().UTC().Format(time.RFC3339)

	b := &pbv1.Build{
		Id:          id,
		PipelineId:  pipelineID,
		BuildNumber: buildNumber,
		Status:      pbv1.BuildStatus_BUILD_STATUS_QUEUED,
		Trigger:     trigger,
		Branch:      branch,
		CommitSha:   commitSHA,
		StartedAt:   now,
	}

	s.builds[pipelineID] = append(s.builds[pipelineID], b)
	return b, nil
}

// GetBuild returns the build with the given pipeline id and build number.
func (s *Store) GetBuild(pipelineID string, buildNumber int32) (*pbv1.Build, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()

	for _, b := range s.builds[pipelineID] {
		if b.BuildNumber == buildNumber {
			return b, nil
		}
	}
	return nil, fmt.Errorf("build %d for pipeline %q not found", buildNumber, pipelineID)
}

// ListBuilds returns the latest N builds for the given pipeline. Defaults to 20 if limit <= 0.
func (s *Store) ListBuilds(pipelineID string, limit int32) []*pbv1.Build {
	s.mu.RLock()
	defer s.mu.RUnlock()

	if limit <= 0 {
		limit = 20
	}

	all := s.builds[pipelineID]
	if int32(len(all)) <= limit {
		result := make([]*pbv1.Build, len(all))
		copy(result, all)
		return result
	}

	// Return the latest N (tail of slice, since builds are appended in order)
	tail := all[int32(len(all))-limit:]
	result := make([]*pbv1.Build, len(tail))
	copy(result, tail)
	return result
}

// UpdateBuildStatus updates the status, url, and duration of a build.
func (s *Store) UpdateBuildStatus(pipelineID string, buildNumber int32, status pbv1.BuildStatus, url string, durationSeconds int32) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	for _, b := range s.builds[pipelineID] {
		if b.BuildNumber == buildNumber {
			b.Status = status
			b.Url = url
			b.DurationSeconds = durationSeconds
			b.FinishedAt = time.Now().UTC().Format(time.RFC3339)
			return nil
		}
	}
	return fmt.Errorf("build %d for pipeline %q not found", buildNumber, pipelineID)
}

// MatchPipelines returns all pipelines whose repository matches exactly and whose
// branch_pattern matches the given branch using path.Match semantics.
func (s *Store) MatchPipelines(repository, branch string) []*pbv1.Pipeline {
	s.mu.RLock()
	defer s.mu.RUnlock()

	var result []*pbv1.Pipeline
	for _, p := range s.pipelines {
		if p.Repository != repository {
			continue
		}
		matched, err := path.Match(p.BranchPattern, branch)
		if err != nil {
			// Invalid pattern — skip
			continue
		}
		if matched {
			result = append(result, p)
		}
	}
	return result
}
