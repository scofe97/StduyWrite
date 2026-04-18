package main

import (
	"encoding/json"
	"fmt"
)

// 과제 1: API 응답 파싱
// 외부 API(예: GitHub API)의 JSON 응답을 적절한 구조체로 언마샬하는 코드를 작성하세요.

// 샘플 JSON 데이터 (GitHub User API 응답 형식)
var sampleJSON = `{
	"login": "octocat",
	"id": 1,
	"avatar_url": "https://github.com/images/error/octocat_happy.gif",
	"html_url": "https://github.com/octocat",
	"name": "monalisa octocat",
	"company": "GitHub",
	"blog": "https://github.blog",
	"location": "San Francisco",
	"email": "octocat@github.com",
	"bio": "There once was...",
	"public_repos": 2,
	"public_gists": 1,
	"followers": 20,
	"following": 0,
	"created_at": "2008-01-14T04:33:35Z",
	"updated_at": "2008-01-14T04:33:35Z"
}`

// TODO: GitHub User 응답을 담을 구조체 정의
// - 적절한 json 태그 사용
// - 필요한 필드만 선택적으로 정의 (모든 필드를 다 정의할 필요 없음)
type GitHubUser struct {
	// TODO: 필드 정의
}

// TODO: 여러 사용자 목록을 담을 구조체 (배열 응답용)
type GitHubUsersResponse struct {
	// TODO: 필드 정의
}

func main() {
	// TODO 1: sampleJSON을 GitHubUser 구조체로 파싱
	// - json.Unmarshal 사용
	// - 에러 처리 포함

	// TODO 2: 파싱된 데이터 출력
	// - fmt.Printf("%+v\n", user) 또는 개별 필드 출력

	// TODO 3: (선택) 배열 형태의 JSON 파싱 연습
	// 샘플:
	// usersJSON := `[{"login": "user1", "id": 1}, {"login": "user2", "id": 2}]`

	fmt.Println("TODO: API 응답 파싱 구현")
}

// TODO 4: (선택) HTTP로 실제 GitHub API 호출
// func fetchGitHubUser(username string) (*GitHubUser, error) {
// 	// GET https://api.github.com/users/{username}
// 	// http.Get 사용
// 	// json.NewDecoder로 응답 파싱
// }
