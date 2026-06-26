---
title: Java Performance (Scott Oaks) 정독 인덱스
tags: [jvm, performance, java-performance-oaks, study-index, moc]
status: final
source:
  - 《Java Performance, 2nd Edition》(Scott Oaks, O'Reilly, 2020)
related:
  - ./00-00.서문 — 책 소개와 2판 변경점.md
  - ../README.md
updated: 2026-06-05
---


# Java Performance (Scott Oaks) 정독 인덱스
> 『Java Performance, 2판』의 장 단위 정독 노트 인덱스입니다 — 05_JVM 폴더의 세 번째 정독 대상 책

이 폴더는 단행본 『Java Performance, Second Edition』(Scott Oaks, O'Reilly)의 정독 노트를 모읍니다. 상위 [`05_JVM/`](../README.md) 폴더가 책별로 정독 노트를 모으는 컨벤션을 따르되, 책 구분을 ch 누적 번호가 아니라 **책 전용 폴더**(`jpf_java-performance/`)로 합니다. 폴더명 `jpf`는 **J**ava **P**er**f**ormance에서 왔고, 《밑바닥까지 파헤치기》(접두 없음·ch01~13)·《JVM Performance Engineering》(`jpe`·ch14~22)와 출처가 섞이지 않게 구분합니다.

파일명은 `{장 번호}-{편 순번}.{제목}.md` 형식입니다. 앞 번호는 책의 실제 장 번호(00=서문, 01~12=본문 장)이고, 뒤 번호는 그 장을 여러 편으로 쪼갠 순번입니다. 책 구분의 1차 기준은 각 노트의 `source` 필드입니다.

> **톤·시각화는 이 책 갈래에 한해 합니다체 + 핵심 요약 SVG 1장 + Mermaid를 씁니다.** 상위 폴더의 다른 두 책(한다체·Mermaid only)과 다릅니다 — 이 책 노트는 합니다체 본문에 각 편마다 `_assets/`의 요약 SVG 1장을 두고, 흐름·상태전이가 자연스러운 곳에 Mermaid를 더합니다.



## 정독 대상 책

| 항목 | 내용 |
|------|------|
| 제목 | Java Performance, Second Edition |
| 저자 | Scott Oaks (전 Sun/Oracle Java Performance Group) |
| 출판사 | O'Reilly |
| 저작권 | 2020 |
| ISBN | 978-1-492-05611-9 |
| 대상 Java | Java 8 + Java 11 (LTS) |
| 예제 코드 | https://github.com/ScottOaks/JavaPerformanceTuning |

> 2판 신규 주제: G1 대규모 업데이트, Java Flight Recorder, 컨테이너 환경 동작, jmh 마이크로벤치마킹, 신규 JIT 컴파일러, AppCDS, compact string·string concatenation. 장 구성·페이지 정보는 각 장 원문 수령 시 보강합니다.



## 장 ↔ 정독 노트 매핑

진척 컬럼: ⏳ = 진행 중, ✅ = 완료, ◻ = 미착수.

| 장 | 영어 제목 | 노트 | 진척 |
|----|----------|------|------|
| 서문 | Preface | [`00-00.서문 — 책 소개와 2판 변경점`](./00-00.서문%20—%20책%20소개와%202판%20변경점.md) | ✅ 책 범위 3축·대상 독자·성능 작업 본질·환경 분기·2판 신규·표기 규약 |
| 1장 | Introduction | [`01-01.성능 — art와 science, 그리고 플랫폼·환경`](./01-01.성능%20—%20art와%20science,%20그리고%20플랫폼·환경.md), [`01-02.완전한 성능 이야기 — JVM 밖의 일곱 원칙`](./01-02.완전한%20성능%20이야기%20—%20JVM%20밖의%20일곱%20원칙.md) | ✅ 2편: 01-01 두 지식 축·HotSpot/LTS·플래그 문법·하이퍼스레딩·컨테이너 ergonomics, 01-02 일곱 원칙(알고리즘·코드 적게·결국 진다·섣부른 최적화·DB 병목·흔한 경우·요약) |
| 2장 | An Approach to Performance Testing | [`02-01.무엇을 측정할까 — 벤치마크 종류와 성능 지표`](./02-01.무엇을%20측정할까%20—%20벤치마크%20종류와%20성능%20지표.md), [`02-02.결과를 어떻게 믿을까 — 변동성과 통계, 일찍 자주`](./02-02.결과를%20어떻게%20믿을까%20—%20변동성과%20통계,%20일찍%20자주.md), [`02-03.벤치마크 실전 — jmh와 공통 예제 코드`](./02-03.벤치마크%20실전%20—%20jmh와%20공통%20예제%20코드.md) | ✅ 3편: 02-01 벤치마크 3종(micro 함정 4·macro·meso)·지표 3종(batch/throughput/response·평균vs백분위·이상치), 02-02 변동성(t-test·p-value·α·유의성≠중요성)·일찍자주(자동화·전수측정·타깃시스템), 02-03 jmh(trial/fork/iteration·Blackhole·@Param·@Setup Level)·공통예제(StockPrice·BigDecimal sqrt·JAX-RS) |
| 3장 | A Java Performance Toolbox | [`03-01.OS 레벨 도구 — CPU·디스크·네트워크`](./03-01.OS%20레벨%20도구%20—%20CPU·디스크·네트워크.md), [`03-02.JDK 기본 도구와 VM 정보·튜닝 플래그`](./03-02.JDK%20기본%20도구와%20VM%20정보·튜닝%20플래그.md), [`03-03.프로파일러 — sampling·instrumented·native`](./03-03.프로파일러%20—%20sampling·instrumented·native.md), [`03-04.Java Flight Recorder와 JMC`](./03-04.Java%20Flight%20Recorder와%20JMC.md) | ✅ 4편: 03-01 OS 도구(CPU user/system·idle 3이유·run queue·iostat·swapping·nicstat 40%), 03-02 JDK 도구 7종·VM 정보·PrintFlagsFinal(콜론·product/pd)·jinfo manageable·Docker, 03-03 프로파일러(sampling·safepoint bias·async·instrumented 호출수·flame/call tree·native), 03-04 JFR(circular buffer·131이벤트·jcmd JFR.*·proactive/reactive·default/profile 템플릿) |
| 4장 | Working with the JIT Compiler | [`04-01.JIT 기초와 tiered compilation`](./04-01.JIT%20기초와%20tiered%20compilation.md), [`04-02.code cache와 컴파일 관찰 — PrintCompilation·deoptimization`](./04-02.code%20cache와%20컴파일%20관찰%20—%20PrintCompilation·deoptimization.md), [`04-03.고급 컴파일러 플래그 — threshold·threads·inlining·escape analysis`](./04-03.고급%20컴파일러%20플래그%20—%20threshold·threads·inlining·escape%20analysis.md), [`04-04.GraalVM과 precompilation — AOT·native image`](./04-04.GraalVM과%20precompilation%20—%20AOT·native%20image.md) | ✅ 4편: 04-01 JIT 기초(컴파일/인터프리트/JIT·HotSpot·레지스터·C1/C2·tiered), 04-02 code cache(ReservedCodeCacheSize·JDK11 3분할)·PrintCompilation(OSR·attributes)·tiered 5레벨·deopt(not entrant/zombie), 04-03 고급 플래그(CompileThreshold·counter decay·CICompilerCount·inlining 35/325·escape analysis·AVX·javac), 04-04 GraalVM(JVMCI)·AOT(jaotc·compile-for-tiered)·native image(제약 7) |
| 5장 | An Introduction to Garbage Collection | [`05-01.GC 기초와 세대별 컬렉터`](./05-01.GC%20기초와%20세대별%20컬렉터.md), [`05-02.GC 알고리즘 선택 — serial·throughput·G1·CMS`](./05-02.GC%20알고리즘%20선택%20—%20serial·throughput·G1·CMS.md), [`05-03.기본 튜닝 (1) — 힙과 세대 크기`](./05-03.기본%20튜닝%20(1)%20—%20힙과%20세대%20크기.md), [`05-04.기본 튜닝 (2) — metaspace·병렬·GC 도구`](./05-04.기본%20튜닝%20(2)%20—%20metaspace·병렬·GC%20도구.md) | ✅ 4편: 05-01 GC 원리(GC root·reachable·compaction·STW)·세대(eden/survivor·minor/full·concurrent), 05-02 알고리즘(serial·throughput·G1·CMS·System.gc·선택 트레이드오프·sawtooth), 05-03 힙(swapping·Xms/Xmx·30% 규칙·NewRatio·adaptive sizing), 05-04 metaspace(permgen·classloader leak)·ParallelGCThreads·GC 로그(JDK8/11)·jstat |
| 6장 | Garbage Collection Algorithms | [`06-01.throughput collector 이해와 튜닝`](./06-01.throughput%20collector%20이해와%20튜닝.md), [`06-02.G1 GC 동작 — 4 연산과 5가지 full GC 실패`](./06-02.G1%20GC%20동작%20—%204%20연산과%205가지%20full%20GC%20실패.md), [`06-03.G1 GC 튜닝과 CMS`](./06-03.G1%20GC%20튜닝과%20CMS.md), [`06-04.고급 튜닝 — tenuring·TLAB·humongous·힙 제어`](./06-04.고급%20튜닝%20—%20tenuring·TLAB·humongous·힙%20제어.md), [`06-05.실험 GC — ZGC·Shenandoah·Epsilon과 선택 가이드`](./06-05.실험%20GC%20—%20ZGC·Shenandoah·Epsilon과%20선택%20가이드.md) | ✅ 5편: 06-01 throughput(minor/full 로그·MaxGCPauseMillis·GCTimeRatio), 06-02 G1 동작(region·4연산·concurrent cycle·5 full GC 실패), 06-03 G1 튜닝(IHOP·ConcGCThreads·MixedGCCountTarget)·CMS(phase·실패·튜닝), 06-04 고급(tenuring·survivor·TLAB·humongous·region·힙 제어), 06-05 실험 GC(ZGC·Shenandoah concurrent compaction·Epsilon·선택 가이드) |
| 7장 | Heap Memory Best Practices | [`07-01.힙 분석 — 히스토그램·힙 덤프·retained 메모리`](./07-01.힙%20분석%20—%20히스토그램·힙%20덤프·retained%20메모리.md), [`07-02.OutOfMemoryError 진단 — 네 가지 원인과 자동 덤프`](./07-02.OutOfMemoryError%20진단%20—%20네%20가지%20원인과%20자동%20덤프.md), [`07-03.메모리 적게 쓰기 — 객체 크기·lazy init·canonical`](./07-03.메모리%20적게%20쓰기%20—%20객체%20크기·lazy%20init·canonical.md), [`07-04.객체 재사용 — object pool·thread-local과 GC 비용`](./07-04.객체%20재사용%20—%20object%20pool·thread-local과%20GC%20비용.md), [`07-05.indefinite reference와 compressed oops`](./07-05.indefinite%20reference와%20compressed%20oops.md) | ✅ 5편: 07-01 힙 분석(histogram·heap dump·shallow/retained/deep·dominator·GC root·back trace), 07-02 OOM 4원인(native·metaspace·heap·GC overhead limit)·classloader 누수·자동 덤프, 07-03 메모리 절약(객체 크기·8byte 정렬·lazy init·DCL·eager deinit·canonical), 07-04 객체 재사용(live data 지배·pool 3특성·thread-local·ThreadLocalRandom 벤치), 07-05 indefinite ref(soft 공식·weak·WeakHashMap·finalizer·Cleaner·compressed oops) |
| 8장 | Native Memory Best Practices | [`08-01.footprint — committed vs reserved와 측정·최소화`](./08-01.footprint%20—%20committed%20vs%20reserved와%20측정·최소화.md), [`08-02.Native Memory Tracking — NMT와 shared library 한계`](./08-02.Native%20Memory%20Tracking%20—%20NMT와%20shared%20library%20한계.md), [`08-03.large pages — TLB와 OS별 huge page 설정`](./08-03.large%20pages%20—%20TLB와%20OS별%20huge%20page%20설정.md) | ✅ 3편: 08-01 footprint(heap+native·committed vs reserved·32/64비트 over-reserve·thread stack 예외·RSS/PSS/working set·최소화 4영역), 08-02 NMT(summary/detail·영역별 committed·baseline/diff·AutoShutdownNMT·shared library 미추적·Inflater/Deflater end()·NIO direct buffer·MaxDirectMemorySize·MALLOC_ARENA_MAX), 08-03 large pages(page·TLB·page table·전통 huge page nr_hugepages/memlock·transparent always/madvise/never·Windows Lock pages) |
| 9장 | Threading and Synchronization Performance | [`09-01.스레드 풀 — 크기 결정과 ThreadPoolExecutor`](./09-01.스레드%20풀%20—%20크기%20결정과%20ThreadPoolExecutor.md), [`09-02.ForkJoinPool — work stealing과 자동 병렬화`](./09-02.ForkJoinPool%20—%20work%20stealing과%20자동%20병렬화.md), [`09-03.동기화 비용 — Amdahl·register flushing·CAS`](./09-03.동기화%20비용%20—%20Amdahl·register%20flushing·CAS.md), [`09-04.동기화 회피와 false sharing`](./09-04.동기화%20회피와%20false%20sharing.md), [`09-05.JVM 스레드 튜닝과 모니터링`](./09-05.JVM%20스레드%20튜닝과%20모니터링.md) | ✅ 5편: 09-01 스레드 풀(하이퍼스레딩 5~6배·min/max·병목 위치·client 역설·TPE 3큐·KISS), 09-02 ForkJoinPool(fork/join 일시중지·balanced→partition·unbalanced→FJP·work stealing·leaf 47·parallelStream common pool), 09-03 동기화 비용(Amdahl·uninflated/inflated·CAS optimistic·JMM register flush·volatile·Vector SPARC), 09-04 동기화 회피(thread-local NumberFormat·CAS 4가이드·LongAdder·false sharing cache line·padding·@Contended), 09-05 JVM 튜닝(-Xss·native OOM 3원인·biased locking·priority·jconsole/JFR/jstack 상태별) |
| 10장 | Java Servers | [`10-01.NIO와 서버 스레드 풀 — selector·worker·async REST`](./10-01.NIO와%20서버%20스레드%20풀%20—%20selector·worker·async%20REST.md), [`10-02.비동기 outbound 호출 — HTTP client와 DB`](./10-02.비동기%20outbound%20호출%20—%20HTTP%20client와%20DB.md), [`10-03.JSON 처리 — 파싱 vs 마샬링과 객체 모델`](./10-03.JSON%20처리%20—%20파싱%20vs%20마샬링과%20객체%20모델.md) | ✅ 3편(+다이어그램 재현 2): 10-01 NIO(blocking 1:1·selector 이벤트 N→M·selector/worker 4구성·worker 수=동시 실행+block·blocking 20→nonblocking 2·JAX-RS @Suspended·503), 10-02 outbound(HttpClient static 재사용·pool throttle 안 함·maxConnections/connectionPoolSize·4 connector·NIO vs blocking async·aggregator·R2DBC·Loom fibers), 10-03 JSON(파싱 vs 마샬링·3기법·JSON-B vs Jackson ObjectMapper 단일·마샬 2318/7071/1549μs·pull parser 필터링·factory 재사용·159/86μs) |
| 11장 | Database Performance Best Practices | [`11-01.JDBC 기초 — 드라이버·connection pool·prepared statement`](./11-01.JDBC%20기초%20—%20드라이버·connection%20pool·prepared%20statement.md), [`11-02.JDBC 트랜잭션 — autocommit·batch·격리 수준·락`](./11-02.JDBC%20트랜잭션%20—%20autocommit·batch·격리%20수준·락.md), [`11-03.JDBC result set과 JPA 쓰기 최적화`](./11-03.JDBC%20result%20set과%20JPA%20쓰기%20최적화.md), [`11-04.JPA 읽기 최적화 — lazy·eager·JOIN·named query`](./11-04.JPA%20읽기%20최적화%20—%20lazy·eager·JOIN·named%20query.md), [`11-05.JPA 캐시와 Spring Data`](./11-05.JPA%20캐시와%20Spring%20Data.md) | ✅ 5편: 11-01 JDBC 기초(thin/thick·type 1~4·connection pool 스레드당 1·PreparedStatement connection별 pool·setMaxStatements), 11-02 트랜잭션(autocommit·batch 537→3.8초·격리 4수준·TRANSACTION_NONE·FOR UPDATE pessimistic·version optimistic·자동 재시도 안 함), 11-03 result set·JPA 쓰기(setFetchSize Oracle 10·bytecode enhance·-javaagent·cache-statements·batch-writing JPA 83→10초), 11-04 JPA 읽기(find/query/관계 3경로·@Lob lazy·fetch group·eager는 JOIN 아님·JPQL JOIN FETCH·named query 빠름), 11-05 캐시·Spring Data(L1/L2·쿼리는 L2 미적재·lazy/eager/JOIN 22.7/9.0/5.8초·쿼리 회피·soft/weak 사이징·Spring Data 4모듈) |
| 12장 | Java SE API Tips | [`12-01.String — compact string·interning·concatenation`](./12-01.String%20—%20compact%20string·interning·concatenation.md), [`12-02.Buffered IO와 classloading (CDS)`](./12-02.Buffered%20IO와%20classloading%20(CDS).md), [`12-03.Random·JNI·Exceptions`](./12-03.Random·JNI·Exceptions.md), [`12-04.Logging과 Collections`](./12-04.Logging과%20Collections.md), [`12-05.Lambda·Stream·Serialization`](./12-05.Lambda·Stream·Serialization.md) | ✅ 5편: 12-01 String(compact string heap 75%·중복제거 3방법 G1/intern/custom·고정 hash table 60013/65536·concat JDK8/11), 12-02 Buffered IO·CDS(1바이트 system call·ByteArray 이중복사·GZIP 21.3→5.7ms·CDS DumpLoadedClassList/Xshare·startup 30%), 12-03 Random·JNI·Exception(ThreadLocalRandom·SecureRandom entropy·JNI boundary 1천만→0·array pinning GC Locker·stack trace 깊이·system exception 재사용), 12-04 Logging·Collections(레벨 균형·isLoggable·sync/unsync 5~8ns·ArrayList 1.5배/StringBuilder 2배·lazy backing store), 12-05 Lambda·Stream·Serialization(lambda=anonymous·classloading만·stream lazy 0.76/108ms·transient·writeObject 함정·압축 lazy 해제·책 전체 요약) |

> 미작성 장은 해당 장 원문이 들어올 때 비로소 노트를 만듭니다. 빈 노트 사전 생성은 하지 않습니다. 각 장은 원문 분량을 보고 분할안을 먼저 제안한 뒤 작성합니다.



## 작성 규칙

- 파일명: `{장 번호}-{편 순번}.{제목}.md` (00=서문, 01~12=본문 장)
- SVG 자산: `_assets/{장-편}.{슬러그}.svg`
- 프론트매터 필수 필드: `title`, `tags`, `status`, `source`(책 §범위 + 공식 스펙 URL), `related`, `updated`
- 본문 톤: **합니다체** 통일, 문단형 우선, "왜?" 포함, AI 강조어("매우/굉장히/획기적/혁신적") 금지
- 시각화: 각 편에 핵심 요약 SVG 1장 필수 + 흐름·상태전이에 Mermaid. 비교는 표
- 원문 사실 불변: 코드·플래그·벤치마크 수치·URL·인용은 원문과 1:1 일치

상세 가드레일은 글로벌 하네스 `~/.claude/skills/content/writing/references/second-brain-harness.md` 참조.
