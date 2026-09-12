# 2026-09-08 B 문항 — 하위 서비스 하나의 타임아웃이 클러스터 전면 장애가 되기까지.
# 논지는 두 가지다. 단계마다 배수가 곱해진다는 것, 그리고 마지막이 처음으로 되돌아와
# 스스로를 먹여 살린다는 것. 그래서 단순 직선이 아니라 되먹임 고리로 그린다.
# focal 은 CoreDNS — 여기가 끊어지는 지점이고 복구도 여기서 이뤄졌다.
# 타입 스펙: type-flowchart — 위에서 아래로 흐르는 단계, 오른쪽에 증폭 배수,
#           마지막에서 위로 돌아가는 되먹임 경로.
#   type-loop 를 검토했으나 기각. loop 는 원형 링 위를 돌며 중앙 허브에 상태가
#   누적되는 구조(점선 스포크가 정의 신호)이고, 스펙이 "경로가 끝나거나 결과로
#   분기하면 flowchart 를 택하라"고 명시한다. 이 사고는 한 방향으로 끝나는
#   경로에 되먹임 화살표 하나가 곁가지로 붙은 형태이고 공유 허브가 없다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 800, 660
CX, NW, NH = 214, 320, 54
Y0, GAP = 112, 72

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-08 B",
      "작은 실패가 전면 장애가 되기까지",
      "핵심이 아닌 하위 서비스 하나의 타임아웃이 클러스터 전체 이름 해석을 무너뜨린 경로. "
      "단계마다 배수가 곱해지고, 마지막이 처음으로 되돌아와 스스로를 먹여 살린다. "
      "강조된 CoreDNS 가 끊어진 지점이자 복구가 이뤄진 지점이다.",
      lead="아무도 큰 실수를 하지 않았고 흔한 기본값들이 곱해졌습니다")

# (제목, 부제, 오른쪽 배수 라벨, 색)
STEPS = [
    ("부가 정보 서비스 타임아웃", "없어도 되는 의존 하나",        None,              INFO),
    ("집계 계층이 404 반환",      "503 이 맞는 자리",             "재시도 억제 안 됨", WARN),
    ("재시도로 인입 급증",         "사용자 · CDN · 클라이언트",     "요청 x N",         WARN),
    ("호출마다 이름 해석",         "커넥션 재사용 없음 · 캐시 없음",  "해석 x 하위 서비스 수", WARN),
    ("search 확장",              "ndots:5",                     "질의 x 10",        WARN),
    ("CoreDNS OOMKilled",        "limit 100Mi · 과거 사용량 기준",  "크래시 루프",      ACC),
    ("클러스터 전체 이름 해석 불가", "모든 Pod 가 공유하는 하나",     None,              BAD),
]

def y(k): return Y0 + k * GAP

for k, (name, sub, mult, c) in enumerate(STEPS):
    yy = y(k)
    if c is ACC:
        d.tone(CX, yy, NW, NH, ACC, 6)
    elif c is BAD:
        d.tone(CX, yy, NW, NH, BAD, 6)
    else:
        d.box(CX, yy, NW, NH, PAPER2, RULE, 0.9, 6)
    col = c if c in (ACC, BAD) else INK
    d.t(CX + 16, yy + 23, name, 13, col, KR, "start", 600)
    d.t(CX + 16, yy + 41, sub, 11, SOFT, KR, "start")
    if k < len(STEPS) - 1:
        d.arrow([(CX + NW / 2, yy + NH), (CX + NW / 2, y(k + 1) - 3)], MUTED, "ar", 1.3)
    if mult:
        d.t(CX + NW + 18, yy + NH / 2 + 4, mult, 11, WARN if c is not ACC else ACC, MONO, "start")

# 되먹임 — 마지막에서 집계 계층(404)으로 되돌아간다
lx = CX - 26
last, back = y(6) + NH / 2, y(1) + NH / 2
d.path(f"M {CX} {last} L {lx} {last} L {lx} {back} L {CX - 3} {back}", BAD, 1.3, "bad", "4 3")
d.o.append(f'<text x="{lx - 12}" y="{(last + back) / 2}" text-anchor="middle" '
           f'font-family="{KR}" font-size="11" fill="{BAD}" '
           f'transform="rotate(-90 {lx - 12} {(last + back) / 2})">이름을 못 찾아 404 가 늘어납니다</text>')

d.legend(H - 54, [("끊어진 지점이자 복구 지점", ACC), ("사고가 스스로를 먹여 살린 고리", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-08.dns-cascade.svg"))
print("ok dns-cascade")
