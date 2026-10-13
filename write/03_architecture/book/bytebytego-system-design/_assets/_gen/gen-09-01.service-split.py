# 타입 스펙: type-architecture — 로드 밸런서 뒤에서 경로로 갈리는 두 서비스와 데이터베이스 클러스터(주 하나·복제본 셋)의 읽기·쓰기·복제 연결. 초점은 복제본에서만 읽는 LBS.
# 사실 출처: PDF 145쪽 그림(Load balancer, /search/nearby → Local Based Service → Read 셋 → Replica 셋, /businesses/{id} → Business Service → Write → Primary, Primary 에서 Replica 로 Replicate)과
#   추출본 v1.txt 3553~3597행(사업장 서비스: 추가·삭제·수정·상세 보기, LBS: 반경과 위치를 받아 근처 목록 반환).
# Layout conventions: 노드 높이 36~52, 신뢰 경계 대신 DB 클러스터를 점선 영역으로 묶음, 직각 화살표만 사용. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 632
d = D(W, H, "BYTEBYTEGO · 09-01 §2",
      "경로 둘이 서비스 둘로 갈리고 읽기는 복제본으로 간다",
      "/search/nearby 는 LBS 가 복제본 셋에서 읽고 /businesses/{id} 는 사업장 서비스가 주 DB 에 씁니다.",
      "복제본 3 · 주 DB 1 은 설계 예의 구성입니다")


def fam(s):
    return KR if any("가" <= ch <= "힣" for ch in s) else MONO


def node(cx, y, w, h, title, sub=None, focal=False, c=INFO):
    x = cx - w / 2
    if focal:
        d.tone(x, y, w, h, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 0.9, 6)
    col = ACC if focal else INK
    if sub:
        d.t(cx, y + 22, title, 13, col, fam(title), "middle", 600)
        d.t(cx, y + 42, sub, 12, MUTED, fam(sub), "middle")
    else:
        d.t(cx, y + h / 2 + 5, title, 13, col, fam(title), "middle", 600)


# 영역: 데이터베이스 클러스터.
d.o.append(f'<rect x="12" y="384" width="936" height="164" rx="8" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(932, 408, "데이터베이스 클러스터", 12, SOFT, KR, "end")

USER, LB, SVC, DB = 92, 160, 264, 432
LBS_X, BIZ_X, PRI_X = 252, 708, 708
REP = [108, 252, 396]

# 화살표는 노드보다 먼저 그린다.
d.arrow([(480, USER + 36), (480, LB)], MUTED, "ar", 1.4)
d.arrow([(480, LB + 40), (480, 232), (LBS_X, 232), (LBS_X, SVC)], MUTED, "ar", 1.4)
d.arrow([(480, LB + 40), (480, 232), (BIZ_X, 232), (BIZ_X, SVC)], MUTED, "ar", 1.4)
for rx in REP:
    d.arrow([(LBS_X, SVC + 52), (LBS_X, 352), (rx, 352), (rx, DB)], INFO, "info", 1.4)
d.arrow([(BIZ_X, SVC + 52), (BIZ_X, DB)], WARN, "warn", 1.4)
for rx in REP:
    d.arrow([(PRI_X, DB + 52), (PRI_X, 520), (rx, 520), (rx, DB + 52)], MUTED, "ar", 1.2, "4 3")

node(480, USER, 120, 36, "사용자")
node(480, LB, 160, 40, "로드 밸런서")
node(LBS_X, SVC, 232, 52, "LBS", "반경·위치 → 근처 목록", focal=True)
node(BIZ_X, SVC, 232, 52, "사업장 서비스", "추가·삭제·수정·상세")
for rx in REP:
    node(rx, DB, 128, 52, "복제본", "읽기")
node(PRI_X, DB, 160, 52, "주 DB", "쓰기")

d.chip(366, 232, "/search/nearby", MUTED, 11)
d.chip(594, 232, "/businesses/{id}", MUTED, 11)
d.chip(LBS_X, 352, "읽기", INFO, 11)
d.chip(BIZ_X, 360, "쓰기", WARN, 11)
d.chip(558, 520, "복제", MUTED, 11)

d.legend(H - 48, [("읽기 경로가 닿는 LBS", ACC), ("읽기", INFO), ("쓰기", WARN)])
d.save("09-01.service-split.svg")
