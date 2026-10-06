# 타입 스펙: type-flowchart
# 06-01 TFTP 패킷 디스패치와 바이트 소비 구조
# 사실 출처: NPG Ch.6 p.3-14 (Listing 6-1~6-8, Fig 6-1, 6-2, 6-4, 6-5)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 480
d = D(W, H, "NPG CH.6 — TFTP PACKET DISPATCH",
      "TFTP 패킷 디스패치와 필드 구조",
      "앞 2바이트 OpCode 판독에 따른 네 패킷 분기와 바이트 소비",
      "2바이트 OpCode 판독 후 각 패킷 규격에 따라 바이트 소비")

# 1. 수신 시작
d.box(24, 214, 140, 48, fill=PAPER2, stroke=INFO, r=8)
d.t(94, 234, "데이터그램 수신", 12, INK, KR, "middle", 600)
d.t(94, 252, "최대 516B", 11, MUTED, KR, "middle")

d.arrow([(164, 238), (200, 238)], MUTED, "ar", 1.4)

# 2. OpCode 판독 (Diamond)
pts = "250,208 300,238 250,268 200,238"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{ACC}" stroke-width="1.2"/>')
d.t(250, 232, "OpCode", 12, ACC, MONO, "middle", 600)
d.t(250, 248, "앞 2B 판독", 11, SOFT, KR, "middle")

# 4개 갈래 Y 좌표
y_rrq  = 108
y_data = 192
y_ack  = 276
y_err  = 360

# 칩과 박스 X 기준선
cx_chip = 365
chip_left, chip_right = 330, 400
x_box = 436

# Branch 1: OpRRQ (1)
d.path(f"M 250 208 L 250 {y_rrq + 22} L {chip_left} {y_rrq + 22}", INFO, 1.3)
d.chip(cx_chip, y_rrq + 22, "OpRRQ = 1", INFO, 10, pad=7.1)
d.arrow([(chip_right, y_rrq + 22), (x_box, y_rrq + 22)], INFO, "info", 1.3)
# Byte layout RRQ: [OpCode 2B] [Filename string + 0x00] [Mode string + 0x00]
d.box(x_box, y_rrq, 70, 44, fill=f"{INFO}15", stroke=INFO, r=4)
d.t(x_box + 35, y_rrq + 18, "OpCode", 11, INFO, MONO, "middle", 600)
d.t(x_box + 35, y_rrq + 34, "2B", 10, SOFT, MONO, "middle")

d.box(x_box + 76, y_rrq, 180, 44, fill=PAPER2, stroke=RULE, r=4)
d.t(x_box + 166, y_rrq + 18, "Filename + 0x00", 11, INK, MONO, "middle", 600)
d.t(x_box + 166, y_rrq + 34, "파일명 문자열", 11, SOFT, KR, "middle")

d.box(x_box + 262, y_rrq, 160, 44, fill=PAPER2, stroke=RULE, r=4)
d.t(x_box + 342, y_rrq + 18, "Mode + 0x00", 11, INK, MONO, "middle", 600)
d.t(x_box + 342, y_rrq + 34, "octet 바이너리", 11, SOFT, KR, "middle")

# Branch 2: OpData (3)
d.path(f"M 300 238 L 315 238 L 315 {y_data + 22} L {chip_left} {y_data + 22}", OK, 1.3)
d.chip(cx_chip, y_data + 22, "OpData = 3", OK, 10, pad=4)
d.arrow([(chip_right, y_data + 22), (x_box, y_data + 22)], OK, "ok", 1.3)
# Byte layout DATA: [OpCode 2B] [Block 2B] [Payload <=512B]
d.box(x_box, y_data, 70, 44, fill=f"{OK}15", stroke=OK, r=4)
d.t(x_box + 35, y_data + 18, "OpCode", 11, OK, MONO, "middle", 600)
d.t(x_box + 35, y_data + 34, "2B", 10, SOFT, MONO, "middle")

d.box(x_box + 76, y_data, 100, 44, fill=PAPER2, stroke=RULE, r=4)
d.t(x_box + 126, y_data + 18, "Block #", 11, INK, MONO, "middle", 600)
d.t(x_box + 126, y_data + 34, "2B uint16", 10, SOFT, MONO, "middle")

d.box(x_box + 182, y_data, 240, 44, fill=PAPER2, stroke=RULE, r=4)
d.t(x_box + 302, y_data + 18, "Payload", 11, INK, MONO, "middle", 600)
d.t(x_box + 302, y_data + 34, "최대 512B 블록", 11, SOFT, KR, "middle")

# Branch 3: OpAck (4)
d.path(f"M 300 238 L 315 238 L 315 {y_ack + 22} L {chip_left} {y_ack + 22}", WARN, 1.3)
d.chip(cx_chip, y_ack + 22, "OpAck = 4", WARN, 10, pad=7.1)
d.arrow([(chip_right, y_ack + 22), (x_box, y_ack + 22)], WARN, "warn", 1.3)
# Byte layout ACK: [OpCode 2B] [Block 2B] (총 4B 고정)
d.box(x_box, y_ack, 70, 44, fill=f"{WARN}15", stroke=WARN, r=4)
d.t(x_box + 35, y_ack + 18, "OpCode", 11, WARN, MONO, "middle", 600)
d.t(x_box + 35, y_ack + 34, "2B", 10, SOFT, MONO, "middle")

d.box(x_box + 76, y_ack, 100, 44, fill=PAPER2, stroke=RULE, r=4)
d.t(x_box + 126, y_ack + 18, "Block #", 11, INK, MONO, "middle", 600)
d.t(x_box + 126, y_ack + 34, "2B uint16", 10, SOFT, MONO, "middle")

d.t(x_box + 205, y_ack + 26, "4B 고정 패킷", 11, MUTED, KR, "start")

# Branch 4: OpErr (5)
d.path(f"M 250 268 L 250 {y_err + 22} L {chip_left} {y_err + 22}", BAD, 1.3)
d.chip(cx_chip, y_err + 22, "OpErr = 5", BAD, 10, pad=7.1)
d.arrow([(chip_right, y_err + 22), (x_box, y_err + 22)], BAD, "bad", 1.3)
# Byte layout ERR: [OpCode 2B] [ErrCode 2B] [Message string + 0x00]
d.box(x_box, y_err, 70, 44, fill=f"{BAD}15", stroke=BAD, r=4)
d.t(x_box + 35, y_err + 18, "OpCode", 11, BAD, MONO, "middle", 600)
d.t(x_box + 35, y_err + 34, "2B", 10, SOFT, MONO, "middle")

d.box(x_box + 76, y_err, 100, 44, fill=PAPER2, stroke=RULE, r=4)
d.t(x_box + 126, y_err + 18, "ErrCode", 11, INK, MONO, "middle", 600)
d.t(x_box + 126, y_err + 34, "2B 코드", 11, SOFT, KR, "middle")

d.box(x_box + 182, y_err, 240, 44, fill=PAPER2, stroke=RULE, r=4)
d.t(x_box + 302, y_err + 18, "Message + 0x00", 11, INK, MONO, "middle", 600)
d.t(x_box + 302, y_err + 34, "오류 설명 문자열", 11, SOFT, KR, "middle")

# Legend
d.legend(H - 42, [("읽기 요청", INFO), ("데이터", OK), ("확인응답", WARN), ("오류", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06-01.opcode-dispatch.svg"))
d.save(out)
print(f"saved: {out}")
