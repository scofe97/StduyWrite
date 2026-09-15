# 04-01 §3 — 원문이 4장 내내 쓰는 회전교차로 비유. 진입로·진입소 = 입력 포트, 회전교차로 = 스위칭 패브릭,
# 나가는 램프 = 출력 포트. 원문이 던지는 물음 넷 중 앞의 셋이 다음 편의 큐잉이고 넷째가 이 편 §6 으로 간다.
# 2026-09-14 신설: 비유를 산문으로만 적어 두면 대응이 눈에 안 들어온다는 지적을 받아, 비유·대응·막히는 자리를
#   같은 자리에 세 칸으로 반복해 도식이 산문을 대신하게 했다.
# 타입 스펙: type-process — 단계마다 같은 슬롯(비유 · 라우터의 무엇 · 여기서 막히면)이 반복된다.
#   축약: 회전교차로를 원이 아니라 사각 고리로 그린다. 대각선 연결선이 금지라 원형은 방향이 사라진다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 668
CX = [24, 348, 672]
CW, CH = 304, 378

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §3",
      "회전교차로로 읽는 라우터",
      "원문의 운전 비유. 차가 진입소에서 목적지를 말하면 안내원이 나갈 램프를 알려 준다. "
      "이 비유가 좋은 이유는 병목이 생길 자리를 묻게 만들기 때문이다.",
      "세 칸이 각각 라우터의 한 부품이고, 각각 다른 데서 밀립니다")

CARDS = [
    ("1", "진입로와 진입소", "차가 서고 안내원이 답함",
     "목적지를 말하면 나갈 램프를 알려 줌",
     "입력 포트", "안내원이 느리면",
     "차가 아무리 빨리 들어와도", "진입소 앞에서 밀림", "→ 다음 편 · 입력 큐", WARN),
    ("2", "회전교차로", "모두가 여기를 지남",
     "안에서 돌다가 자기 출구로 빠짐",
     "스위칭 패브릭", "고리 안이 느리면",
     "안내원이 아무리 빨라도", "건너지 못해 밀림", "→ 다음 편 · 패브릭 속도", WARN),
    ("3", "나가는 램프", "출구는 방향마다 하나",
     "세 방향의 차가 한 램프로 몰림",
     "출력 포트", "같은 출구로 몰리면",
     "한 대만 나가고 나머지는", "램프 앞에 줄을 섬", "→ 다음 편 · 출력 큐", ACC),
]

for x0, (num, title, sub, cap, part, q, e1, e2, dest, c) in zip(CX, CARDS):
    d.box(x0, 110, CW, CH, PAPER2, RULE, 0.9, 8)
    d.t(x0 + 20, 132, num, 11, SOFT, MONO, "start")
    d.t(x0 + CW / 2, 152, title, 14, INK, KR, "middle", 600)
    d.t(x0 + CW / 2, 172, sub, 12, SOFT, KR)
    d.t(x0 + CW / 2, 288, cap, 12, MUTED, KR)
    d.line(x0 + 16, 316, x0 + CW - 16, 316, RULE, 0.8)
    d.t(x0 + CW / 2, 338, "라우터에서는", 12, SOFT, KR)
    d.t(x0 + CW / 2, 358, part, 13, INK, KR, "middle", 600)
    d.tone(x0 + 16, 372, CW - 32, 100, c, 6, "12", 1.3)
    d.t(x0 + CW / 2, 398, q, 13, c, KR, "middle", 600)
    d.t(x0 + CW / 2, 420, e1, 12, MUTED, KR)
    d.t(x0 + CW / 2, 440, e2, 12, MUTED, KR)
    d.t(x0 + CW / 2, 462, dest, 12, SOFT, KR)

# 1 — 차가 줄을 서고 진입소가 답한다
for i in range(3):
    d.o.append(f'<rect x="{48 + i * 48}" y="200" width="40" height="24" rx="4" '
               f'fill="{MUTED}22" stroke="{MUTED}" stroke-width="1.1"/>')
d.path("M 192 212 L 212 212", MUTED, 1.2, m="ar")
d.box(216, 190, 88, 44, PAPER, WARN, 1.2, 6)
d.t(260, 208, "진입소", 12, WARN, KR, "middle", 600)
d.t(260, 226, "안내원", 12, SOFT, KR)

d.path("M 330 222 L 344 222", MUTED, 1.2, m="ar")

# 2 — 사각 고리 안에서 돌다가 자기 출구로 빠진다
d.o.append(f'<rect x="396" y="186" width="160" height="72" rx="10" fill="none" '
           f'stroke="{WARN}" stroke-width="1.6"/>')
d.o.append(f'<rect x="416" y="200" width="36" height="22" rx="4" '
           f'fill="{MUTED}22" stroke="{MUTED}" stroke-width="1.1"/>')
d.o.append(f'<rect x="502" y="222" width="36" height="22" rx="4" '
           f'fill="{MUTED}22" stroke="{MUTED}" stroke-width="1.1"/>')
d.path("M 368 222 L 392 222", MUTED, 1.2, m="ar")
d.path("M 560 222 L 584 222", MUTED, 1.2, m="ar")

d.path("M 654 222 L 668 222", MUTED, 1.2, m="ar")

# 3 — 세 방향이 한 램프로 모인다
for i in range(3):
    y = 184 + i * 32
    d.o.append(f'<rect x="696" y="{y}" width="36" height="24" rx="4" '
               f'fill="{MUTED}22" stroke="{MUTED}" stroke-width="1.1"/>')
    d.line(732, y + 12, 800, y + 12, MUTED, 1.0)
d.line(800, 196, 800, 260, MUTED, 1.0)
d.path("M 800 228 L 816 228", ACC, 1.3, m="acc")
d.box(820, 212, 64, 32, PAPER, ACC, 1.3, 5)
d.t(852, 232, "램프", 12, ACC, KR)

# 네 번째 물음은 성격이 다르다
d.tone(24, 512, 928, 66, INFO, 8, "0A", 1.2)
d.t(48, 538, "네 번째 물음은 줄 이야기가 아님", 13, INFO, KR, "start", 600)
d.t(48, 560, "차마다 우선순위 · 특정 차 진입 차단 → 무엇을 보고 무엇을 할지 (이 편 §6 일치 후 동작)",
    13, MUTED, KR, "start")

d.legend(H - 44, [("다음 편이 이어받는 자리", ACC), ("여기서 밀림", WARN), ("이 편 §6 으로", INFO)])
d.save("04-01.roundabout.svg")
print("ok roundabout")
