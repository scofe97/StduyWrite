# 03-concurrency

Go 동시성 프로그래밍의 핵심 패턴을 학습합니다.

## 구조

```
03-concurrency/
├── learning/
│   ├── 01-basics.md
│   ├── 02-select.md
│   ├── 03-sync-primitives.md
│   └── 04-worker-pool.md
├── practice/
│   ├── 01-basics/
│   ├── 02-select/
│   ├── 03-sync-primitives/
│   └── 04-worker-pool/
└── README.md
```

## 학습 순서

| # | 토픽 | learning | practice |
|---|------|----------|----------|
| 1 | Goroutine & Channel 기초 | 01 | 01-basics (loose .go + 4개) |
| 2 | Select | 02 | 02-select (3개) |
| 3 | Sync Primitives | 03 | 03-sync-primitives (4개) |
| 4 | Worker Pool | 04 | 04-worker-pool (4개) |

## Worker Pool 주요 라이브러리

### golang.org/x/sync/errgroup
```bash
go get golang.org/x/sync/errgroup
```
고루틴 그룹 관리 및 에러 수집

### golang.org/x/sync/semaphore
```bash
go get golang.org/x/sync/semaphore
```
동시 실행 수 제한
