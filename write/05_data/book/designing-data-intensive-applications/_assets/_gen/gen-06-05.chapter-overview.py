# 06-05 개요 — 다중 리더의 동시 쓰기 충돌과 네 가지 해소 전략의 지형을 조망하는 전체 지도.
# 사실 출처: 06-05 본문 도입부(L21~L23), §1(L30~L32), §2(L41~L47), §3(L54~L60).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 280
LEG = PY + PH + 36
H = LEG + 56

d = D(W, H, "06-05 · CHAPTER OVERVIEW", "쓰기 충돌 해소 전체 지도",
      "다중 리더 환경에서 발생하는 동시 쓰기 충돌의 회피부터, LWW의 데이터 손실과 수동 해소의 형제 값 보존, CRDT와 OT를 통한 알고리즘적 자동 수렴까지의 해소 지형을 조망한다.",
      "충돌 회피 · LWW 폐기 · 형제 값 보존 · strong eventual consistency 자동 수렴")

# 상단 현실 배너 (공통 전제 축)
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "다중 리더 복제 현실: 비동기 복제 시 동시(concurrent) 쓰기 충돌 발생", 12, INK, KR, "middle", 600)

CW = 264
GAP = 20
X0 = 24

cards = [
    ("§1", "충돌 회피와 LWW", "단순 해소와 데이터 손실",
     [("충돌 회피(avoidance)", "특정 레코드 쓰기 동일 리더 고정"),
      ("회피의 한계", "지정 리더를 바꾸는 순간 회피가 깨짐"),
      ("LWW(last write wins)", "최대 타임스탬프 채택·나머지 폐기"),
      ("LWW의 대가", "수렴하지만 데이터 손실")],
     INFO),
    ("§2", "수동 해소와 자동 해소", "형제 값 보존과 수렴 보장",
     [("수동 해소(siblings)", "동시 값 모두 보존·조회 시 반환"),
      ("API 변경 부담", "단일 값 필드가 형제 집합으로 변경"),
      ("삭제 부활 함정", "합집합 병합 시 삭제 항목 부활"),
      ("자동 해소", "도착 순서와 무관하게 같은 상태로 수렴")],
     WARN),
    ("§3", "CRDT와 OT", "알고리즘으로 자동 수렴",
     [("OT(operational trans.)", "연산 인덱스 기록 후 동시 연산 변환"),
      ("CRDT(conflict-free)", "문자별 불변 ID 부여·무변환 정렬"),
      ("적용 분야 대조", "OT 협업 문서 · CRDT 분산 DB"),
      ("자동 병합의 한계", "'리스트 5개 이하' 같은 제약은 깨짐")],
     ACC),
]

FOCAL = 2

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 24, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT if not is_focal else ACC, KR, "middle")

    # 카드 내부 4개 항목 박스
    for j, (term, desc_text) in enumerate(items):
        iy = PY + 64 + j * 50
        d.box(x + 10, iy, CW - 20, 44, PAPER, RULE, 0.7)
        d.t(x + 20, iy + 18, term, 11, card_c if is_focal else INK, KR, "start", 600)
        d.t(x + 20, iy + 34, desc_text, 11, MUTED, KR, "start")

# 카드 간 진행 화살표
d.arrow([(X0 + CW + 2, PY + PH / 2), (X0 + CW + GAP - 2, PY + PH / 2)], MUTED, "ar", 1.2)
d.arrow([(X0 + 2 * CW + GAP + 2, PY + PH / 2), (X0 + 2 * (CW + GAP) - 2, PY + PH / 2)], ACC, "acc", 1.4)

d.legend(LEG, [("회피·단순 폐기 전략", INFO), ("형제 보존·위험 요소", WARN), ("자동 수렴 (focal)", ACC)])
d.save("06-05.chapter-overview.svg")
