# 타입 스펙: type-data-flow — 레인 둘(함수 호출 · 인라인) × 단계 넷. 명령어 흐름 두 줄을 같은 열에 세워 본문 벌 수를 비교한다.
# 사실 출처: 추출본 ebpf2.txt 680~728행 — static __always_inline void my_function(void *ctx, int val);
#   호출 지점마다 jump 로 한 벌의 본문에 갔다 돌아오는 방식과, 호출 지점마다 본문을 복사하는 인라인 방식.
# Layout formulas(type-data-flow §2) 변형: 레인 2 · lane_h 112 · node 168×64 · 단계 간격 36.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 448
d = D(W, H, "LEARNING EBPF · 02-02 §3",
      "인라인이면 호출 지점마다 본문이 한 벌씩 붙는다",
      "인라인이 아니면 두 호출 지점이 jump 로 같은 본문 한 벌에 갔다 돌아오고, __always_inline 이면 호출 지점마다 본문이 복사된다.",
      "같은 my_function 을 두 곳에서 호출할 때")

NX = [148, 352, 556, 760]
NW, NH = 168, 64
HEAD = ["01 호출 1", "02 호출 2", "03 본문", "04 복귀"]
for i, x in enumerate(NX):
    d.box(x + NW/2 - 44, 100, 88, 20, PAPER2, RULE, 0.9, 10)
    d.t(x + NW/2, 114, HEAD[i], 12, MUTED, KR, "middle", 600)

LT0, LT1, LH = 140, 252, 112
for top, name, sub, shade in ((LT0, "함수 호출", "jump · return", True), (LT1, "인라인", "__always_inline", False)):
    if shade:
        d.o.append(f'<rect x="12" y="{top}" width="{W-24}" height="{LH}" fill="#F5F5F3" fill-opacity="0.025"/>')
    d.t(24, top + LH/2 - 2, name, 14, INK, KR, "start", 600)
    d.t(24, top + LH/2 + 16, sub, 12, MUTED, MONO, "start")

def node(x, y, title, sub, c, mono_sub=True):
    d.tone(x, y, NW, NH, c, 6, "12", 1.2)
    d.t(x + NW/2, y + 28, title, 13, c, KR if any("가" <= ch <= "힣" for ch in title) else MONO, "middle", 600)
    d.t(x + NW/2, y + 48, sub, 12, MUTED, MONO if mono_sub else KR)

Y0 = LT0 + 28
Y1 = LT1 + 24
# 줄 1 — 함수 호출
node(NX[0], Y0, "호출 지점 1", "jump → my_function", INFO)
node(NX[1], Y0, "호출 지점 2", "jump → my_function", INFO)
node(NX[2], Y0, "my_function", "본문 1벌", WARN)
node(NX[3], Y0, "return", "호출 지점 다음 줄", OK, False)
yc0 = Y0 + NH // 2
d.arrow([(NX[1] + NW + 2, yc0), (NX[2] - 6, yc0)], WARN, "warn", 1.6)
d.arrow([(NX[2] + NW + 2, yc0), (NX[3] - 6, yc0)], OK, "ok", 1.5)
# 호출 지점 1 → 본문: 위로 돌아 들어간다
cx0, cx2 = NX[0] + NW // 2, NX[2] + NW // 2
d.arrow([(cx0, Y0 - 2), (cx0, LT0 + 8), (cx2, LT0 + 8), (cx2, Y0 - 6)], WARN, "warn", 1.6)
# 줄 2 — 인라인
node(NX[0], Y1, "호출 지점 1", "본문 복사 1", WARN, False)
node(NX[1], Y1, "호출 지점 2", "본문 복사 2", WARN, False)
d.t(NX[2] + NW/2, Y1 + 32, "jump 없음", 12, SOFT, KR)
d.t(NX[3] + NW/2, Y1 + 32, "return 없음", 12, SOFT, KR)

d.legend(H - 56, [("호출 지점", INFO), ("함수 본문", WARN), ("복귀", OK)])
d.save("02-02.call-inline.svg")
