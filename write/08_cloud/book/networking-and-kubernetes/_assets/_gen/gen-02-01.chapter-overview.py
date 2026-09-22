# 02-01.chapter-overview — 세로 체인 + 이 편의 경계
# 2026-09-21 옛 02-01 을 둘로 나누며 다시 그렸다. 그림은 커널이 맡는 네 갈래 전체를 그대로 두고,
#            이 편(소켓·배선) 두 칸만 점선으로 감싼다. 아래 두 칸은 02-02 의 번호를 달고 흐리게 둔다.
#            주제 배치도이지 시간순이 아니다 — 시간순은 02-02 §3 끝의 request-through-kernel 이 맡는다.
# 2026-09-21 2차 — 본문 §3 을 네임스페이스(§3)와 veth·브리지(§4)로 나눠 둘째 칸 이름과 번호를 바꿨다.
# 타입 스펙: type-layers.md — 위·아래가 의미를 갖는 축이므로 가로로 눕히지 않는다.
#           경계 링은 type-nested.md 관례. 링 밖 두 칸이 '이 편이 다루지 않는 곳'이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

# 2026-09-18 세로 간격 재배치 — 첫 화살표(애플리케이션 → 소켓)가 8px 뿐이라 '커널 공간' 점선
#            테두리와 겹쳐 화살촉만 테두리에 얹힌 꼴로 보였다. 단 사이 화살표도 stride 80 · BH 64 에
#            insets 를 빼면 2px 이었다. stride 를 96 으로 벌려 통로 32px 을 만들고, 링 위쪽에 여유를
#            둬 경계를 넘는 화살표가 테두리 위아래로 충분히 뻗게 한다.
# 2026-09-18 2차 — 통로 32px 도 여전히 답답하다는 지적. 잘 읽히는 같은 편 도식이 48~146px 이므로
#            stride 를 112 로 올려 통로를 48px 로 맞춘다. 가로 폭은 글자 크기를 정하므로 건드리지
#            않고(스타일 계약 §캔버스 폭), 늘어난 양만큼 캔버스 높이로 받는다.
W, H = 1000, 896
d = D(W, H, "02-01 · CHAPTER MAP",
      "커널이 패킷을 주고받는 자리 개념 지도 — 이 편은 점선 안을 다룬다",
      "위는 유저 공간, 아래는 물리 네트워크. 커널이 맡는 네 갈래 중 위 두 칸이 이 편이고 아래 두 칸은 02-02 다. 시간순이 아니라 주제 배치이며, 시간순은 02-02 3절 끝의 관통 도식이 맡는다.",
      lead="주제 배치도 · 패킷이 지나는 시간순이 아니다")

BX, BW, BH = 180, 640, 64
RING = (156, 232, 688, 224)                                    # 링 라벨 마스크가 첫 행에 닿지 않게 위로
APP_CY, NIC_CY = 180, 756
STEPS = [(296, "소켓 · fd", "앱과 커널의 분업", "§1 · §2", True),   # stride 112 — 통로 48px
         (408, "네임스페이스 · veth · 브리지", "격리와 배선", "§3 · §4", True),
         (520, "훅 · 연결 추적", "버릴지 고칠지", "02-02 §1 · §2", False),
         (632, "라우팅", "어디로 넘길지", "02-02 §3", False)]

def row(cy, label, sub, tag, c=None, h=BH, dash=False, muted=False):
    y = cy - h // 2
    d.o.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{h}" rx="6" fill="{PAPER2}" '
               f'stroke="{c or RULE}" stroke-width="1.1"{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(BX + 20, cy - 4, ddx.fit(label, 13, 300, label), 13, MUTED if muted else (c or INK), KR, "start", 600)
    d.t(BX + 20, cy + 16, ddx.fit(sub, 11, 340, sub), 11, MUTED, KR, "start")
    d.t(BX + BW - 20, cy + 4, tag, 11, SOFT, KR, "end")

ddx.band(d, 104, 824, "부르는 쪽과 물리 네트워크 사이 · 커널이 하는 일")

rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "이 편 — 소켓 · 격리 · 배선", 11, ACC)

row(APP_CY, "애플리케이션", "socket() 을 부른다", "유저 공간", INFO, 72, dash=True)
for cy, l, s, tag, mine in STEPS: row(cy, l, s, tag, muted=not mine)   # 다른 편 칸은 테두리는 그대로, 제목만 흐리게
row(NIC_CY, "NIC", "물리 네트워크로", "커널 밖", INFO, 72, dash=True)

# 2026-09-20 화살표를 선으로 바꿨다 — 화살표가 패킷의 시간 순서로 읽혀 veth 가 소켓과 훅 사이의
#            단계처럼 보였다. 이 그림은 주제 배치도이고 시간순은 request-through-kernel 이 맡는다.
d.path(f"M 500 {APP_CY+36+6} L 500 {STEPS[0][0]-BH//2-10}", RULE, 1.2)
for (a, *_), (b, *_) in zip(STEPS, STEPS[1:]):
    d.path(f"M 500 {a+BH//2+4} L 500 {b-BH//2-10}", RULE, 1.2)
d.path(f"M 500 {STEPS[-1][0]+BH//2+4} L 500 {NIC_CY-36-10}", RULE, 1.2)

d.legend(840, [("커널 밖", INFO), ("이 편의 범위", ACC), ("02-02 가 다룸", MUTED)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01.chapter-overview")
