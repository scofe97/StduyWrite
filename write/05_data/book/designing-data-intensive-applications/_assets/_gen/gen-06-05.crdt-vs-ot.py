# 06-05 §3 — 동일 문자열("ice") 동시 삽입("nice" vs "ice!")에 대한 OT의 인덱스 위치 변환과 CRDT의 불변 식별자 무변환 수렴 데이터 흐름.
# 사실 출처: 06-05 §3(L54~L60), DDIA 2판 6장 Figure 6-11 및 "Conflict-free replicated datatypes and operational transformation" (PDF p.38).
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 638
H = LEG + 56

d = D(W, H, "06-05 · CRDT VS OT DATA FLOW", "동시 텍스트 삽입에 대한 OT와 CRDT의 병합 흐름",
      "동일 문자열('ice')에 대한 동시 삽입('nice' vs 'ice!')을 OT의 인덱스 변환과 CRDT의 불변 식별자 무변환 정렬로 각각 병합하는 데이터 흐름을 대조한다.",
      "초기 문자열 ice · OT 인덱스 변환 · CRDT 불변 식별자 정렬 · nice! 로 수렴")

# 공통 전제 상단 배너
d.box(24, 104, W - 48, 54, PAPER2, INFO, 1.1, r=6)
d.t(W / 2, 125, "초기 상태 및 동시 삽입: 두 레플리카 모두 문자열 'ice'에서 시작", 12, INK, KR, "middle", 600)
d.t(W / 2, 144, "레플리카 1은 앞에 'n' 삽입 · 레플리카 2는 뒤에 '!' 삽입 (목표 수렴: 'nice!')", 11, MUTED, KR, "middle")

# 1단계: 연산 생성 및 위치 표현
d.box(24, 176, 404, 72, PAPER, RULE, 0.9, r=6)
d.chip(226, 194, "1단계: 위치 인덱스 기록", INFO, 11)
d.t(226, 218, "삽입 위치를 정수 오프셋으로 기록", 11, INK, KR, "middle", 600)
d.t(226, 236, "R1: insert('n', at=0) · R2: insert('!', at=3)", 11, MUTED, MONO, "middle")

d.box(452, 176, 404, 72, PAPER, ACC, 1.2, r=6)
d.chip(654, 194, "1단계: 불변 식별자 부여", ACC, 11)
d.t(654, 218, "문자마다 고유·불변 ID 부여", 11, INK, KR, "middle", 600)
d.t(654, 236, "초기 ID: [1A: 'i', 2A: 'c', 3A: 'e'] (불변)", 11, MUTED, MONO, "middle")

d.arrow([(226, 248), (226, 272)], MUTED, "ar", 1.2)
d.arrow([(654, 248), (654, 272)], ACC, "acc", 1.4)

# 2단계: 연산 교환
d.box(24, 272, 404, 72, PAPER, RULE, 0.9, r=6)
d.chip(226, 290, "2단계: 연산 상호 교환", INFO, 11)
d.t(226, 314, "인덱스 기반 편집 연산 전송", 11, INK, KR, "middle", 600)
d.t(226, 332, "R1에 insert('!', at=3) · R2에 insert('n', at=0)", 11, MUTED, MONO, "middle")

d.box(452, 272, 404, 72, PAPER, ACC, 1.2, r=6)
d.chip(654, 290, "2단계: 상대 위치 연산 교환", ACC, 11)
d.t(654, 314, "선행 ID 기반 상대 위치 연산 전달", 11, INK, KR, "middle", 600)
d.t(654, 332, "R1: insert(4A:'n', nil 뒤) · R2: insert(4B:'!', 3A 뒤)", 11, MUTED, MONO, "middle")

d.arrow([(226, 344), (226, 368)], WARN, "warn", 1.2)
d.arrow([(654, 344), (654, 368)], OK, "ok", 1.4)

# 3단계: 병합 처리 메커니즘
d.tone(24, 368, 404, 96, WARN, 6, "14", 1.2)
d.chip(226, 386, "3단계: 인덱스 변환(Transformation)", WARN, 11)
d.t(226, 410, "오류: 'nice'의 index 3에 '!' 삽입 시 'nic!e' 결함", 11, WARN, KR, "middle", 600)
d.t(226, 428, "동시 연산 반영: 선행 'n' 삽입 감안하여 3 → 4 변환", 11, INK, KR, "middle")
d.t(226, 446, "변환 연산 적용: insert('!', at=4)", 11, OK, MONO, "middle", 600)

d.tone(452, 368, 404, 96, ACC, 6, "14", 1.4)
d.chip(654, 386, "3단계: 무변환 ID 상대 정렬", OK, 11)
d.t(654, 410, "인덱스 변환 불필요: 영구 불변 ID로 삽입 위치 확정", 11, OK, KR, "middle", 600)
d.t(654, 428, "R1은 '!' 를 3A('e') 뒤에 · R2는 'n' 을 맨 앞(nil)에", 11, INK, KR, "middle")
d.t(654, 446, "동시 삽입 시 문자 ID 순서로 결정론적 정렬", 11, ACC, KR, "middle")

d.arrow([(226, 464), (226, 488)], OK, "ok", 1.2)
d.arrow([(654, 464), (654, 488)], OK, "ok", 1.4)

# 4단계: 최종 결과 및 적용 분야
d.box(24, 488, 404, 76, PAPER2, OK, 1.1, r=6)
d.t(226, 510, "최종 수렴: 문자열 \"nice!\" 달성", 12, OK, KR, "middle", 600)
d.t(226, 530, "JSON sync engine: ShareDB", 11, MUTED, KR, "middle")
d.t(226, 546, "대표 적용: Google Docs (실시간 텍스트 협업)", 11, INFO, KR, "middle", 600)

d.box(452, 488, 404, 76, PAPER2, ACC, 1.4, r=6)
d.t(654, 510, "최종 수렴: 문자열 \"nice!\" 달성", 12, OK, KR, "middle", 600)
d.t(654, 530, "JSON sync engine: Automerge · Yjs", 11, MUTED, KR, "middle")
d.t(654, 546, "대표 적용: Redis Enterprise · Riak · Cosmos DB", 11, ACC, KR, "middle", 600)

# 하단 요약 배너
d.tone(24, 580, W - 48, 36, OK, 4, "14", 1.0)
d.t(W / 2, 602, "결론: OT는 인덱스를 변환해 병합 · CRDT는 불변 ID로 변환 없이 수렴 · 성능·기능 트레이드오프", 12, INK, KR, "middle", 600)

d.legend(LEG, [("OT 인덱스 방식", INFO), ("인덱스 오류 및 변환", WARN), ("CRDT 불변 ID (focal)", ACC), ("최종 일관 수렴", OK)])
d.save("06-05.crdt-vs-ot.svg")
