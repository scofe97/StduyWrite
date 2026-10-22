# 타입 스펙: type-swimlane — 가로 레인 둘(--pid=host · 사이드카) × 단계 셋(공유되는 것 · 받는 컨테이너 · 얻는 능력). 같은 namespace 공유가 한 레인은 다른 컨테이너의 sleep 을 보고 kill -9 까지 하고, 한 레인은 필요한 namespace 만 받아 기능을 대신한다. focal 은 호스트 PID namespace 통째 공유 칸.
# 사실 출처: 노트 L224~L235(--pid=host · 컨테이너 sleep 과 alpine · ps | grep sleep · kill -9 <pid>), L239~L247(사이드카가 필요한 namespace 만 받음 · 서비스 메시 상호 TLS · 관측 로깅·추적·메트릭 · 보안 실행 파일·네트워크 연결 단속)
# Layout conventions: 레인 라벨 x=36 w156, 단계 열 x=204·476·700 w232·184·232, 머리 y=96 h=32, 레인1 y=140 h=148, 레인2 y=300 h=216, 셀 h=56 stride 68. 갈라지는 출구는 열 사이 x 의 직각 버스. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, PAPER2, KR, MONO

W, H = 984, 612


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "SWIMLANE · 09-01 §5",
      "namespace 공유는 같은 장치이고 범위와 의도가 위험인지 기능인지를 가릅니다",
      "두 레인 모두 컨테이너가 다른 쪽의 namespace 를 받는다. --pid=host 레인은 호스트 PID namespace 를 통째로 받아 sleep 1000 이 보이고 kill -9 로 종료할 수 있다. "
      "사이드카 레인은 앱 컨테이너의 필요한 namespace 만 받아 서비스 메시 · 관측 · 보안 기능을 대신한다.",
      lead="호스트 PID namespace 를 통째로 넘기면 kill 까지 가능하고, 사이드카는 필요한 namespace 만 받아 기능을 대신합니다.")

CX = [204, 476, 700]
CWS = [232, 184, 232]
CH = 56
LX, LW = 36, 156

for j, (num, name) in enumerate((("1", "공유되는 것"), ("2", "받는 컨테이너"), ("3", "얻는 능력"))):
    d.box(CX[j], 96, CWS[j], 32, PAPER2)
    d.t(CX[j] + 14, 117, num, 11, SOFT, MONO, "start")
    d.t(CX[j] + CWS[j] / 2 + 6, 117, name, 13, INK, KR, "middle", 600)

L1_Y, L1_H = 140, 148
L2_Y, L2_H = 300, 216
for y, h, name, sub, mono in ((L1_Y, L1_H, "--pid=host", "호스트 전체", True), (L2_Y, L2_H, "사이드카", "필요한 것만", False)):
    fit(name, 13, LW - 24)
    d.box(LX, y, LW, h)
    d.t(LX + 16, y + h / 2 - 2, name, 13, INK, MONO if mono else KR, "start", 600)
    d.t(LX + 16, y + h / 2 + 20, sub, 12, MUTED, KR, "start")


def cell(j, y, title, sub, c=None, tmono=False, smono=False, focal=False, h=CH):
    x, w = CX[j], CWS[j]
    ts = 12 if tmono else 13
    fit(title, ts, w - 20)
    fit(sub, 12, w - 20)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
    elif c:
        d.tone(x, y, w, h, c, 6, "14", 1.1)
    else:
        d.box(x, y, w, h)
    col = ACC if focal else (c or INK)
    d.t(x + w / 2, y + h / 2 - 3, title, ts, col, MONO if tmono else kr(title), "middle", 600)
    d.t(x + w / 2, y + h / 2 + 15, sub, 12, MUTED, MONO if smono else kr(sub), "middle")


def fan(y_src, ys, c, mk):
    """열 2 → 열 3 : 직각 버스. y_src 는 열 2 셀의 중심 y."""
    bus = 680
    d.line(CX[1] + CWS[1] + 2, y_src, bus, y_src, c, 1.3)
    d.line(bus, min(ys), bus, max(ys), c, 1.3)
    for y in ys:
        d.arrow([(bus, y), (CX[2] - 4, y)], c, mk, 1.3)


# 레인 1: --pid=host
a1, a2 = 152, 220
mid1 = L1_Y + L1_H / 2
cell(0, mid1 - CH / 2, "호스트 PID namespace", "통째로 공유", focal=True)
cell(1, mid1 - CH / 2, "alpine", "--pid=host", tmono=True, smono=True)
cell(2, a1, "다른 컨테이너의 sleep 1000", "ps | grep sleep", BAD, smono=True)
cell(2, a2, "sleep 프로세스 종료", "kill -9 <pid>", BAD, smono=True)
d.arrow([(CX[0] + CWS[0] + 2, mid1), (CX[1] - 4, mid1)], ACC, "acc", 1.4)
fan(mid1, [a1 + CH / 2, a2 + CH / 2], BAD, "bad")

# 레인 2: 사이드카
b = [312, 380, 448]
mid2 = L2_Y + L2_H / 2
cell(0, mid2 - CH / 2, "앱 컨테이너 namespace", "필요한 것만")
cell(1, mid2 - CH / 2, "사이드카", "의도한 공유")
cell(2, b[0], "서비스 메시", "네트워킹 · 상호 TLS", OK)
cell(2, b[1], "관측", "로깅 · 추적 · 메트릭", OK)
cell(2, b[2], "보안", "실행 파일 · 연결 단속", OK)
d.arrow([(CX[0] + CWS[0] + 2, mid2), (CX[1] - 4, mid2)], MUTED, "ar", 1.4)
fan(mid2, [y + CH / 2 for y in b], OK, "ok")

d.legend(H - 56, [("통째 공유", ACC), ("피해", BAD), ("기능", OK)])
d.save(str(ASSETS / "09-01.namespace-sharing.svg"))
print("ok 09-01 namespace-sharing")
