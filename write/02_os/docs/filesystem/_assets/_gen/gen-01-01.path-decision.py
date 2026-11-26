# 01-01 §3 관리 주체별 설치 경로 결정 흐름.
# 타입 스펙: type-flowchart — 외부 노출 여부와 관리 주체 순서로 설치·데이터 경로를 가르는 흐름도.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 920, 684
d = D(W, H, "FHS 3.0 · OWNERSHIP & EXPOSURE",
      "외부 노출과 관리 주체로 설치 경로 결정",
      "먼저 외부 노출 서비스 데이터(/srv)를 가른 뒤, 배포판 패키지·관리자 로컬 설치·통짜 추가 패키지 순으로 설치 트리를 분기하고 비노출 상태는 /var/lib 로 보내는 흐름도.",
      "외부 노출 데이터를 먼저 가르고, 소프트웨어는 관리 주체 순으로 설치 트리를 나눕니다")

CX = 212
RX, RW, RH = 464, 428, 64
DYS = [204, 300, 396, 492]
R5Y = 556

def diamond_pts(cx, cy, hw=144, hh=32):
    return f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"

# 1. 커넥터 먼저 (z-order)
d.arrow([(CX, 144), (CX, DYS[0] - 34)], MUTED, "ar", 1.4)
for i in range(3):
    d.arrow([(CX, DYS[i] + 32), (CX, DYS[i + 1] - 34)], MUTED, "ar", 1.4)
    d.t(CX - 16, (DYS[i] + 32 + DYS[i + 1] - 32) // 2 + 4, "NO", 11, MUTED, MONO, "end", 600)

# D4 NO → R5 (직각 L-elbow)
d.arrow([(CX, DYS[3] + 32), (CX, R5Y + 28), (RX - 2, R5Y + 28)], INFO, "info", 1.4)
d.t(CX - 16, DYS[3] + 64, "NO", 11, INFO, MONO, "end", 600)

# D1~D4 YES → R1~R4
yes_colors = [(OK, "ok"), (INFO, "info"), (OK, "ok"), (WARN, "warn")]
for i, cy in enumerate(DYS):
    col, mk = yes_colors[i]
    d.arrow([(CX + 144, cy), (RX - 2, cy)], col, mk, 1.4)
    d.t((CX + 144 + RX) // 2, cy - 10, "YES", 11, col, MONO, "middle", 600)

# 2. 시작 Oval
d.box(CX - 108, 104, 216, 40, PAPER2, RULE, 1.0, 20)
d.t(CX, 129, "새 소프트웨어 · 데이터", 13, INK, KR, "middle", 600)

# 3. 결정 다이아몬드 4개 (D1 focal — 외부 노출 데이터 우선 분리)
decisions = [
    "외부 노출 서비스 데이터?",
    "배포판 패키지 관리?",
    "관리자 로컬 직접 설치?",
    "의존성 포함 통짜 패키지?",
]
for i, (cy, txt) in enumerate(zip(DYS, decisions)):
    focal = (i == 0)
    fill = f"{ACC}12" if focal else PAPER2
    stroke = ACC if focal else MUTED
    sw = 1.4 if focal else 1.0
    d.o.append(f'<polygon points="{diamond_pts(CX, cy)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    d.t(CX, cy + 5, txt, 13, ACC if focal else INK, KR, "middle", 600)

# 4. 결과 상자 5개
results = [
    (DYS[0] - RH // 2, "/srv", "외부 노출 서비스 데이터 · 하위 구조 자유", OK),
    (DYS[1] - RH // 2, "/usr · /etc · /var/lib", "배포판 패키지 · 업그레이드 시 갱신", INFO),
    (DYS[2] - RH // 2, "/usr/local · /var/local", "로컬 직접 설치 · OS 업그레이드 보호", OK),
    (DYS[3] - RH // 2, "/opt/<pkg> · /etc/opt · /var/opt", "통짜 추가 패키지 · 정적·설정·가변 세 트리", WARN),
    (R5Y, "/var/lib/<app>", "비노출 내부 상태 · 실행 중 갱신", INFO),
]
for i, (ry, path_txt, sub_txt, col) in enumerate(results):
    h = 56 if i == 4 else RH
    d.tone(RX, ry, RW, h, col, r=6, op="12", sw=1.1)
    d.t(RX + 16, ry + 24, path_txt, 14, INK, MONO, "start", 600)
    d.t(RX + 16, ry + 46 if i == 4 else ry + 48, sub_txt, 13, MUTED, KR, "start")

d.legend(636, [("외부 노출 우선 분기", ACC), ("배포판 · 비노출 상태", INFO), ("로컬 · 외부 노출", OK), ("세 트리 분리", WARN)])
d.save("01-01.path-decision.svg")
