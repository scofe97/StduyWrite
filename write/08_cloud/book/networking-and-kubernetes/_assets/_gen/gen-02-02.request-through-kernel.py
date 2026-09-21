# 02-02.request-through-kernel — 가로 체인 + 커널 경계 (경계를 두 번 넘는다)
# 2026-09-20 수정: Conntrack 을 PRE_ROUTING 다음 칸으로 그려 두 단계가 순차인 것처럼 읽혔다.
#            실제로는 같은 훅에 등록된 콜백이다 — 커널 헤더 nf_ip_hook_priorities 기준
#            raw(-300) · conntrack(-200) · mangle(-150) · dstnat(-100) 이 모두 PRE_ROUTING 안에서
#            숫자 순으로 불린다. 본문 §1 의 우선순위 표와 어긋나 있었으므로, 훅 칸 안에 우선순위
#            순서를 적고 Conntrack 을 별도 칸에서 뺀다.
# 본문: "점선 안이 커널 공간. 왼쪽 두 칸은 그 밖(하드웨어와 유저 공간)이고,
#        패킷은 경계를 두 번 넘는다."
# 타입 스펙: type-process.md 의 단계 열 + type-nested.md 의 경계 링.
#           링을 가운데 다섯 칸에만 씌워 '두 번 넘는다'가 자리로 드러나게 한다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

# 2026-09-18 한 줄 일곱 칸을 두 줄로 접었다. 통로를 48px 로 벌리려면 일곱 칸에 288px 의 통로가
#            필요한데, 캔버스를 1000 에 두는 한(스타일 계약 §캔버스 폭 — 넓히면 본문에서 글자가
#            그만큼 작아진다) 칸에 남는 폭이 102px 이라 'Mangle·NAT·Filter' 같은 부제가 안 들어간다.
#            접으면 칸이 180px 로 오히려 넓어지고 통로도 48px 이 된다.
#            경계는 계단 모양 한 덩어리로 그린다 — 사각형 둘로 나누면 커널이 두 곳처럼 보이고,
#            접히는 화살표가 밖으로 나갔다 들어오는 꼴이 되어 '두 번 넘는다'가 깨진다.
W, H = 1000, 672
d = D(W, H, "ONE REQUEST · THROUGH THE KERNEL",
      "요청 하나가 커널을 관통하는 순서 — 네 절이 실제로 이어지는 자리",
      "점선 안이 커널 공간. 앞 두 칸은 PRE_ROUTING 훅 하나를 우선순위 순으로 펼친 것이고, Conntrack 은 그 훅에 등록된 콜백이지 뒤따르는 별도 단계가 아니다.",
      lead="앞 두 칸은 같은 훅의 앞뒤 자리 · 양 끝은 커널 밖")

OW, BW, BH, GAP = 88, 180, 104, 48                   # 커널 밖 카드는 좁게
IN_X = [258, 486, 714]                               # 커널 칸 세 열 — 168~348 · 396~576 · 624~804
ROW1, ROW2 = 300, 476                                # 줄 사이 통로 72px (접히는 화살표가 지난다)
OUT_L, OUT_R = 56, 668                               # 밖 카드 — 12~100 · 624~712
BX0, BY0, BY1 = 148, 212, 560                        # 경계 왼쪽·위·아래
BSTEP_X, BSTEP_Y, BX1 = 600, 392, 824                # 계단이 꺾이는 자리 (소켓 큐와 Go 서버 사이)
WRAP_Y = 372                                         # 접히는 화살표가 지나는 높이 (계단보다 위 = 커널 안)

ROW1_NODES = [("NIC 도착", "8080 행 SYN", "하드웨어", INFO, OW, OUT_L),
              ("PRE_ROUTING 앞자리", "raw · conntrack", "§1·§2 우선순위 -300·-200", None, BW, IN_X[0]),
              ("PRE_ROUTING 뒷자리", "mangle · DNAT", "§1 우선순위 -150·-100", None, BW, IN_X[1]),
              ("라우팅 판단", "바뀐 목적지로", "§3 로컬이냐 전달이냐", None, BW, IN_X[2])]
ROW2_NODES = [("LOCAL_IN", "mangle · filter", "§1 목적지가 나일 때", None, BW, IN_X[0]),
              ("소켓 큐", "포트로 소켓 선택", "02-01 §1 fd 로 전달", None, BW, IN_X[1]),
              ("Go 서버", "epoll 깨어남", "유저 공간", OK, OW, OUT_R)]

ddx.band(d, 104, 600, "네 절이 이어지는 자리 · 훅 · 연결 추적 · 라우팅 · 소켓", x=16, w=968)

# 계단 경계 — 모든 변이 직각이라 dd-lint 의 대각선 금지에 걸리지 않는다
d.o.append(f'<path d="M {BX0} {BY0} L {BX1} {BY0} L {BX1} {BSTEP_Y} L {BSTEP_X} {BSTEP_Y} '
           f'L {BSTEP_X} {BY1} L {BX0} {BY1} Z" fill="{ACC}0A" stroke="{ACC}" '
           f'stroke-width="1.4" stroke-dasharray="7 6"/>')
ddx.ring_label(d, BX0, BY0, "커널 공간", 11, ACC, off=20)

def card(cx, cy, l, s, t, c, w):
    d.box(cx - w // 2, cy - BH // 2, w, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 24, ddx.fit(l, 12, w - 14, l), 12, c or INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    d.t(cx, cy - 2, ddx.fit(s, 11, w - 12, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in s) else KR)
    d.t(cx, cy + 26, ddx.fit(t, 11, w - 10, t), 11, SOFT, KR)

for l, s, t, c, w, cx in ROW1_NODES: card(cx, ROW1, l, s, t, c, w)
for l, s, t, c, w, cx in ROW2_NODES: card(cx, ROW2, l, s, t, c, w)

def step(cy, a, aw, b, bw, lab, crossing=False):
    x1, x2 = a + aw // 2, b - bw // 2
    c = ACC if crossing else MUTED
    d.path(f"M {x1+6} {cy} L {x2-10} {cy}", c, 1.8 if crossing else 1.5,
           m="acc" if crossing else "ar")
    if lab: d.t((x1 + x2) // 2, cy - BH // 2 - 12, ddx.fit(lab, 11, GAP + 22, lab), 11, c, KR)

step(ROW1, OUT_L, OW, IN_X[0], BW, "", crossing=True)          # 경계를 넘는 첫 걸음
step(ROW1, IN_X[0], BW, IN_X[1], BW, "같은 훅 안")
step(ROW1, IN_X[1], BW, IN_X[2], BW, "훅 끝")
step(ROW2, IN_X[0], BW, IN_X[1], BW, "통과")
step(ROW2, IN_X[1], BW, OUT_R, OW, "", crossing=True)          # 경계를 넘는 두 번째 걸음

# 줄바꿈 — 계단보다 위(y=372)로 지나므로 커널 안에 머문다
d.path(f"M {IN_X[2]} {ROW1+BH//2+4} L {IN_X[2]} {WRAP_Y} L {IN_X[0]} {WRAP_Y} "
       f"L {IN_X[0]} {ROW2-BH//2-10}", MUTED, 1.5, m="ar")

d.t(OUT_L, ROW1 + BH // 2 + 24, "경계 진입", 12, ACC, KR)
d.t(OUT_R, ROW2 + BH // 2 + 24, "경계 이탈", 12, ACC, KR)
d.legend(616, [("커널 밖", INFO), ("도착", OK), ("경계를 넘는 걸음", ACC)])
d.save("02-02.request-through-kernel.svg")
print("ok request-through-kernel")
