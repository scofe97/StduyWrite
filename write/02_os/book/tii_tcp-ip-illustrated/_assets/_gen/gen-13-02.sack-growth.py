# 13-02 §3 — 수신자가 돌려보낸 ACK 여섯 개에서 SACK 블록이 하나씩 늘고, 구멍이 메워지면 앞쪽 블록이 빠지는 모습.
# 값 출처: OrbStack Ubuntu(커널 7.0.14) 네트워크 네임스페이스 둘, 수신 쪽 약 4% 손실 링크로 400KB 전송한 캡처(2026-10-04).
#   순서 번호는 tcpdump 상대값. 블록 {L:R} 은 L 부터 R − 1 까지(RFC 2018 의 오른쪽 경계 = 다음 바이트).
#   ack 21721 sack 1 {23169:24617} (IP 64) → sack 1 {23169:28961} → sack 2 {30409:31857}{23169:28961} (IP 72)
#   → sack 2 {30409:46337}{23169:28961} → sack 3 {47785:55025}{30409:46337}{23169:28961} (IP 80)
#   → ack 28961 sack 2 {47785:55025}{30409:46337}.
#   첫 블록 = 이 ACK 를 일으킨 세그먼트를 담은 블록(RFC 2018 §4) — 막대 안 숫자가 옵션 안의 순서다.
#   구멍(점선)은 ACK 번호와 가장 오른쪽 블록 사이에서 어느 블록에도 들지 않은 범위다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 축 + 행마다 막대, 막대 길이 = 구간. 가로 축은 시간이 아니라 바이트 번호이고
#           행이 시간 순서다. 12-01.cumulative-ack-hole · 14-02.sack-block 과 같은 축 문법을 쓴다.
#           focal 은 블록 셋으로 옵션 칸 40바이트를 다 쓴 다섯째 ACK 한 행.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 512
LX, TX0, TX1 = 24, 232, 720
B0, B1 = 21721, 55025
PITCH = (TX1 - TX0) / (B1 - B0)
def bx(b): return TX0 + (b - B0) * PITCH

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-02 §3",
      "구멍 뒤의 섬이 SACK 블록으로 하나씩 늘어난다",
      "수신자가 돌려보낸 ACK 여섯 개를 위에서 아래로 시간순으로 놓았다. ACK 번호는 21721 에 멈춘 채 구멍 뒤에 받은 범위가 블록으로 늘고, "
      "블록이 하나 늘 때마다 IP 길이가 8바이트씩 커진다. 막대 안 숫자는 옵션 안의 순서로, 가장 최근에 받은 블록이 1 이다. "
      "구멍이 메워지면 ACK 번호가 28961 로 뛰고 그 앞의 블록이 목록에서 빠진다.",
      "ACK 번호는 멈춰 있고, 섬은 블록으로 쌓입니다")

ACKS = [
    (21721, [(23169, 24617)], "sack 1 · IP 64"),
    (21721, [(23169, 28961)], "sack 1"),
    (21721, [(30409, 31857), (23169, 28961)], "sack 2 · IP 72"),
    (21721, [(30409, 46337), (23169, 28961)], "sack 2"),
    (21721, [(47785, 55025), (30409, 46337), (23169, 28961)], "sack 3 · IP 80"),
    (28961, [(47785, 55025), (30409, 46337)], "sack 2"),
]
FOCAL = 4
Y_AX, Y0, ROW_H, BAR_H = 112, 132, 52, 24

# 축 눈금
for b in (21721, 28961, 46337, 55025):
    d.t(bx(b), Y_AX, str(b), 11, SOFT, MONO)
    d.line(bx(b), Y_AX + 8, bx(b), Y0 + len(ACKS) * ROW_H - 4, RULE, 0.6, "2 4")
d.t(TX1 + 32, Y_AX, "옵션", 12, SOFT, KR, "start", 600)

for i, (ack, blocks, note) in enumerate(ACKS):
    y = Y0 + i * ROW_H
    if i == FOCAL:
        d.o.append(f'<rect x="{LX - 8}" y="{y}" width="{W - 40 - (LX - 8)}" height="{ROW_H - 8}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(LX - 8, y, W - 40 - (LX - 8), ROW_H - 8, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, y + 27, f"ack {ack}", 13, ACC if i == FOCAL else INK, MONO, "start", 600)
    d.t(TX1 + 32, y + 27, note, 12, ACC if i == FOCAL else MUTED, MONO, "start", 600)
    by = y + 10
    # 구멍 — ACK 번호부터 가장 오른쪽 블록까지 중 어느 블록에도 들지 않은 범위
    got = sorted(blocks)
    cur = ack
    for l, r in got:
        if l > cur:
            x, w = bx(cur), bx(l) - bx(cur)
            d.o.append(f'<rect x="{x}" y="{by}" width="{w}" height="{BAR_H}" rx="3" fill="none" stroke="{BAD}" stroke-width="1.1" stroke-dasharray="4 3"/>')
        cur = max(cur, r)
    # ACK 번호 — 경계선 하나
    d.line(bx(ack), y + 4, bx(ack), y + ROW_H - 12, MUTED, 2.0)
    for k, (l, r) in enumerate(blocks, start=1):
        x, w = bx(l), bx(r) - bx(l)
        d.tone(x, by, w, BAR_H, INFO, 3, "14", 1.0)
        d.t(x + w / 2, by + 17, str(k), 12, INFO, MONO, "middle", 600)

d.legend(H - 56, [("옵션 칸 40바이트를 다 쓴 ACK", ACC), ("SACK 블록 · 숫자는 옵션 안 순서", INFO), ("아직 안 온 구멍", BAD)])
d.save("13-02.sack-growth.svg")
