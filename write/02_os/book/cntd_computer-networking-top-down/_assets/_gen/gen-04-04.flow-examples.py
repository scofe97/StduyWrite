# 타입 스펙: type-architecture — 예제 망의 물리 구조와 포트 번호. 표가 고르는 길을 그 위에 얹는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.4.3 Figure 4.30 의 포트 번호와 주소 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, KR, MONO

W, H = 1000, 620
d = D(W, H, "FIGURE 4.30 · MATCH-PLUS-ACTION NETWORK",
      "표가 고르면 길이 바뀝니다",
      "패킷 스위치 셋과 호스트 여섯으로 이루어진 예제 망. 첫째 예의 흐름 표는 s3 과 s2 를 잇는 직통 링크를 일부러 비우고 s1 을 거쳐 가게 만든다.",
      "주황 경로가 첫째 예입니다 — h5·h6 에서 h3·h4 로, s3 에서 s1 을 거쳐 s2 로")


def box(x, y, w, h, name, sub, kind="host"):
    c = {"host": MUTED, "sw": INK}[kind]
    d.box(x, y, w, h, PAPER2, f"{c}66", 1.0, 7)
    d.t(x + w / 2, y + 24, name, 12, INK, MONO, "middle", 600)
    d.t(x + w / 2, y + 41, sub, 11, MUTED, KR)


box(200, 206, 100, 56, "s3", "10.3.*.*", "sw")
box(700, 206, 100, 56, "s2", "10.2.*.*", "sw")
box(450, 346, 100, 56, "s1", "10.1.*.*", "sw")
box(40, 150, 120, 52, "h6", "10.3.0.6")
box(40, 254, 120, 52, "h5", "10.3.0.5")
box(840, 150, 120, 52, "h4", "10.2.0.4")
box(840, 254, 120, 52, "h3", "10.2.0.3")
box(280, 470, 120, 52, "h1", "10.1.0.1")
box(600, 470, 120, 52, "h2", "10.1.0.2")

# 호스트 링크 — 스위치의 어느 포트에 붙는지가 보이도록 직각으로
d.path("M 160 176 L 178 176 L 178 220 L 196 220", MUTED, 1.2)
d.path("M 160 280 L 178 280 L 178 248 L 196 248", MUTED, 1.2)
d.path("M 840 176 L 822 176 L 822 220 L 804 220", MUTED, 1.2)
d.path("M 840 280 L 822 280 L 822 248 L 804 248", MUTED, 1.2)
d.path("M 340 470 L 340 440 L 476 440 L 476 406", MUTED, 1.2)
d.path("M 660 470 L 660 440 L 524 440 L 524 406", MUTED, 1.2)

# 첫째 예가 쓰는 두 구간
d.arrow([(288, 288), (288, 374), (438, 374)], ACC, "acc", 2.0)
d.arrow([(562, 374), (712, 374), (712, 290)], ACC, "acc", 2.0)
# 일부러 비워 두는 직통 링크
d.path("M 320 226 L 680 226", BAD, 1.4, dash="6 5")


def port(x, y, n, c=SOFT):
    d.o.append(f'<rect x="{x - 9}" y="{y - 9}" width="18" height="18" rx="3" '
               f'fill="{PAPER}" stroke="{c}" stroke-width="0.9"/>')
    d.t(x, y + 4, str(n), 10, c, MONO)


# 포트 번호는 Figure 4.30 그대로 — s3: 1=h6 2=h5 3=s1 4=s2
port(188, 220, 1); port(188, 248, 2); port(288, 274, 3, ACC); port(312, 226, 4, BAD)
# s2: 1=s3 2=s1 3=h3 4=h4
port(688, 226, 1, BAD); port(712, 274, 2, ACC); port(812, 248, 3); port(812, 220, 4)
# s1: 1=s3 2=h1 3=h2 4=s2
port(442, 374, 1, ACC); port(476, 414, 2); port(524, 414, 3); port(558, 374, 4, ACC)

d.t(500, 250, "직통 링크를 비워 둡니다", 11, BAD, KR)
d.t(500, 330, "표를 계산해 설치하는 것은 원격 컨트롤러입니다", 11, SOFT, KR)

d.t(40, 548, "둘째 예는 같은 그림에서 s2 의 표만 바꿔, 들어온 포트 3 과 4 를 서로 다른 링크로 갈라 보냅니다. "
              "목적지가 같으므로 목적지만 보는 규칙으로는 만들 수 없는 동작입니다.", 11, MUTED, KR, "start")

d.legend(566, [("첫째 예가 쓰는 경로", ACC), ("일부러 쓰지 않는 링크", BAD), ("링크와 포트", MUTED)])
d.t(960, 588, "KUROSE-ROSS 9E FIG 4.30", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-04.flow-examples.svg"
d.save(out)
print("→", out)
