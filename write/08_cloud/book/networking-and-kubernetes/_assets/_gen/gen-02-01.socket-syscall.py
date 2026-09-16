# 02-01.socket-syscall — 한 줄 코드가 커널에 남기는 세 가지
# 본문 요구: "`net.Listen` 한 줄 뒤에서 커널은 소켓을 만들고 포트를 예약하고 대기 큐를 겁니다."
#            §1 의 세 증상(Address already in use · 접속 지연)이 각 syscall 이 남긴 객체에서 나온다.
#            02-03 도 같은 그림을 참조한다.
# 2026-09-15 이전 이 자리의 SVG 는 생성기가 없는 손 SVG 였다 — 코드 칸에서 세 칸으로 뻗는 방사형 사선,
#            한글 10px 서브라벨 15개, 하단 해설 문장이 계약 위반이었다. 사실은 그 SVG 와 본문에서만 가져왔다.
# 타입 스펙: type-tree — 부모(내 코드 한 줄) → 자식 셋(syscall) → 손자(커널 객체)의 부모-자식 관계다.
#           연결선은 줄기 → 버스 → 드롭의 직각. 깊이 4(뿌리 + 3단), 단당 폭 3.
#           coral 은 뿌리 한 곳(내가 쓰는 유일한 코드)에만 둔다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 552
d = D(W, H, "ONE LINE → THREE SYSCALLS → KERNEL OBJECTS",
      "한 줄 코드가 커널에 남기는 세 가지",
      "Go 의 net.Listen 한 줄은 런타임이 socket · bind · listen 세 syscall 로 커널에 넣는다. "
      "각 syscall 은 파일 디스크립터 · 포트 예약 · accept 큐를 남기고, 포트 중복과 큐 넘침이 실무 증상이 된다.",
      lead="내 코드 한 줄 → syscall 셋 → 커널 객체 셋 → 실무 증상")

CX = [212, 500, 788]                    # stride 288
NW = 240                                # 자식·손자 폭 (두 폭 규칙: 뿌리 360 · 나머지 240)
ROOT_Y, ROOT_H = 104, 52
BUS_Y = 188
T1_Y, T1_H = 208, 60
T2_Y, T2_H = 316, 64
T3_Y, T3_H = 420, 52

# ── 연결선 먼저 (스펙: Draw connectors before nodes) ─────────────
d.line(500, ROOT_Y + ROOT_H, 500, BUS_Y, MUTED, 1.0)
d.line(CX[0], BUS_Y, CX[2], BUS_Y, MUTED, 1.0)
for cx in CX:
    d.path(f"M {cx} {BUS_Y} L {cx} {T1_Y-8}", MUTED, 1.2, m="ar")
d.t(512, BUS_Y - 8, "Go 런타임이 대신 호출", 12, SOFT, KR, "start")

EFFECT = ["할당", "예약", "생성"]
for cx, lab in zip(CX, EFFECT):
    d.path(f"M {cx} {T1_Y+T1_H} L {cx} {T2_Y-8}", MUTED, 1.2, m="ar")
    d.t(cx + 10, T1_Y + T1_H + 28, lab, 12, SOFT, KR, "start")
for cx in CX[1:]:
    d.path(f"M {cx} {T2_Y+T2_H} L {cx} {T3_Y-8}", WARN, 1.2, m="warn", dash="4 4")

# ── 뿌리 — 내가 쓰는 코드는 이 한 줄뿐 ───────────────────────────
d.o.append(f'<rect x="320" y="{ROOT_Y}" width="360" height="{ROOT_H}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(500, ROOT_Y + 32, 'ln, _ := net.Listen("tcp", ":8080")', 13, ACC, MONO, "middle", 600)

# ── 1단 — syscall 셋 ─────────────────────────────────────────────
T1 = [("socket()", "AF_INET6 · SOCK_STREAM"),
      ("bind()", "htons(8080) · [::]"),
      ("listen()", "두 번째 인자 = 백로그")]
for cx, (name, sub) in zip(CX, T1):
    d.box(cx - NW // 2, T1_Y, NW, T1_H, PAPER2, INFO, 1.1, 6)
    d.t(cx, T1_Y + 24, name, 13, INFO, MONO, "middle", 600)
    d.t(cx, T1_Y + 46, ddx.fit(sub, 12, NW - 20, sub), 12, MUTED,
        MONO if all(ord(ch) < 128 or ch == '·' for ch in sub) else KR)

# ── 2단 — 커널 객체 셋 ───────────────────────────────────────────
T2 = [("파일 디스크립터 (fd)", "연결을 파일로 다루는 번호표", "0·1·2 다음 번호"),
      ("포트 8080 예약", "와일드카드 주소에 묶임", "v4·v6 함께 수신"),
      ("accept 큐", "수립됐지만 아직 안 받은 연결", "칸 수 = somaxconn")]
for cx, (name, sub, tag) in zip(CX, T2):
    d.box(cx - NW // 2, T2_Y, NW, T2_H, PAPER2, RULE, 1.1, 6)
    d.t(cx, T2_Y + 22, ddx.fit(name, 13, NW - 20, name), 13, INK, KR, "middle", 600)
    d.t(cx, T2_Y + 40, ddx.fit(sub, 12, NW - 20, sub), 12, MUTED, KR)
    d.t(cx, T2_Y + 56, ddx.fit(tag, 11, NW - 20, tag), 11, SOFT, KR)

# ── 3단 — 그 자리에서 터지는 실무 증상 (bind · listen 만) ──────────
T3 = [(CX[1], "중복 bind", "Address already in use"),
      (CX[2], "넘치면 조용한 drop", "거절 대신 접속 지연")]
for cx, head, body in T3:
    d.tone(cx - NW // 2, T3_Y, NW, T3_H, WARN, 6, "12", 1.1)
    d.t(cx, T3_Y + 21, head, 12, WARN, KR, "middle", 600)
    d.t(cx, T3_Y + 40, ddx.fit(body, 12, NW - 20, body), 12, INK,
        MONO if all(ord(ch) < 128 or ch == ' ' for ch in body) else KR)

d.legend(496, [("내 코드", ACC), ("syscall", INFO), ("실무 증상", WARN)])
d.save("02-01.socket-syscall.svg")
print("ok socket-syscall")
