# Database 학습 문서

데이터베이스 이론부터 PostgreSQL 실전, AI/벡터 검색까지 체계적으로 정리한 학습 자료입니다.

---

## 폴더 구조

```
Database/
├── README.md                    # 이 파일
├── 01_기본개념/                  # 데이터베이스 핵심 이론
├── 02_분산시스템/                # 분산 데이터베이스 아키텍처
├── 03_데이터처리/                # 배치/스트림 처리
├── 04_PostgreSQL/               # PostgreSQL 실전 가이드
└── 05_AI와_벡터검색/             # 벡터 DB, RAG, 임베딩
```

---

## 학습 경로

### 입문자
```
01_기본개념 → 04_PostgreSQL
```

### 분산 시스템 관심
```
01_기본개념 → 02_분산시스템 → 03_데이터처리
```

### AI/GenAI 통합
```
01_기본개념 → 04_PostgreSQL → 05_AI와_벡터검색
```

---

## 폴더별 내용

### 01_기본개념
데이터베이스의 핵심 이론과 원리

| 파일 | 내용 | 출처 |
|------|------|------|
| 01_데이터_모델과_쿼리언어.md | 관계형, 문서, 그래프 모델 | DDIA Ch.3 |
| 02_저장소와_검색.md | B-tree, LSM-tree, 인덱스 | DDIA Ch.4 |
| 03_인코딩과_진화.md | 직렬화, 스키마 진화 | DDIA Ch.5 |
| 04_트랜잭션.md | ACID, 격리 수준, 2PC | **통합** (DDIA Ch.8 + JUP Ch.2) |
| 05_인덱스_이론.md | B-tree, LSM-tree, Hash | **신규 작성** |
| 06_NoSQL_비교.md | MongoDB, Redis, Cassandra, Neo4j | **신규 작성** |
| 07_캐싱_전략.md | Cache-Aside, Write-Through, Redis | **신규 작성** |

### 02_분산시스템
분산 데이터베이스의 아키텍처와 문제 해결

| 파일 | 내용 | 출처 |
|------|------|------|
| 01_시스템_아키텍처_트레이드오프.md | 데이터 시스템 설계 원칙 | DDIA Ch.1 |
| 01_시스템_아키텍처_트레이드오프_부록.md | 비기능 요구사항 | DDIA Ch.2 |
| 02_복제.md | Leader/Follower, Multi-Leader | DDIA Ch.6 |
| 03_샤딩.md | 파티셔닝 전략, 리밸런싱 | DDIA Ch.7 |
| 04_분산시스템의_문제점.md | 네트워크, 클록, 장애 | DDIA Ch.9 |
| 05_일관성과_합의.md | Linearizability, Consensus | DDIA Ch.10 |
| 06_철학적_고찰.md | 데이터 윤리, 미래 | DDIA Ch.14 |

### 03_데이터처리
대용량 데이터 처리 패러다임

| 파일 | 내용 | 출처 |
|------|------|------|
| 01_배치_처리.md | MapReduce, Spark, 데이터플로우 | DDIA Ch.11 |
| 02_스트림_처리.md | Kafka, Flink, 이벤트 소싱 | DDIA Ch.12 |
| 03_스트리밍_시스템_철학.md | Lambda/Kappa 아키텍처 | DDIA Ch.13 |

### 04_PostgreSQL
PostgreSQL 실전 활용 가이드

| 파일 | 내용 | 출처 |
|------|------|------|
| 01_시작하기.md | 설치, 기본 설정 | JUP Ch.1 |
| 02_RDBMS_기본기능.md | 스키마, 제약조건, 트랜잭션 | JUP Ch.2 |
| 03_모던_SQL.md | CTE, 윈도우 함수, LATERAL | JUP Ch.3 |
| 04_인덱스.md | B-tree, GIN, GiST, BRIN | JUP Ch.4 |
| 05_JSON_처리.md | JSONB, 연산자, 인덱싱 | JUP Ch.5 |
| 06_전문검색.md | tsvector, tsquery, 랭킹 | JUP Ch.6 |
| 07_익스텐션.md | pgvector, PostGIS 등 | JUP Ch.7 |
| 08_시계열_데이터.md | TimescaleDB, 파티셔닝 | JUP Ch.9 |
| 09_지리공간_데이터.md | PostGIS, 공간 쿼리 | JUP Ch.10 |
| 10_메시지_큐.md | LISTEN/NOTIFY, pg_queue | JUP Ch.11 |
| A_최적화_팁.md | 쿼리 최적화, 설정 튜닝 | JUP Appendix A |
| B_PostgreSQL_적합성.md | PostgreSQL 선택 기준 | JUP Appendix B |
| C_성능_모니터링.md | pg_stat_*, EXPLAIN ANALYZE | **신규 작성** |

### 05_AI와_벡터검색
벡터 데이터베이스와 AI 통합

| 파일 | 내용 | 출처 |
|------|------|------|
| 01_벡터_데이터베이스_소개.md | 벡터 DB 개요 | VDB Ch.1 |
| 02_임베딩.md | 텍스트/이미지 임베딩 | VDB Ch.2 |
| 03_FAISS_유사도검색.md | FAISS 라이브러리 | VDB Ch.3 |
| 04_SQLite_시맨틱검색.md | SQLite-VSS | VDB Ch.4 |
| 05_pgvector_유사도검색.md | pgvector, RAG | **통합** (VDB Ch.5 + JUP Ch.8) |
| 06_RAG_시스템_SQLite.md | Ollama + SQLite RAG | VDB Ch.6 |
| 07_RAG_시스템_PostgreSQL.md | PostgreSQL RAG | VDB Ch.7 |
| 08_대화검색_RAG.md | 대화형 검색 시스템 | VDB Ch.8 |
| 09_VQL.md | Vector Query Language | VDB Ch.9 |
| 10_고급_임베딩_기법.md | 멀티모달, Fine-tuning | VDB Ch.10 |
| 11_GenAI_면접정리.md | GenAI/LLM 통합 | JUP Ch.8 |

---

## 출처 약어

| 약어 | 원본 |
|------|------|
| DDIA | Designing Data-Intensive Applications (DB패턴) |
| JUP | Just Use Postgres! |
| VDB | Vector Databases (벡터 데이터베이스) |

---

## 참고 자료

### 도서
- **Designing Data-Intensive Applications** - Martin Kleppmann
- **Just Use Postgres!** - Denis Magda
- **Database Internals** - Alex Petrov

### 공식 문서
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Redis Documentation](https://redis.io/docs/)

---

## 학습 체크리스트

### 기본
- [ ] ACID 속성과 트랜잭션 격리 수준
- [ ] B-tree vs LSM-tree 인덱스
- [ ] CAP 정리와 NoSQL 유형

### 분산 시스템
- [ ] 복제 전략 (Single-Leader, Multi-Leader)
- [ ] 샤딩과 리밸런싱
- [ ] 합의 알고리즘 (Paxos, Raft)

### PostgreSQL
- [ ] 인덱스 유형 (B-tree, GIN, GiST, BRIN)
- [ ] JSONB 처리와 인덱싱
- [ ] pg_stat_* 모니터링

### AI 통합
- [ ] 벡터 임베딩과 유사도 검색
- [ ] pgvector 인덱스 (IVFFlat, HNSW)
- [ ] RAG 파이프라인 구축

---

*마지막 업데이트: 2026-01-25*
