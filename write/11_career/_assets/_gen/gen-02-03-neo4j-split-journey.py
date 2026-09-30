# 02-03 Neo4j 분할 사례 — 저장공간이 찼다는 운영 질문 하나가 다음 질문을 부르며 내려간다.
# 초점은 "어떻게 나눌까" 가 "무엇을 함께 둘까" 로 바뀌는 지점. 그 뒤가 공부 범위다.
# 타입 스펙: type-flowchart — 위에서 아래로 흐르는 질문 열, 오른쪽에 각 단계가 새로 만든 문제.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 800, 830
CX, NW, NH = 40, 300, 50
Y0, GAP = 108, 62
RX = 380

d = D(W, H, "11_CAREER · GREEDYCON · KANG DAEMYUNG",
      "운영 질문 하나가 만드는 질문의 연쇄",
      "Neo4j 한 대의 저장공간이 찼다는 문제에서 출발해, 절반 분할이 만든 서버 간 간선, 지역성과 균등의 충돌, "
      "질의 기록 확인을 거쳐 질문이 '무엇을 함께 둘까' 로 바뀐다. 그 뒤로 분할 방식·슈퍼노드·복제·재분할이 공부 범위로 정해진다.",
      lead="질문이 바뀌는 지점부터 공부 범위가 정해집니다")

# (단계, 부제, 오른쪽 메모, 색, focal)
STEPS = [
    ("저장공간 부족",       "1.4 TB / 디스크 1.0 TB",     "서버 한 대 추가",             INFO, False),
    ("절반 분할",       "첫 번째 생각 · 문서 보기 전", "서버를 넘는 간선",            INFO, False),
    ("서버 경계를 넘는 탐색", "사용자 A · 상품 B",          "간선마다 네트워크 왕복",       INFO, False),
    ("지역성 vs 저장량 균등", "두 목표의 충돌",              "동시에 만족하기 어려움",       INFO, False),
    ("실제 질의 기록 확인",   "이웃 조회 · 다단계 · 전체 분석", "구조가 아니라 질의가 답",   INFO, False),
    ("무엇을 함께 둘까",      "질문이 바뀐 지점",            "그래프 파티셔닝 공부 시작",    ACC,  True),
    ("edge cut · vertex cut", "읽기 · 쓰기 비율",            "동기화 비용",                 INFO, False),
    ("슈퍼노드",              "연결이 몰린 노드 하나",        "노드 수 균등해도 부하 집중",   INFO, False),
    ("복제의 대가",           "읽기 빠름 · 쓰기 동기화",      "일관성 비용",                 INFO, False),
    ("시간이 만든 문제",      "간선 증가 · 인기 노드 변화",   "데이터 이동 · 재분할",        OK,   False),
]

def y(k): return Y0 + k * GAP

for k, (name, sub, memo, c, focal) in enumerate(STEPS):
    yy = y(k)
    if focal:
        d.tone(CX, yy, NW, NH, ACC, 6)
    elif k == len(STEPS) - 1:
        d.tone(CX, yy, NW, NH, OK, 6)
    else:
        d.box(CX, yy, NW, NH, PAPER2, RULE, 0.9, 6)
    col = ACC if focal else (OK if k == len(STEPS) - 1 else INK)
    d.t(CX + 14, yy + 21, name, 13, col, KR, "start", 600)
    d.t(CX + 14, yy + 38, sub, 11, SOFT, KR, "start")
    if k < len(STEPS) - 1:
        d.arrow([(CX + NW / 2, yy + NH), (CX + NW / 2, y(k + 1) - 3)], MUTED, "ar", 1.3)
    # 오른쪽 — 이 단계가 새로 만든 문제 또는 얻은 것
    mc = ACC if focal else (BAD if k in (1, 2, 6, 7, 8) else MUTED)
    d.line(CX + NW + 6, yy + NH / 2, RX - 8, yy + NH / 2, RULE, 0.8, "2 3")
    d.t(RX, yy + NH / 2 + 4, memo, 11, mc, KR, "start")

# 초점 구간 괄호 — 여기부터 공부 범위
bx = 560
top, bot = y(5), y(9) + NH
d.line(bx, top, bx, bot, ACC, 1.2)
d.line(bx - 6, top, bx, top, ACC, 1.2); d.line(bx - 6, bot, bx, bot, ACC, 1.2)
d.t(bx + 10, (top + bot) / 2 - 6, "공부하게 된 것", 11, ACC, KR, "start", 600)
d.t(bx + 10, (top + bot) / 2 + 10, "파티셔닝 · 네트워크 비용", 11, SOFT, KR, "start")
d.t(bx + 10, (top + bot) / 2 + 24, "복제 · 일관성 · 재배치", 11, SOFT, KR, "start")

d.legend(H - 56, [("초점 — 질문이 바뀐 지점", ACC), ("새로 생긴 문제", BAD), ("운영 중 반복되는 결정", OK)])
d.save(os.path.join(os.path.dirname(__file__), "..", "02-03.neo4j-split-journey.svg"))
