# 타입 스펙: type-nested — 포함으로 드러나는 계층. 데이터그램 안에 데이터그램이 들어간다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.4.2 Figure 7.41 —
#   GTP 로 감싸 UDP 에 싣고 다시 IP 데이터그램으로 만든다는 순서는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 600
d = D(W, H, "SECTION 7.4.2 · GTP TUNNELING",
      "데이터그램을 데이터그램으로 감싸는 이유",
      "터널을 파면 백홀의 라우터들이 기기의 현재 위치를 몰라도 된다. 아는 것은 터널 양 끝뿐이다.",
      "감싸는 순서와 프로토콜 이름은 원문 Figure 7.41 의 것입니다")

LEVELS = [
    (24, 118, 496, 300, "바깥 IP 데이터그램", "출발지 UPF · 목적지 기지국", ACC),
    (56, 168, 432, 212, "UDP 세그먼트", "백홀 라우터가 보는 것은 여기까지", INFO),
    (88, 218, 368, 122, "GTP 헤더", "어느 기기의 터널인지 식별합니다", INFO),
    (120, 272, 304, 56, "원래 IP 데이터그램", "출발지 외부 호스트 · 목적지 무선 기기", OK),
]
for x, y, w, h, name, sub, c in LEVELS:
    d.tone(x, y, w, h, c, 8, "10", 1.3)
    d.t(x + 16, y + 24, name, 12, c, KR, "start", 600)
    d.t(x + 16, y + 42, sub, 10, MUTED, KR, "start")

PX, PW = 556, 348
d.box(PX, 118, PW, 300, PAPER2, RULE, 1.0)
d.t(PX + 20, 144, "터널이 없다면", 12, INK, KR, "start", 600)
d.line(PX + 20, 156, PX + PW - 20, 156, RULE, 0.8)
for i, ln in enumerate([
    "백홀 모든 라우터가 기기마다",
    "현재 기지국 정보를",
    "실시간 보유 (망 내 전 기기 대상)",
]):
    d.t(PX + 20, 180 + i * 20, ln, 11, MUTED, KR, "start")
d.t(PX + 20, 282, "터널이 있으면", 12, ACC, KR, "start", 600)
d.line(PX + 20, 294, PX + PW - 20, 294, RULE, 0.8)
for i, ln in enumerate([
    "터널 끝 UPF 만 기지국 인지",
    "백홀 라우터는 기지국까지의",
    "경로만 인지",
]):
    d.t(PX + 20, 318 + i * 20, ln, 11, ACC, KR, "start")

NY = 440
d.box(24, NY, 880, 80, PAPER2, RULE, 1.0)
d.t(44, NY + 26, "UPF = 기기 접속 동안의 고정점", 12, INK, KR, "start", 600)
d.t(44, NY + 50,
    "기지국 변경에도 터널 한쪽 끝은 UPF 고정 → 바깥에서 기기 위치 불변으로 관측",
    11, MUTED, KR, "start")
d.t(44, NY + 70,
    "세션 수립 시 SMF 가 기지국·UPF 사이 터널 생성",
    11, MUTED, KR, "start")

d.legend(548, [("터널 바깥", ACC), ("전달에 쓰이는 층", INFO), ("실제 사용자 데이터", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-04.gtp-tunnel.svg"
d.save(out)
print("→", out)
