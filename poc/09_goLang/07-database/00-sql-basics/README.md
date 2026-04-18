# 17. 데이터베이스 연동

Go에서 SQL 데이터베이스를 다루는 방법을 학습합니다.

## 학습 목표

- database/sql 패키지 사용
- jmoiron/sqlx 활용
- 커넥션 풀 관리
- 트랜잭션 처리
- 쿼리 빌더 패턴

## 주요 라이브러리

### database/sql (표준 라이브러리)
Go 표준 SQL 인터페이스

### jmoiron/sqlx
```bash
go get github.com/jmoiron/sqlx
```

구조체 스캔, Named Query 지원

### 드라이버
```bash
# PostgreSQL
go get github.com/lib/pq

# MySQL
go get github.com/go-sql-driver/mysql

# SQLite
go get github.com/mattn/go-sqlite3
```

## 프로젝트 구조

```
17-database/
├── README.md
├── EXERCISES.md
├── HINTS.md
├── LEARNED.md
├── go.mod
├── main.go
├── db/
│   ├── connection.go     # DB 연결 관리
│   └── migrations/       # 마이그레이션 파일
├── models/
│   └── user.go           # 엔티티 정의
└── repository/
    └── user_repository.go # DB 액세스 레이어
```

## 참조 자료

### 📚 Learning Go, 2nd Edition 참조
- **13_The_Standard_Library.md**: database/sql 패키지 사용법
- **14_The_Context.md**: 쿼리 타임아웃, 트랜잭션 컨텍스트
- **09_Errors.md**: SQL 에러 처리 패턴
- **07_Types_Methods_and_Interfaces.md**: Repository 인터페이스 설계

## 다음 단계

다음 모듈 [18-worker-pool](../18-worker-pool/)에서 워커 풀 패턴을 학습합니다.
