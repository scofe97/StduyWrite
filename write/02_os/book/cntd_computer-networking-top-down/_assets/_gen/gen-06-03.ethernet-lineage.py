# 타입 스펙: type-timeline — 시간 축 위의 사건. 세대가 바꾼 것과 끝내 안 바뀐 것을 한 축에 놓는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.2 와 Case History: Bob Metcalfe and Ethernet.
#   원문이 십년 단위로만 적은 시기는 그 표현을 그대로 옮기고 연도를 지어내지 않는다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 496
d = D(W, H, "SECTION 6.4.2 · FIFTY YEARS OF ETHERNET",
      "토폴로지는 세 번 바뀌고 프레임 형식은 그대로입니다",
      "동축 버스에서 허브 성형으로, 다시 스위치 성형으로 옮겨 가는 동안 속도는 세 자릿수로 올랐다. 그 사이 프레임 형식만 바뀌지 않았다.",
      "원문이 십년 단위로 적은 시기는 그대로 옮겼습니다")

AX, AW, AY = 40, 920, 268
d.line(AX, AY, AX + AW, AY, RULE, 1.4)

EVENTS = [
    (0.06, "1970년대 중반", ["Metcalfe·Boggs 가", "2.94 Mbps 로 시작"], INFO, True),
    (0.20, "1980년대 ~ 1990년대 중반", ["동축 버스 토폴로지", "CSMA/CD 가 필요합니다"], MUTED, False),
    (0.44, "1990년대 후반", ["허브 기반 성형", "여전히 브로드캐스트 LAN"], MUTED, True),
    (0.63, "2000년대 초", ["허브를 스위치로 교체", "충돌이 사라집니다"], OK, False),
    (0.80, "2000년대 중반", ["기가비트 표준", "MAC·프레임 형식 유지"], OK, True),
    (0.94, "오늘", ["10 · 40 · 100", "200 · 400 Gbps"], ACC, False),
]
for pos, when, lines, c, above in EVENTS:
    x = AX + AW * pos
    d.o.append(f'<circle cx="{x}" cy="{AY}" r="5" fill="{PAPER}" stroke="{c}" stroke-width="2"/>')
    if above:
        d.line(x, AY - 8, x, AY - 40, RULE, 0.9, "3 4")
        d.t(x, AY - 52, when, 11, c, KR, "middle", 600)
        for j, s in enumerate(lines):
            d.t(x, AY - 96 + j * 18, s, 11, MUTED, KR)
    else:
        d.line(x, AY + 8, x, AY + 40, RULE, 0.9, "3 4")
        d.t(x, AY + 56, when, 11, c, KR, "middle", 600)
        for j, s in enumerate(lines):
            d.t(x, AY + 76 + j * 18, s, 11, MUTED, KR)

d.tone(AX, 116, AW, 40, ACC, 6, "14", 1.4)
d.t(AX + AW / 2, 141, "거의 50 년 동안 바뀌지 않은 하나 — 이더넷 프레임 형식", 12, ACC, KR, "middle", 600)

d.line(24, 380, W - 48, 380, RULE, 0.8)
d.t(24, 402, "속도는 세 자릿수로 올랐고 매체는 동축에서 구리와 광으로 갈렸으며 토폴로지는 버스에서 스위치로 옮겼습니다.",
     11, MUTED, KR, "start")
d.t(24, 420, "스위치 기반 LAN 에는 충돌이 없어 MAC 프로토콜조차 필요하지 않습니다. 그래도 이것은 여전히 이더넷입니다.",
     11, MUTED, KR, "start")

d.legend(438, [("바뀌지 않은 것", ACC), ("시작", INFO), ("충돌이 사라진 뒤", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-03.ethernet-lineage.svg"
d.save(out)
print("→", out)
