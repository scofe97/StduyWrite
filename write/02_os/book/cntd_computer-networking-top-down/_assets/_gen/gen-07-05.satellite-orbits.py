# 타입 스펙: type-deployment — 소프트웨어가 어디서 도는가. 여기서는 무엇이 어느 고도에 놓이는가.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.6.2 Figure 7.49 · Figure 7.50 —
#   고도 35,000 km 와 500~1,200 km, RTT ~800 msec 와 ~30 msec, 27,000 km/hr 는 원문 수치 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 940, 620
d = D(W, H, "SECTION 7.6.2 · GEO AND LEO SATELLITES",
      "움직이는 쪽이 기기가 아니라 인프라입니다",
      "지구 정지 궤도는 하늘에 붙박여 있고 저궤도는 쉬지 않고 지나간다. 그래서 저궤도에서는 핸드오버가 일상이다.",
      "고도와 왕복 지연은 원문 §7.6.2 의 값입니다")

BANDS = [
    (128, "지구 정지 궤도 (GEO)", "약 35,000 km", "왕복 지연 약 800 ms · 하늘에 고정", ACC),
    (216, "저궤도 (LEO)", "500 에서 1,200 km", "왕복 지연 약 30 ms · 초속 7.5 km 로 지나감", OK),
    (304, "지상", "지상국과 사용자 단말", "게이트웨이가 지상 인터넷과 잇습니다", INFO),
]
for y, name, alt, note, c in BANDS:
    d.tone(24, y, 512, 72, c, 6, "12", 1.2)
    d.t(44, y + 28, name, 12, c, KR, "start", 600)
    d.t(44, y + 50, note, 10, MUTED, KR, "start")
    d.t(516, y + 34, alt, 11, c, MONO, "end", 600)

d.t(24, 400, "60 년 넘게 방송과 관측과 오지 인터넷에 쓰인 것이 GEO 입니다. 최근 10 년의 변화는 LEO 쪽입니다.",
    11, MUTED, KR, "start")
d.t(24, 422, "2022 년 11 월까지 역사상 활동 위성이 6,800 기였는데, 스타링크 혼자 5 년 동안 6,281 기를 올렸습니다.",
    11, MUTED, KR, "start")

PX, PW = 572, 332
d.box(PX, 128, PW, 248, PAPER2, RULE, 1.0)
d.t(PX + 20, 154, "하늘에 링크인가, 하늘에 망인가", 12, INK, KR, "start", 600)
d.line(PX + 20, 166, PX + PW - 20, 166, RULE, 0.8)
MODES = [
    ("굽은 파이프", INK, ["위성 하나를 링크 하나로 봅니다.", "홉마다 지상으로 내려옵니다."]),
    ("하늘의 망", INK, ["위성끼리 광 링크로 잇습니다.", "여러 홉을 하늘에서 지납니다.", "서로 움직여 라우팅이 어렵습니다."]),
]
my = 190
for name, c, lines in MODES:
    d.t(PX + 20, my, name, 11, c, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(PX + 20, my + 20 + j * 18, "·  " + ln, 10, MUTED, KR, "start")
    my += 20 + len(lines) * 18 + 18

WY = 452
d.tone(24, WY, 880, 90, WARN, 8, "10", 1.3)
d.t(44, WY + 26, "원문 정오 — 세 수치가 서로 안 맞습니다", 12, WARN, KR, "start", 600)
for i, ln in enumerate([
    "위성 속도 27,000 km/hr = 초속 7.5 km · 풋프린트 지름 15 마일 = 24 km · 체류 시간 10 분",
    "24 km 를 초속 7.5 km 로 지나면 3.2 초입니다. 10 분 체류라면 지름이 약 4,500 km 여야 합니다.",
]):
    d.t(44, WY + 50 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(562, [("지구 정지 궤도", ACC), ("저궤도", OK), ("지상", INFO), ("맞지 않는 수치", WARN)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-05.satellite-orbits.svg"
d.save(out)
print("→", out)
