# [핸드오프] ch03_gc 측정·진단 실습 (2026-06-03, B방식=챕터 완독 후 몰아서)

경로: `write/01_language/java/05_JVM/ch03_gc/` · 실습 모듈: `_practice/ch03-gc/` (allocation·serial·parallel·cms·g1·zgc·shenandoah 존재)
실행 위치: Drive 밖 `~/jvm-practice` ([[project_jvm_practice_local_path]]) · Java 17 ([[feedback_tps_build_java17]] 아님, 학습용은 21 가능 확인 필요)

## 학습 완료 상태
- 01-01 GC운영(로그·튜닝), 01-02 Java성능(JMH·측정) — 4-Phase 학습 + SVG 보강 완료, 커밋 cb26e2c 푸시됨
- 시각화 새 규칙(SVG 1순위) 적용됨, Spring 렌즈 메모리 박제 ([[feedback_learning_docs_spring_lens]])

## 실습 TODO (정독 노트 02-01~02-08 마저 읽은 뒤 몰아서)
**핵심: 도구들이 하나의 진단 사이클로 물려 있으니 따로 말고 한 흐름으로.**
1. **[독립·아무때나] JMH** — `StringConcatBenchmark`(`+` vs StringBuilder) 실제 실행. Blackhole 빼면 결과 0 수렴 확인. 진단 사이클과 무관해 먼저 해도 됨.
2. **[사이클] 누수 시나리오 한 흐름**:
   - 일부러 누수 코드(static Map에 계속 put) 돌리기 → `-Xlog:gc*`로 GC 로그 관찰(01-01)
   - `jstat -gcutil`로 Old 점유율 우상향 확인(01-02 §4-2)
   - `jmap` 힙 덤프 → MAT/VisualVM으로 범인(안 죽는 Map) 찾기(01-02 §4-1)
   - JFR 떠서 JMC로 GC·CPU 전체 보기(01-02 §5-2)
3. **[보조] async-profiler** — CPU 먹는 코드 짜서 플레임 그래프 뽑기. 가장 넓은 상단 프레임 = 핫스팟.
4. 실습 후 각 노트 §실습 연결에 "직접 관찰한 것" 한 줄씩 기록(05ops/04api 패턴처럼).

## 완료 시 본 섹션 삭제

---

# 핸드오프: 02_Jenkins/04_api Phase 4 톤 개편

## 현재 상태 (2026-05-29, 커밋 a6a087f 푸시 완료, origin 동기 0/0)

레포: github.com/scofe97/StduyWrite (라벨 [runners-high]/[StduyWrite])
경로: write/07_devops/02_Jenkins/04_api/ (28편)

### ✅ 완료 (한다체 0 검증됨, 전 파일)
- 28편 전부 **종결 한다체 0건** (일반규칙 변환기 v3 적용, 코드/URL/펜스 무결성 검증)
- 변환기: /tmp/conv3.py (핵심: '~니다' 종결이면 변환 skip → 이중변환 방지)

### 구조(§학습목표/§면접/Mermaid) 적용 현황
- ✅ 적용 완료: 01-점검, 01-00, 01-01, 01-01a, 01-02, 01-02a, 01-02b,
  01-03, 01-03a, 01-04, 01-04a, 01-04b, 01-04c, 01-04d, 01-04e,
  01-05, 01-05a, 01-05b, 01-06, 01-06a, 01-06b, 01-06c
- ⬜ **구조 미적용 (G8/G9 6편)** — 한다체만 변환됨, §학습목표·§면접·Mermaid 추가 필요:
  - 01-07 (Mer 0) — §학습목표/§사전지식 + Mermaid 2(자원계층, 마스킹비대칭) + §면접/정답
  - 01-07a (Mer 0) — + Mermaid 2(바인딩흐름, 보안방어선) + §면접/정답
  - 01-07b (Mer 3 충분) — §학습목표/§사전지식 + §면접/정답만
  - 01-08 (Mer 0, 619줄) — + Mermaid 2(승인흐름, 헬스체크) + §면접/정답. 800 주의
  - 01-08a (Mer 1) — + Mermaid 1 + §면접/정답
  - 01-09 (Mer 1) — + Mermaid 1(depth/tree 비교) + §면접/정답

## 다음 세션 작업 = G8/G9 6편 구조 추가만

### 방법 (반드시 준수 — 이번 세션 사고 교훈)
1. **python conv3.py로 한다체는 이미 끝남.** 구조 추가만 하면 됨.
2. 구조 추가는 **anchor를 실제 파일의 현재 텍스트(합니다체 변환 후)로** 잡아야 함.
   assert로 anchor count==1 확인하고, 실패하면 그 파일 헤더 다시 grep해서 정확한 anchor 사용.
3. **검증 게이트 (커밋 전 필수, 통과 못 하면 커밋 금지):**
   - 종결 한다체: `python3`로 `([가-힣]{2,})다([.:]|$)` 중 어간이 '니'로 안 끝나는 것 = 0
   - 이중변환: 파일에 '니입니다' 문자열 0
   - Mermaid ≥ 2 (01-07b·01-08a·01-09는 기존 포함해서 ≥2 확인)
   - 펜스(```) 짝수, ≤800줄
   - 코드블록/URL: 직전 커밋 대비 변경 0 (python으로 codeblock·URL 비교)
4. **atomic write**: os.open+O_TRUNC+fsync+os.replace, 체크섬 일치 확인 후 git.
5. PRE-COMMIT GATE: git diff --cached --name-status 로 04_api만 staged 확인.
6. 커밋 라벨 [runners-high], #time, push 후 sync 0/0 확인.

## 다음다음 = Phase 5 (05_operations 14편, Groovy 642줄 파일 포함)

## 이번 세션 교훈 (메모리 박제됨)
- feedback_drive_edit_verify_before_commit.md: python+Edit 혼용 금지, grep FAIL 보고 커밋 금지
- 추가 교훈: term-dict 변환기는 미등록 동사/copula/`다:` 놓침 → 일반규칙 변환기 사용.
  '~니다' 종결 skip 안 하면 이중변환('다룹니다→다룹니입니다') 발생.


---

## [핸드오프] 03_network realtime 재구성 후속 (2026-05-30 세션)

이번 세션 완료: reactive-net 7편(01-01~01-07) + realtime 10편(websocket→realtime 리네임 + 새 노션자료 이론 보강) **main 커밋·푸시 완료**.

다음 세션 우선순위:

1. **[P1-A] `동기 비동기` raw 흡수** — `write/11_spring/_notion_import/netty/[Spring Netty] 동기 비동기.md` 가 reactive-net 01-02 본문·MOC 표에 미반영. 동기/비동기·블로킹/논블로킹 4분면 이론을 01-02에 흡수하거나 별도 편 분리 + MOC 등재. (<1h, reactive-net 완결 조건)
2. **[P1-B] realtime 10편 육안 검토** — 검증(grep 5종)은 통과했으나 사용자 본문 검토 미완. Spring 구현(SseEmitter·WebSocketHandler·STOMP) 환각 위험. 편당 ~5분.
3. **[P2-C] _notion_import raw archive/폐기** — reactive-net·realtime 이관 완료. A 완료 후 netty/·websocket/ raw 처리 결정.
4. **[P2-D] feign 예외처리 풀편** — ErrorDecoder·RetryableException·fallback. 현재 압축본 2편만.
5. **[P3-E] React/JS 프론트 트랙 여부** — 노션 자료 9편의 프론트 부분 이번에 제외함. 별도 트랙 만들지 미정.

작업 원칙: 외부자료는 프론트 제외+Spring 보강([[feedback_external_source_strip_framework_code]]), 이관 전 관점 질문([[feedback_external_import_perspective_first]]), Drive sequential mv+atomic write, 커밋 직전 staged 인덱스 전체 확인(무관 변경 섞임 주의 — 워킹트리에 08_cloud/10_security 등 동시세션 변경 다수 있었음).
