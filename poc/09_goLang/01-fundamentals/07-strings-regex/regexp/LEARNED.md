# Regexp Exercise - LEARNED

## 학습 내용

### 정규표현식 기본

```go
import "regexp"

// 패턴 컴파일
pattern := regexp.MustCompile(`(TPS|TQ|IGMU)-\d+`)

// 문자열에서 매칭 찾기
result := pattern.FindString(input)
```

### 핵심 개념

1. **MustCompile**: 컴파일 실패 시 panic (확실한 패턴에 사용)
2. **FindString**: 첫 번째 매칭 문자열 반환
3. **백틱(`)**: raw string literal, 이스케이프 불필요

### 사용 예시

- Jira 티켓 번호 추출: `(TPS|TQ|IGMU)-\d+`
- 커밋 메시지에서 이슈 키 파싱

## 참고

- [regexp 패키지](https://pkg.go.dev/regexp)
