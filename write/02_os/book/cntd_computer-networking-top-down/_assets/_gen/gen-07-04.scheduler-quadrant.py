# 타입 스펙: type-quadrant — 두 축 위의 위치. 스케줄러 넷이 채널 인지와 공평성 두 축에서 갈린다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.5 Figure 7.37 과 각 알고리즘 서술 —
#   RR·MT·BET·PF 의 채널 인지 여부와 공평성 판정은 원문의 서술 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 940, 616
d = D(W, H, "SECTION 7.3.5 · MAC SCHEDULING",
      "채널이 좋은 기기를 밀어줄 것인가, 고르게 나눌 것인가",
      "무선에서는 누구에게 보내느냐가 총 처리량을 바꾼다. 그래서 스케줄러 선택이 곧 성능 정책이다.",
      "네 알고리즘의 성격 판정은 원문 §7.3.5 의 서술입니다")

X0, X1, Y0, Y1 = 130, 570, 452, 122
d.line(X0, Y1 - 12, X0, Y0, RULE, 1.0)
d.line(X0, Y0, X1 + 12, Y0, RULE, 1.0)
d.line(X0, (Y0 + Y1) / 2, X1, (Y0 + Y1) / 2, RULE, 0.8, "4 6")
d.line((X0 + X1) / 2, Y0, (X0 + X1) / 2, Y1, RULE, 0.8, "4 6")
d.t((X0 + X1) / 2, Y0 + 26, "채널 상태를 보는 정도", 11, MUTED, KR)
d.t(X0 - 10, Y0 + 4, "낮음", 10, SOFT, KR, "end")
d.t(X1, Y0 + 4, "", 10, SOFT, KR)
d.t(X0 - 96, (Y0 + Y1) / 2 - 8, "처리량 공평성", 11, MUTED, KR, "start")
d.t(X0 - 96, (Y0 + Y1) / 2 + 12, "위쪽이 더 고름", 10, SOFT, KR, "start")

POINTS = [
    ("RR", 0.14, 0.42, INFO, "순번은 고르지만"),
    ("MT", 0.88, 0.17, BAD, "총량 최대, 공평 없음"),
    ("BET", 0.46, 0.90, OK, "처리량을 고르게"),
    ("PF", 0.86, 0.72, ACC, "둘 사이의 균형"),
]
for name, fx, fy, c, note in POINTS:
    x = X0 + (X1 - X0) * fx
    y = Y0 + (Y1 - Y0) * fy
    d.o.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}44" stroke="{c}" stroke-width="1.6"/>')
    d.t(x, y - 24, name, 13, c, MONO, "middle", 600)
    d.t(x, y + 28, note, 10, MUTED, KR)

PX, PW = 620, 284
d.box(PX, 122, PW, 330, PAPER2, RULE, 1.0)
d.t(PX + 20, 148, "무엇을 최대로 만드는가", 12, INK, KR, "start", 600)
d.line(PX + 20, 160, PX + PW - 20, 160, RULE, 0.8)
ROWS = [
    ("RR", INFO, ["기기마다 같은 수의 자원 블록", "채널도 QoS 도 안 봅니다"]),
    ("MT", BAD, ["보고된 채널 품질이 가장 좋은 기기", "한 기기가 다 가져갈 수 있습니다"]),
    ("BET", OK, ["평균 처리량이 가장 낮은 기기", "지수 가중 이동 평균을 씁니다"]),
    ("PF", ACC, ["기대 처리량을 평균 처리량으로 나눈 값", "높은 쪽에 자원 블록을 줍니다"]),
]
ry = 184
for name, c, lines in ROWS:
    d.t(PX + 20, ry, name, 11, c, MONO, "start", 600)
    for j, ln in enumerate(lines):
        d.t(PX + 20, ry + 20 + j * 18, ln, 10, MUTED, KR, "start")
    ry += 66

NY = 500
d.box(24, NY, 880, 62, PAPER2, RULE, 1.0)
d.t(44, NY + 24, "표준은 스케줄링 알고리즘을 정하지 않습니다", 12, INK, KR, "start", 600)
d.t(44, NY + 46,
    "3GPP 도 WiFi 표준도 이것을 규정하지 않아서, 사업자와 장비 회사가 서로를 가르는 비법으로 씁니다.",
    11, MUTED, KR, "start")

d.legend(576, [("채널 무관", INFO), ("총량 우선", BAD), ("공평 우선", OK), ("균형", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-04.scheduler-quadrant.svg"
d.save(out)
print("→", out)
