# 04-01 §3 — 도청되는 선 위에서 양쪽이 같은 값을 갖는 구조.
# 본문 요구: 새 소절이 "각자 비밀값을 쥐고 공개값만 선에 흘린 뒤, 자기 비밀값과 상대 공개값으로
#            같은 결과를 계산한다. 엿보는 쪽은 공개값 둘만으로는 그 결과를 못 만든다" 를 말한다.
#            → 비밀값이 상자 안에 머물고 공개값만 선을 건너는 것이 그림의 전부여야 한다.
# 수치 출처: p=23, g=5, a=6, b=15 → A=8, B=19, 공유=2. python pow() 로 재계산해 확인했고
#            04-02 §1 이 이미 쓰는 같은 값이다(정본은 그쪽, 여기서는 그림 라벨로만 쓴다).
# 타입 스펙: type-swimlane — 레인 셋(클라이언트 · 선 = 도청자 · 서버)이고, 레인 경계를 넘는 것은
#           공개값 둘뿐이다. 비밀값 칸은 레인 안에 머물러 경계를 넘지 않는다. 스펙의 "handoffs
#           (arrows crossing lane boundaries) are the most important edges" 를 역으로 쓴다 —
#           무엇이 건너가지 *않는지*가 논지라, 건너가는 선을 둘로 제한해 대비를 만든다.
#           focal 은 양쪽 끝의 같은 공유 비밀(ACC)과 도청자 칸의 결손(BAD).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 960, 470
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §3",
      "공개값만 건너가고 비밀값은 남습니다",
      "양쪽이 각자 고른 비밀값은 자기 쪽에 머물고, 선을 건너는 것은 공개값 둘뿐이다. "
      "그 둘을 다 본 도청자도 양쪽이 계산해 낸 같은 값에는 도달하지 못한다.",
      "이 그림에서 볼 것은 선을 건너는 화살표가 둘뿐이라는 점입니다")

LX, RX, CW = 60, 660, 240          # 왼쪽·오른쪽 레인 칸
MIDX = (LX + CW + RX) / 2          # 선(도청자) 레인 중심
ROW = [150, 214, 278, 352]         # 비밀 · 공개 · 계산 · 공유

# ── 레인 머리
d.t(LX, 120, "CLIENT", 9, MUTED, MONO, "start", 600)
d.t(RX, 120, "SERVER", 9, MUTED, MONO, "start", 600)
d.t(MIDX, 120, "WIRE", 9, MUTED, MONO, "middle", 600)

# ── 선 레인 경계 — 공개값만 이 통로를 지난다
for x in (LX + CW + 20, RX - 20):
    d.line(x, 132, x, 400, RULE, 0.8, "4,4")

# ── 1단: 비밀값 — 레인 안에 머문다
for x, lab, val in ((LX, "비밀값 a", "6"), (RX, "비밀값 b", "15")):
    y = ROW[0]
    d.tone(x, y, CW, 40, WARN, 4, "18")
    d.t(x + 14, y + 25, lab, 12, INK, MONO, "start", 600)
    d.t(x + CW - 14, y + 25, val, 12, WARN, MONO, "end", 600)
d.t(MIDX, ROW[0] + 25, "건너가지 않음", 11, MUTED, KR)

# ── 2단: 공개값 — 선을 건넌다
for x, lab, val in ((LX, "공개값 A", "8"), (RX, "공개값 B", "19")):
    y = ROW[1]
    d.tone(x, y, CW, 40, INFO, 4, "18")
    d.t(x + 14, y + 25, lab, 12, INK, MONO, "start", 600)
    d.t(x + CW - 14, y + 25, val, 12, INFO, MONO, "end", 600)
# 두 화살표가 통로를 가로지른다 — 서로 다른 높이로 두어 겹치지 않게
d.arrow([(LX + CW + 8, ROW[1] + 14), (RX - 8, ROW[1] + 14)], INFO, "ar", 1.4)
d.arrow([(RX - 8, ROW[1] + 30), (LX + CW + 8, ROW[1] + 30)], INFO, "ar", 1.4)

# ── 3단: 계산 — 자기 비밀값 + 상대 공개값
for x, expr in ((LX, "B^a mod p"), (RX, "A^b mod p")):
    y = ROW[2]
    d.box(x, y, CW, 40)
    d.t(x + CW / 2, y + 25, expr, 12, SOFT, MONO)
d.t(MIDX, ROW[2] + 25, "공개값 둘만 봄", 11, BAD, KR, "middle", 600)

# ── 4단: 공유 비밀 — 양쪽이 같은 값에 도달 (focal)
for x in (LX, RX):
    y = ROW[3]
    d.tone(x, y, CW, 44, ACC, 4, "22", 1.6)
    d.t(x + 14, y + 27, "공유 비밀", 12, INK, KR, "start", 600)
    d.t(x + CW - 14, y + 27, "2", 14, ACC, MONO, "end", 600)

# 도청자 칸 — 같은 자리에 값이 없다
y = ROW[3]
d.o.append(f'<rect x="{LX + CW + 34}" y="{y}" width="{RX - LX - CW - 68}" height="44" rx="4" '
           f'fill="none" stroke="{BAD}" stroke-width="1.4" stroke-dasharray="4,3"/>')
d.t(MIDX, y + 27, "5^x mod p = 8 의 x 를 찾아야 함", 11, BAD, KR)

d.t(LX, 424, "선을 지나간 값 · p · g · 8 · 19", 12, MUTED, KR, "start")

d.legend(H - 26, [("레인 안에 머무는 비밀값", WARN), ("선을 건너는 공개값", INFO),
                  ("양쪽이 도달한 같은 값", ACC), ("도청자에게 남는 것", BAD)])
d.save("04-01.key-exchange-idea.svg")
