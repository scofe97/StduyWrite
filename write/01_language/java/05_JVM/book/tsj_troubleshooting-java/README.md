---
title: Troubleshooting Java (Laurențiu Spilcă) 정독 인덱스
tags: [java, troubleshooting, debugging, profiling, visualvm, study-index, moc]
status: draft
source:
  - 《Troubleshooting Java, 2nd Edition》(Laurențiu Spilcă, Manning)
related:
  - ./00-00.서문 — 트러블슈팅의 본질과 책 구성.md
  - ../README.md
updated: 2026-06-07
---


# Troubleshooting Java (Laurențiu Spilcă) 정독 인덱스
> 『Troubleshooting Java, 2판』의 장 단위 정독 노트 인덱스입니다 — 05_JVM 폴더의 네 번째 정독 대상 책

이 폴더는 단행본 『Troubleshooting Java, Second Edition』(Laurențiu Spilcă, Manning)의 정독 노트를 모읍니다. 상위 [`05_JVM/`](../README.md) 폴더가 책별로 정독 노트를 모으는 컨벤션을 따르되, 책 구분을 ch 누적 번호가 아니라 **책 전용 폴더**(`tsj_troubleshooting-java/`)로 합니다. 폴더명 `tsj`는 **T**rouble**s**hooting **J**ava에서 왔고, 《밑바닥까지 파헤치기》(접두 없음·ch01~13)·《JVM Performance Engineering》(`jpe`·ch14~22)·《Java Performance》(`jpf`)와 출처가 섞이지 않게 구분합니다.

파일명은 `{장 번호}-{편 순번}.{제목}.md` 형식입니다. 앞 번호는 책의 실제 장 번호(00=서문, 01~N=본문 장)이고, 뒤 번호는 그 장을 여러 편으로 쪼갠 순번입니다. 책 구분의 1차 기준은 각 노트의 `source` 필드입니다.

> **톤·시각화는 이 책 갈래에 한해 합니다체 + 핵심 요약 SVG 1장 + Mermaid를 씁니다.** 상위 폴더의 두 책(《밑바닥》·《JVM Performance Engineering》, 한다체·Mermaid only)과 다르고, 《Java Performance》(`jpf`) 갈래와 같은 방식입니다 — 합니다체 본문에 각 편마다 `_assets/`의 요약 SVG 1장을 도입부에 `![설명](./_assets/{슬러그}.svg)`로 **임베드**하고, 흐름·상태전이가 자연스러운 곳에 Mermaid를 더합니다. 5장부터는 개념적으로 중요한 원문 Figure도 *캡션 기반 개념도* SVG로 만들어 해당 섹션 본문에 임베드합니다(스크린샷 UI는 창작하지 않고 캡션에 명시된 사실만 도식화). 1~4장은 요약 SVG를 도입부에 임베드하도록 소급 정비했습니다.



## 정독 대상 책

| 항목 | 내용 |
|------|------|
| 제목 | Troubleshooting Java, Second Edition |
| 저자 | Laurențiu Spilcă (『Spring Security in Action』·『Spring Start Here』 저자) |
| 추천사 | Ben Evans (Java 챔피언, 『The Well-Grounded Java Developer』 저자) |
| 출판사 | Manning |

> ISBN·출판 연도·페이지·예제 코드 저장소는 원문 판권면을 확인하는 시점에 보강합니다. 책 구성은 추천사 기준으로 1부(디버깅·로그)·2부(리소스 소비·VisualVM)·3부(메모리)·마무리(분산 추적·분산 트랜잭션)로 나뉘며, 각 장의 세부 주제는 해당 장 원문을 받을 때 채웁니다.



## 장 ↔ 정독 노트 매핑

진척 컬럼: ⏳ = 진행 중, ✅ = 완료, ◻ = 미착수.

추천사가 알려 주는 부(Part) 구성을 *틀*로만 적어 둡니다. 각 장의 장 번호·제목·세부 주제는 해당 장 원문을 받는 시점에 확정합니다 — 본문을 받기 전에는 장 세부를 추측해 채우지 않습니다.

| 부·장 | 영역 | 노트 | 진척 |
|--------|------|------|------|
| 서문 | Foreword + Preface | [`00-00.서문 — 트러블슈팅의 본질과 책 구성`](./00-00.서문%20—%20트러블슈팅의%20본질과%20책%20구성.md) | ✅ 조사가 작성보다 길다·무료 도구(IntelliJ CE·VisualVM)·3부 구성·AI의 역할·대상 독자 |
| 1부 | 디버깅과 로그 (디버거 기법·조건부/비중단 중단점·로그) | — | ✅ 1~4장 완료 |
| └ 1장 | Starting to know your apps (도입) | [`01-01.코드 조사와 트러블슈팅 — 정의와 기법의 지형`](./01-01.코드%20조사와%20트러블슈팅%20—%20정의와%20기법의%20지형.md), [`01-02.조사 기법의 네 시나리오와 AI 활용`](./01-02.조사%20기법의%20네%20시나리오와%20AI%20활용.md) | ✅ 2편: 01-01 조사·트러블슈팅 정의·디버깅≠디버거·postmortem(§1.1), 01-02 네 시나리오(디버거·프로파일러·stub·Heisenbug·힙/스레드 덤프)+AI 활용(§1.2~1.4) |
| └ 2장 | Debugging techniques (디버거) | [`02-01.코드 읽기의 본질과 디버거 기초`](./02-01.코드%20읽기의%20본질과%20디버거%20기초.md), [`02-02.실행 스택 트레이스와 코드 네비게이션`](./02-02.실행%20스택%20트레이스와%20코드%20네비게이션.md), [`02-03.디버거가 부족한 다섯 가지 상황`](./02-03.디버거가%20부족한%20다섯%20가지%20상황.md) | ✅ 3편: 02-01 코드 읽기 비선형·cognitive plan·breakpoint·JDWP attach(§2.1~2.2), 02-02 스택 트레이스·Aspect 숨은 로직(Beer→Chocolate)·step over/into/out(§2.2.1~2.2.2), 02-03 디버거가 부족한 5상황(§2.3) |
| └ 3장 | Advanced debugging techniques (고급 디버깅) | [`03-01.조건부 중단점과 비중단 중단점`](./03-01.조건부%20중단점과%20비중단%20중단점.md), [`03-02.인메모리 데이터 변경과 프레임 되감기`](./03-02.인메모리%20데이터%20변경과%20프레임%20되감기.md) | ✅ 2편: 03-01 조건부 중단점(sum==0·성능비용·IDE차)·비중단 중단점(코드수정 없는 로그·환경 간 비교)(§3.1~3.2), 03-02 인메모리 데이터 변경(타입일치·immutability)·drop frame(step out과 차이·외부변경 undo 불가)(§3.3~3.4) |
| └ 4장 | Making the most of logs (로그) | [`04-01.로그로 조사하기`](./04-01.로그로%20조사하기.md), [`04-02.로그 영속화와 로깅 레벨`](./04-02.로그%20영속화와%20로깅%20레벨.md), [`04-03.로그가 일으키는 세 가지 문제`](./04-03.로그가%20일으키는%20세%20가지%20문제.md) | ✅ 3편: 04-01 로그 해부·과거vs현재·UTC·AI 분석·예외(위치≠근본원인)·호출자찾기·시간측정·멀티스레드(§4.1), 04-02 영속화(NoSQL/파일/RDB)·레벨 피라미드·Log4j(logger/appender/formatter·status≠level)(§4.2.1~4.2.2), 04-03 세 부작용(보안·GDPR/성능·모기→코끼리/유지보수성)(§4.2.3) |
| 2부 | 리소스 소비 (VisualVM·CPU 샘플링/instrumentation·Hibernate SQL·락) | — | ✅ 5~7장 완료 |
| └ 5장 | Identifying resource consumption problems using profiling techniques (프로파일러 도입·VisualVM) | [`05-01.프로파일러는 어디에 유용한가`](./05-01.프로파일러는%20어디에%20유용한가.md), [`05-02.VisualVM 설치와 CPU·스레드 관찰`](./05-02.VisualVM%20설치와%20CPU·스레드%20관찰.md), [`05-03.메모리 누수와 metaspace, AI 활용`](./05-03.메모리%20누수와%20metaspace,%20AI%20활용.md) | ✅ 3편: 05-01 프로파일러 정의(JVM 가로채 CPU·메모리·스레드·메서드소요)·세 용도·비정상 리소스(스레드/메모리누수)·샘플링 X-ray·느림(§도입~5.1), 05-02 VisualVM 설치(visualvm_jdkhome·-Djava.rmi.server.hostname)·producer-consumer race condition·좀비 신호(CPU50%+GC0%+메모리0)·synchronized 수정(§5.2.1~5.2.2), 05-03 메모리누수(peaks/valleys vs 계속차오름)·OOM위치≠근본원인·힙덤프(10장)·-Xmx임시방편·metaspace(Hibernate오용)·AI(§5.2.3~5.3) |
| └ 6장 | Finding hidden problems using profiling techniques (샘플링·instrumentation·SQL 쿼리) | [`06-01.샘플링으로 실행 코드 관찰`](./06-01.샘플링으로%20실행%20코드%20관찰.md), [`06-02.instrumentation과 JDBC SQL 가로채기`](./06-02.instrumentation과%20JDBC%20SQL%20가로채기.md), [`06-03.프레임워크가 만든 SQL과 criteria 함정`](./06-03.프레임워크가%20만든%20SQL과%20criteria%20함정.md) | ✅ 3편: 06-01 샘플링(2스텝·da-ch6-ex1 /demo 5초·CPU시간0=대기·getResponseCode 무죄·OpenFeign 동적프록시·AI export)(§도입~6.1), 06-02 instrumentation(호출횟수·`com.example.**`/`feign.**` 필터·`*`vs`**`)·da-ch6-ex2 N+1(findProduct 10회)·JDBC탭 가로채기(드라이버 직전 복사·스택트레이스)·native(JdbcTemplate)(§6.2~6.3.1), 06-03 Spring Data JPA(쿼리2개·Hibernate 최적화로 2nd 1회)·로그 한계(show-sql·파라미터 분리)·da-ch6-ex4 criteria from() 2회→cross join·Root 재사용 수정·N회 반복은 별건(§6.3.2~6.3.3) |
| └ 7장 | Investigating locks in multithreaded architectures (스레드 락·대기) | [`07-01.스레드 락 모니터링`](./07-01.스레드%20락%20모니터링.md), [`07-02.락 분석 — 자기 자신을 기다리는 스레드`](./07-02.락%20분석%20—%20자기%20자신을%20기다리는%20스레드.md), [`07-03.대기 스레드와 wait·notify 함정`](./07-03.대기%20스레드와%20wait·notify%20함정.md) | ✅ 3편: 07-01 락 정의·da-ch7-ex1 producer-consumer(ArrayList 모니터·synchronized·10초 sleep·백만 반복)·Threads 탭 교대 점유·locked(블록입구/join/블로킹객체)(§도입~7.1), 07-02 샘플링(총실행>CPU=대기)·self time 700ms≪4903ms="자기자신 기다림"=락·Locks 버튼·모니터 4476199c·상호차단 3698/3699·공정성/기아·JProfiler Keep VM Alive(§7.2), 07-03 락 vs 대기(입구막힘 vs 모니터 명시멈춤·경찰관비유)·da-ch7-ex2 wait()/notifyAll()·9초→50초 느려짐(대기만 이동·전환 더 느림)·"최적화는 측정하라"(§7.3) |
| 3부 | 스레드 덤프·메모리 (데드락·메모리 할당·누수 추적·힙 덤프·OQL·GC 로그) | — | ✅ 8~11장 완료 |
| └ 8장 | Investigating deadlocks with thread dumps (스레드 덤프·데드락) | [`08-01.스레드 덤프 획득`](./08-01.스레드%20덤프%20획득.md), [`08-02.스레드 덤프 읽기와 데드락 추적`](./08-02.스레드%20덤프%20읽기와%20데드락%20추적.md), [`08-03.fastThread와 AI로 덤프 읽기`](./08-03.fastThread와%20AI로%20덤프%20읽기.md) | ✅ 3편: 08-01 덤프=단일시점 스냅숏(샘플링과 대비)·da-ch8-ex1 중첩 synchronized(listA/listB 순서반대)→데드락·VisualVM Thread Dump 버튼·CLI(jps -l→jstack PID→File>Load)(§도입~8.1), 08-02 스레드 항목 해부(tid/nid/prio/상태/스택/락)·데드락 3단계 추적(안막힌것 필터→락ID(꺾쇠)따라가기→되돌아오면 데드락)·simple vs complex·cascading locks(외부이벤트 대기)·사진vs영화(§8.2.1), 08-03 raw읽기 토대·fastThread(데드락감지/의존성/플레임그래프)·AI비서(막힌스레드 단서·전용GPT)(§8.2.2) |
| └ 9장 | Profiling memory-related problems (메모리 할당) | [`09-01.메모리 샘플링으로 할당 문제 찾기`](./09-01.메모리%20샘플링으로%20할당%20문제%20찾기.md), [`09-02.프로파일링으로 범인 찾기`](./09-02.프로파일링으로%20범인%20찾기.md) | ✅ 2편: 09-01 CPU(5~8장)→메모리·신호(CPU낮은데 메모리↑→GC가 CPU 더씀)·Monitor 위젯·da-ch9-ex1 /products/1000000(백만 객체)·Sampler→Memory·두 상황(다수 소형 vs 소수 대형=비디오)·Live Bytes/Objects 정렬·프리미티브/문자열/JDK 건너뜀·Product 백만 인스턴스(§도입~9.1), 09-02 샘플링→프로파일링 전환("무엇을 프로파일할지 알기 전엔 안함")·FQN 표현식(Product/`.model.*`/`.**`)·live+total+GC세대·(+)버튼 스택트레이스로 생성지점=근본원인·역참조 안되면 OOM·힙덤프 예고(10장)(§9.2) |
| └ 10장 | Investigating memory problems with heap dumps (힙 덤프·OQL) | [`10-01.힙 덤프 획득`](./10-01.힙%20덤프%20획득.md), [`10-02.힙 덤프 읽기 — referrers와 누수`](./10-02.힙%20덤프%20읽기%20—%20referrers와%20누수.md), [`10-03.OQL로 힙 덤프 쿼리하기`](./10-03.OQL로%20힙%20덤프%20쿼리하기.md) | ✅ 3편: 10-01 힙덤프=메모리 스냅숏(모든 객체+관계)·세 획득법(`-XX:+HeapDumpOnOutOfMemoryError`+`-XX:HeapDumpPath` 자동/VisualVM Heap Dump 버튼/jps→`jmap -dump:format=b`)·da-ch10-ex1 static 리스트에 Product 무한add→OOM·Docker는 영속볼륨(§도입~10.1), 10-02 평문 못읽음(스레드덤프와 대비)·요약뷰로 올바른덤프 확인·Objects뷰 정렬(수·크기)·Product·referee(참조하는것) vs referrer(참조받는것)·GC는 referrer없어야 회수·static ArrayList 백만참조=누수·AI는 통째로 못맡김(4GB+)(§10.2), 10-03 OQL(SQL유사·덤프 비교)·`select p from model.Product p`·점연산자·JSON 프로젝션·where(>15)·`unique(referrers(p))`로 누수탐지(다수↔소수 referrer)·5함수용도(referee/referral/중복/하위상위/긴생명경로)(§10.3) |
| └ 11장 | Analyzing potential JVM problems with GC logs (GC 로그) | [`11-01.GC 로그 활성화와 힙 구조`](./11-01.GC%20로그%20활성화와%20힙%20구조.md), [`11-02.GC 로그 파일 저장과 로테이션`](./11-02.GC%20로그%20파일%20저장과%20로테이션.md), [`11-03.GC 로그로 문제 진단 네 시나리오`](./11-03.GC%20로그로%20문제%20진단%20네%20시나리오.md) | ✅ 3편: 11-01 GC로그=메모리 일기·기본꺼짐(`-Xlog:gc*`)·초기화로그(G1·JVM버전·CPU/메모리·힙 region/min/initial/max·병렬워커)·힙구조 Eden/Survivor/Old(옷장·나이=살아남은 사이클)·GC이벤트(타입+단계별ms·Eden 4->0·잘튜닝)(§도입~11.1), 11-02 콘솔 부적합→`file=`+time/uptime/level/tags·로테이션(filecount/filesize·오래된것 덮어씀)·레벨(error~trace 내림차순·상위 자동포함)·운영=error/warning·기본 info·깊은조사 staging debug/trace·GCeasy/AI(§11.2~11.3), 11-03 네 시나리오: 멈춤(0~50ms 정상·초과+잦으면 문제·25ms→2.5s/5.3s full)·누수(점점 덜 비움·full도 효과없음·계속차오름)·메모리부족(full이 효과적 비우되 잦음·peaks/valleys·-Xmx 단기/수평확장 근본)·병렬튜닝(8중2 과소→ParallelGCThreads↑·16 과다 CPU경합→↓·ConcGCThreads non-STW)(§11.4) |
| 마무리 | 시스템 수준 장애·서비스 통신·데이터 일관성 (분산 추적·직렬화·장애 모드·트랜잭션) | — | ✅ 12~13장 완료 (책 완독) |
| └ 12장 | Uncovering system-level failures and service communication problems (분산 추적·통신) | [`12-01.분산 추적 — trace ID와 span`](./12-01.분산%20추적%20—%20trace%20ID와%20span.md), [`12-02.직렬화·버전 불일치`](./12-02.직렬화·버전%20불일치.md), [`12-03.시스템 장애 모드 — cascading·retry·timeout`](./12-03.시스템%20장애%20모드%20—%20cascading·retry·timeout.md) | ✅ 3편: 12-01 장애=팀스포츠(메아리침)·누락주문 시나리오(checkout REST→order→Kafka→fulfillment)·trace ID=요청 여권(경계마다 찍힘·한곳 떨구면 끊김)·span=작업단위(중첩 트리·listing 12.1-3)·OpenTelemetry(생성)/Jaeger·Zipkin(수집·시각화)/Sentry(예외 보완)·SHIPPING_METHOD_DRONE enum 불일치(§도입~12.1), 12-02 직렬화 조용히 어긋남(드롭/기본값/특정상황 에러)·Protobuf+gRPC(.proto 자동생성·독립진화 함정)·payload 로깅(가시성vs안전: 디코딩만·샘플링·마스킹)·스키마검증(CI Buf로 현재vs이전·optional추가 안전/이름변경·타입변경 깨짐·런타임 Confluent Registry)(§12.2), 12-03 cascading(느린 하류가 상류 스레드 막음·풀고갈·WAITING 동일스택·에러던지는건 전령)·retry storm(백오프없는 동시재시도 증폭·트래픽없는 부하급증)·timeout mismatch(client 2초vs server 3초·client span 타임아웃/server span 성공·중복요청ID)·평균말고 P95/P99·시스템수준 사고(여러 렌즈)(§12.3) |
| └ 13장 | Measuring data consistency and transactions (분산 데이터 일관성·트랜잭션) | [`13-01.서비스 간 데이터 불일치 — 시간 이상과 도메인 불변식`](./13-01.서비스%20간%20데이터%20불일치%20—%20시간%20이상과%20도메인%20불변식.md), [`13-02.다단계 트랜잭션 추적 — 감사 로그와 이벤트 재생`](./13-02.다단계%20트랜잭션%20추적%20—%20감사%20로그와%20이벤트%20재생.md), [`13-03.일관성 측정 — 체크섬·해시와 reconciliation`](./13-03.일관성%20측정%20—%20체크섬·해시와%20reconciliation.md) | ✅ 3편: 13-01 일관성=움직이는 표적·시간기반 이상(1유로 사건: POS "Approved"→추적 payment-processing서 끊김→Kafka 미발행→DB ID시퀀스 갭→재시도 없이 조용히 abort된 PostgreSQL 데드락=조율 사각지대·낮은가치도 무시X·한도구론 부족 결합)·도메인 불변식(QA 농담·유령 환불·refund.orderId 존재 AND ts>order.ts·SQL NOT EXISTS·경쟁조건/최종일관성지연·reconciliation 주기스캔)(§13.1), 13-02 단일커밋 아닌 수십단계(Fig13.3)·감사로그=블랙박스(디버그=자기대화 vs 감사=바깥향함·다섯성질 immutable/structured/queryable/centralized/retained·listing13.1-3 마스킹·비번/JWT/스택트레이스 금지·재구성 4단계)·이벤트 드리븐(event=이미 일어난일·재생=스테이징 재트리거·Ahmed 환영이메일 누락→consumer group offset→잘못된 토픽 오설정→kafka-console-consumer/producer 재생·postmortem=학습)(§13.2), 13-03 일관성 기본보장X·silent drift(Fig13.7)·체크섬(CRC32/Adler-32 우발오류 1차방어) vs 해시(SHA-256/MD5 한방향·강함)·감사로그 hash필드·blast radius(1개↔수천 Fig13.8·spot-check)·reconciliation job(있어야할것vs실제·야간배치·shipped→paid·마지막 방어선·divide-and-conquer 파티션해시→per-invoice·stateless·충돌저항성)·책닫으며(한 줄→시스템 전체)(§13.3~13.4) |

> 미작성 장은 해당 장 원문이 들어올 때 비로소 노트를 만듭니다. 빈 노트 사전 생성은 하지 않습니다. 각 장은 원문 분량을 보고 분할안을 먼저 제안한 뒤 작성합니다.



## 작성 규칙

- 파일명: `{장 번호}-{편 순번}.{제목}.md` (00=서문, 01~N=본문 장)
- SVG 자산: `_assets/{장-편}.{슬러그}.svg`
- 프론트매터 필수 필드: `title`, `tags`, `status`, `source`(책 §범위 + 공식 스펙·도구 URL), `related`, `updated`
- 본문 톤: **합니다체** 통일, 문단형 우선, "왜?" 포함, AI 강조어("매우/굉장히/획기적/혁신적") 금지
- 시각화: 각 편에 핵심 요약 SVG 1장 필수(도입부에 `![…](./_assets/…svg)` 임베드) + 흐름·상태전이에 Mermaid. 비교는 표. 5장부터 주요 원문 Figure는 캡션 기반 개념도 SVG로 섹션 본문에 추가 임베드(스크린샷 UI 창작 금지)
- 원문 사실 불변: 코드·도구 옵션·수치·URL·인용은 원문과 1:1 일치. 본문 미수령 장의 세부 주제는 추측해 채우지 않음
- 노트 성격: 면접 대비 + 실무 도구 사용법 + 개념·이론을 함께 다루는 종합 학습 노트

상세 가드레일은 글로벌 하네스 `~/.claude/skills/content/writing/references/06-second-brain-harness.md` 참조.
