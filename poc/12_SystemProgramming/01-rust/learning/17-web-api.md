# 17. Web API (Axum)

Axum은 tokio 기반의 ergonomic한 웹 프레임워크로, tower 미들웨어 에코시스템을 활용합니다. Spring Boot의 DI 컨테이너와 달리 State로 의존성을 공유하고, serde_json으로 요청/응답을 처리하며, sqlx로 DB와 연동합니다. 타입 안전성과 컴파일 타임 검증이 강점입니다.

## 목표
- [ ] axum의 Router와 Handler 기본 구조 이해
- [ ] tower 미들웨어 체인 구성
- [ ] serde_json으로 요청/응답 처리
- [ ] State로 공유 상태(DB 풀 등) 관리
- [ ] sqlx로 PostgreSQL 연동
- [ ] 에러 처리 및 커스텀 응답
- [ ] Spring Boot와 아키텍처 비교

## 1. axum 기본 구조

## 2. Router/Handler

## 3. 미들웨어(tower)

## 4. 요청/응답(serde_json)

## 5. 상태 공유(State)

## 6. DB 연동(sqlx)

## 7. 에러 처리

## 명령어 요약
| 개념 | 설명 |
|------|------|
| `Router::new()` | 라우터 생성 |
| `.route("/path", get(handler))` | 라우트 등록 |
| `Json<T>` | JSON 요청/응답 추출/생성 |
| `State<T>` | 공유 상태 추출 |
| `tower::ServiceBuilder` | 미들웨어 체인 구성 |
| `sqlx::query!` | 컴파일 타임 SQL 검증 |
| `axum::serve` | 서버 실행 |

## 체크포인트
- axum vs actix-web을 선택하는 기준은?
- tower 미들웨어 패턴이란 무엇인가?
- Spring Boot의 DI vs Rust의 State 관리 차이는?
- sqlx의 컴파일 타임 검증은 어떻게 동작하는가?
- Json<T> 추출자가 실패하는 경우는?
- IntoResponse 트레이트의 역할은?
- 비동기 핸들러에서 블로킹 작업을 처리하는 방법은?
