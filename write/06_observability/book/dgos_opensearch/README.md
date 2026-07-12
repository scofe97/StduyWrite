---
title: The Definitive Guide to OpenSearch (정독 노트 MOC)
tags: [moc, observability, opensearch, search, book]
status: done
related:
  - ../../README.md
  - 01-01.OpenSearch 개요 — 진화·핵심 역량·활용 사례.md
  - 06-01.고급 쿼리 — 복합·지리·faceted·percolation.md
  - 07-01.분석과 시각화 — 집계·대시보드·관측성.md
  - 08-01.플러그인 — 유형·주요 플러그인·아키텍처.md
  - 09-01.검색 앱 만들기 — autocomplete·fuzzy·faceted·UI.md
  - 10-01.벡터·생성 AI — 시맨틱 검색과 RAG.md
  - 11-01.OpenSearch 마이그레이션 — 단계·무중단 패턴·Migration Assistant.md
  - 12-01.보안 — 인증·인가·FGAC·멀티테넌시.md
  - 13-01.모니터링·백업·복구 — 지표·admission control·DR.md
  - 14-01.스케일링·성능 최적화 — 분산 구조·사이징·튜닝.md
updated: 2026-07-10
---

# The Definitive Guide to OpenSearch
---
> O'Reilly 단행본(ISBN 9781835885789)입니다. 검색·분석 엔진 **OpenSearch**(Apache Lucene 기반, Elasticsearch 포크)를 설치·구성에서 시작해 인덱싱·쿼리·시각화·벡터/생성 AI·마이그레이션·보안·운영·확장까지 **14개 장(4개 파트)** 에 걸쳐 다룹니다. 초심자는 아키텍처 기초를, 경험자는 고급 쿼리·성능 튜닝을 얻어 갈 수 있게 짜여 있습니다.

## 이 책을 여기 두는 이유

상위 [`06_observability/README.md`](../../README.md) 는 "예정 주제 — 관측 저장소 심화(TBD)" 에서 **OpenSearch** 를 LGTM 스택과 대비해 배우겠다고 예고해 두었습니다. 이 폴더가 그 예고를 실현합니다.

핵심 대비는 **저장 전략의 트레이드오프**입니다. LGTM 의 Loki 는 *라벨 기반 최소 인덱싱*이라 저장 비용이 싸지만 본문 검색 표현력이 제한됩니다. OpenSearch 는 *전문(full-text) 역색인*이라 그 반대편에 섭니다 — 인덱싱·저장 비용은 크지만 임의 필드에 대한 복합·지리·faceted·의미(vector) 검색까지 표현력이 압도적입니다. 같은 로그·관측 문제를 정반대 지점에서 푸는 셈이라, Loki([상위 02-03](../../02_LGTMStack/02-03.Grafana%20Loki.md)) 를 이미 익힌 상태에서 이 대비를 짚는 것이 학습 포인트입니다.

## 파트 구조

원본은 4개 파트로 묶여 있습니다(각 Part 디바이더에서 확인).

| 파트 | 제목 | 장 |
|------|------|----|
| Part 1 | Getting Started with OpenSearch — Fundamentals and Deployment | 1–3 |
| Part 2 | Data Management and Discovery — Indexing, Querying, and Visualization | 4–7 |
| Part 3 | Extending OpenSearch — Plugins, AI Integration, and Application Development | 8–10 |
| Part 4 | Securing and Optimizing OpenSearch — Administration Best Practices | 11–14 |

## 장별 목표

각 장 앞머리의 "In this chapter... / We'll cover the following topics" 를 근거로 정리했습니다.

| 장 | 제목 | 이 장의 목표 | 주요 토픽 |
|----|------|------------|----------|
| 1 | Overview of OpenSearch | OpenSearch 의 기원·진화와 핵심 역량, 실사용 사례를 이해한다 | 진화 여정 · 핵심 역량 · 실사용 예 · e-commerce 검색 · 로그 분석/관측성 |
| 2 | Installing and Configuring OpenSearch | 핵심 용어부터 설치·클러스터 구성·보안까지 환경을 셋업한다 | 용어(node·cluster·index·shard·replica) · 클러스터 기초 · 인덱스 · 시스템 요건 · 설치 · Dashboards 셋업 |
| 3 | Deployment Options: Amazon OpenSearch Service & Serverless | 관리형 서비스로 배포한다 — 매니지드 클러스터 vs 서버리스 | OpenSearch Service 소개 · API·SDK 접근 · 인프라 · 운영 관리 · Serverless |
| 4 | Indexing Data | 데이터를 실제로 인덱싱한다 — 인덱스 생성·설정·매핑 심화 | 인덱싱 개요 · Dashboards Dev Tools 연결 · 인덱스 생성(API) · 인덱스 설정 · 매핑 |
| 5 | Searching: Core APIs | 검색 처리 원리와 핵심 쿼리 API 로 효과적 검색을 구축한다 | 쿼리 처리 · 데이터 로딩 · leaf 쿼리(match·term) · 하이라이팅 · completion/suggestion · 검색 템플릿 |
| 6 | Advanced Querying | leaf 쿼리를 넘어 복합·지리·faceted 검색으로 고급 검색을 만든다 | compound 쿼리·필터 · geospatial · faceted search · percolation · profile API |
| 7 | Analyze and Visualize OpenSearch Data | aggregation 분석과 Dashboards 시각화·관측성 도구를 다룬다 | Dashboards 소개 · aggregation 유형 · 시각화 · 로깅/관측성 · 로그 워크로드 베스트 프랙티스 |
| 8 | Introduction to OpenSearch Plugins | 플러그인으로 기능을 확장한다 — 내장·커스텀·설치·관리 | 내장 vs 커스텀 플러그인 · 주요 플러그인 · 설치·관리 · 플러그인의 미래 |
| 9 | OpenSearch in Action: Making Apps Awesome | OpenSearch 를 앱의 검색 엔진으로 삼아 API 연동 앱을 만든다 | Iva 시나리오 · API 기반 개발 · autocomplete·fuzzy · 필터·faceted · UI 통합 |
| 10 | OpenSearch Vectors and Generative AI | 벡터·의미 검색과 LLM/생성 AI 통합을 익힌다 | 벡터·의미 검색 · GPT·LLM · 챗봇·AI 에이전트 · RAG 계열 활용 |
| 11 | Migrate to OpenSearch | 조직이 OpenSearch 로 마이그레이션하는 이유와 단계를 파악한다 | Why OpenSearch · 마이그레이션 단계 · POC · 배포 · Migration Assistant |
| 12 | Security in OpenSearch | 인증·인가·FGAC·멀티테넌시로 보안 체계를 구축한다 | 보안 프레임워크 · 인증·인가 · 멀티테넌트 · 감사·컴플라이언스 |
| 13 | Monitoring, Backup, and Recovery | 모니터링·백업·재해복구로 운영 회복탄력성을 확보한다 | 도메인 모니터링 · 대시보드·알람 · admission control·backpressure · 백업 · DR(RPO·RTO) |
| 14 | Scaling and Performance Optimization | 분산 시스템 관점에서 클러스터 사이징·성능 튜닝을 한다 | 분산 시스템 · 클러스터 사이징 · 고성능 최적화 |

## 작성된 정독 노트

> **14개 장 전권 완료** (2026-07-10). 각 편은 07-04 책 요약 템플릿(9섹션)에 `Spring 앱 개발 관점`(면접 대비 바로 위)과 SVG 1장을 더한 구조입니다.

| 노트 | 범위 |
|------|------|
| [01-01 OpenSearch 개요 — 진화·핵심 역량·활용 사례](./01-01.OpenSearch%20개요%20—%20진화·핵심%20역량·활용%20사례.md) | 1장 전체 — 진화(ES 포크→Linux Foundation) · 분산 DB/ACID 트레이드오프 · 어휘 vs 시맨틱(벡터) 검색 · 로그 분석 · Hello OpenSearch |
| [02-01 설치와 구성 — 노드·클러스터·샤드·세그먼트](./02-01.설치와%20구성%20—%20노드·클러스터·샤드·세그먼트.md) | 2장 전체 — 노드 5종 · 클러스터 5단계 · 샤딩(해싱·primary/replica) · 세그먼트(flush·병합) · Java 호환·네트워크 포트 |
| [03-01 배포 옵션 — Amazon OpenSearch Service와 Serverless](./03-01.배포%20옵션%20—%20Amazon%20OpenSearch%20Service와%20Serverless.md) | 3장 전체 — 관리형 클러스터(domain·rightsizing·스케일링·스냅샷) vs 서버리스(컬렉션·OCU·pay-per-use) 대비 |
| [04-01 데이터 색인 — 인덱스·매핑·애널라이저](./04-01.데이터%20색인%20—%20인덱스·매핑·애널라이저.md) | 4장 전체 — 색인(`_doc`·`_bulk`) · dynamic vs explicit 매핑 · text vs keyword · 애널라이저 3단(char_filter·tokenizer·token_filter) · index template |
| [05-01 검색 핵심 API — 쿼리 처리와 leaf 쿼리](./05-01.검색%20핵심%20API%20—%20쿼리%20처리와%20leaf%20쿼리.md) | 5장 전체 — 쿼리 처리 4단계(매칭·병합·스코어링·페칭) · TF-IDF→BM25 · text vs term 쿼리 · 페이지네이션(from/size·scroll·PIT) |
| [06-01 고급 쿼리 — 복합·지리·faceted·percolation](./06-01.고급%20쿼리%20—%20복합·지리·faceted·percolation.md) | 6장 전체 — bool(must/should/filter·filter context) · 점수 조율(boost·dis_max·function_score·rescore) · geospatial(geo_distance/polygon·geohash_grid) · faceted(집계·근사성·버킷 폭발) · percolation(인터페이스 역전) · profile API |
| [07-01 분석과 시각화 — 집계·대시보드·관측성](./07-01.분석과%20시각화%20—%20집계·대시보드·관측성.md) | 7장 전체 — 집계 3유형(metric·bucket·pipeline·중첩·buckets_path) · Dashboards 시각화(line·bar·pie·TSVB·Vega·대시보드) · 관측성(로그·메트릭·트레이스·service map·PPL) · 저비용 로깅(primary/secondary·UltraWarm·Flint) |
| [08-01 플러그인 — 유형·주요 플러그인·아키텍처](./08-01.플러그인%20—%20유형·주요%20플러그인·아키텍처.md) | 8장 전체 — 유형(bundled·additional·custom·버전 호환) · 주요 플러그인(SQL·Alerting·ISM·Security·Sec Analytics·KNN·Neural·LTR) · 설치/관리(opensearch-plugin) · 커스텀 개발 5단계 · 라이프사이클(class-load·핫스왑 불가·DI) · extensions 미래 |
| [09-01 검색 앱 만들기 — autocomplete·fuzzy·faceted·UI](./09-01.검색%20앱%20만들기%20—%20autocomplete·fuzzy·faceted·UI.md) | 9장 전체 — Iva 시나리오(RDB 한계) · API 개발(opensearch-py·_search) · autocomplete(match_phrase_prefix) · fuzzy(fuzziness AUTO) · bool should 결합 · 필터·faceted(term·range·terms 집계) · Streamlit UI |
| [10-01 벡터·생성 AI — 시맨틱 검색과 RAG](./10-01.벡터·생성%20AI%20—%20시맨틱%20검색과%20RAG.md) | 10장 전체 — 벡터화(임베딩·dense vs sparse) · 시맨틱 검색(KNN·exact vs approximate) · HNSW/IVF(m·ef·centroid·FAISS) · ML Commons·Neural Search·파이프라인 · hybrid(정규화·결합) · RAG(환각 감소·conversational memory·Claude 3.5) |
| [11-01 마이그레이션 — 단계·무중단 패턴·Migration Assistant](./11-01.OpenSearch%20마이그레이션%20—%20단계·무중단%20패턴·Migration%20Assistant.md) | 11장 전체 — Why(오픈소스·생태계) · 소스별 동기(Solr·Algolia·Splunk·ES·CloudSearch) · 3단계(Planning·POC·Deploy) · 무중단 5패턴(dual-write·shadow read·blue-green·canary·cold replay) · Migration Assistant(메타데이터·traffic replay·snapshot) |
| [12-01 보안 — 인증·인가·FGAC·멀티테넌시](./12-01.보안%20—%20인증·인가·FGAC·멀티테넌시.md) | 12장 전체 — 다층 방어(인증·인가·암호화) · 구성요소(Users·Roles·Backend roles·Role mappings) · 인증(basic auth·SAML SSO) · FGAC 3종(DLS 문서·FLS 필드·FM 값) · 멀티테넌시(index-level vs document-level isolation) · 감사·컴플라이언스(JSON 로그·HIPAA/GDPR/PCI DSS·ISM) |
| [13-01 모니터링·백업·복구 — 지표·admission control·DR](./13-01.모니터링·백업·복구%20—%20지표·admission%20control·DR.md) | 13장 전체 — 모니터링 도구(CloudWatch·Prometheus·PA 5s·Datadog)·3유형 지표(Cluster·Node·Shard) · 과부하 방어 사다리(알람→admission control→Search Backpressure 429→circuit breaker 6종→JVM 92% 자동블록) · 트러블슈팅(red/yellow·저장 20%/20GB·1000샤드·ISM rollover) · 튜닝(refresh·bulk 5~15MiB·SSD·filter context) · 백업·DR(AWS 4모델·스냅샷 ISM/KMS·CCR active-passive·복구 후 검증) |
| [14-01 스케일링·성능 최적화 — 분산 구조·사이징·튜닝](./14-01.스케일링·성능%20최적화%20—%20분산%20구조·사이징·튜닝.md) | 14장 전체 — 분산 구조(노드 역할·요청 fan-out·스레드/큐 1000·HTTP 429=언더스케일) · 사이징 체인(저장 source/index 1:0.7·watermark 85/90/95→샤드 10~50GiB→CPU 1.5/샤드 67%→RAM 32GiB heap·25샤드/GiB→800) · 최적화(POC bottom-up/top-down·테넌시 siloed/pooled/hybrid·document routing·shard skew 배수 배치·수직/수평 스케일링) |

## 출처·톤 메모

- 원본: O'Reilly 학습 플랫폼 — *The Definitive Guide to OpenSearch* (ISBN 9781835885789, `learning.oreilly.com/library/view/the-definitive-guide/9781835885789`). 장별 목표·토픽은 각 챕터 PDF 앞머리에서 추출했습니다.
- 정독 노트는 **합니다체**로 쓰고, 형제 단행본 폴더(`07_devops/04_cicd/book/*`)와 동일하게 07-04 책 요약 템플릿 구조(핵심 요약 → 학습 목표 → 본문 정리 → 심화 학습 → 실무 적용 → 체크리스트 → 면접 관점 → 참고 자료)를 따릅니다. 각 편에 Mermaid 1장 이상을 두고, 책 밖 조사분은 본문 정리와 섹션을 분리해 출처 링크를 남깁니다.
