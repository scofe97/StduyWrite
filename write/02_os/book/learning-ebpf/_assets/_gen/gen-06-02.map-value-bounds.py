# 타입 스펙: type-nested — 바깥 상자(맵 값 value_size=16) 안에 c(off 0~3)·message[12](off 4~15), 바깥 경계 밖에 걸린 off 16 접근. 옆에 패킷 상자 안 data~data_end 와 data_end++.
# 사실 출처: 예제 chapter6/hello-verifier.bpf.c 7~8행(int c = 1; char message[12]), 추출본 src/ebpf6.txt 463~464행(value_size=16 off=16 size=1),
#   477~491행(vs=16, R2 off=4 umax_value=12), 431~433행(R3 pointer arithmetic on pkt_end prohibited), 커널 v7.2 verifier.c 4175행·13734행.
# Layout conventions: 1바이트 = 26px, 맵 값 x=56..472, 상태 칸 h=56, 패널 둘(x=24·552). 모든 좌표 4의 배수(바이트 폭 26 은 눈금 용도).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, MUTED, INK, SOFT, PAPER2, RULE, KR, MONO

W, H = 960, 444
B = 26
VX, VY = 56, 164
d = D(W, H, "LEARNING EBPF · 06-02 §2",
      "맵 값 16바이트 안의 c 와 message, 그리고 패킷 끝 포인터",
      "message[12] 는 맵 값의 4~15 바이트에 놓인다. 인덱스가 12 가 되면 접근 오프셋은 16 이라 값 바깥이다.",
      "비교로 얻은 상한이 곧 증명이다")

# 패널 틀
d.box(24, 116, 496, 244, "#0D1117", RULE, 0.9, 8)
d.box(552, 116, 384, 244, "#0D1117", RULE, 0.9, 8)

# 맵 값 바깥 상자
d.box(VX - 8, VY - 28, 16 * B + 16, 56 + 40, PAPER2, RULE, 1.0, 6)
d.t(VX, VY - 8, "맵 값 · value_size=16", 13, MUTED, KR, "start")
d.tone(VX, VY, 4 * B, 56, INFO, 4, "12", 1.2)
d.t(VX + 2 * B, VY + 26, "c", 13, INFO, MONO, "middle", 600)
d.t(VX + 2 * B, VY + 44, "off 0~3", 12, MUTED, MONO)
d.tone(VX + 4 * B, VY, 12 * B, 56, ACC, 4, "18", 1.4)
d.t(VX + 10 * B, VY + 26, "message[12]", 13, ACC, MONO, "middle", 600)
d.t(VX + 10 * B, VY + 44, "off 4~15", 12, MUTED, MONO)

# 경계 밖 한 바이트
gx = VX + 16 * B
d.o.append(f'<rect x="{gx + 8}" y="{VY}" width="{B}" height="56" rx="4" fill="none" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 4"/>')

# 통과 접근 — 최대 off 15
okx = VX + 15 * B + B // 2
d.arrow([(okx, 264), (okx, VY + 56 + 4)], OK, "ok", 1.6)
d.t(okx, 284, "최대 off 15 · c < 12", 12, OK, MONO, "end")
# 거부 접근 — off 16
bx = gx + 8 + B // 2
d.arrow([(bx, 316), (bx, VY + 56 + 4)], BAD, "bad", 1.6)
d.t(bx, 336, "off=16 size=1 · c <= 12", 12, BAD, MONO, "end")

# 패킷 패널
PX, PY, PW = 576, 164, 304
d.t(PX, PY - 20, "패킷", 13, MUTED, KR, "start")
d.tone(PX, PY, PW, 56, INFO, 4, "12", 1.2)
d.t(PX + PW / 2, PY + 34, "data ~ data_end", 13, INFO, MONO, "middle", 600)
d.o.append(f'<rect x="{PX + PW + 8}" y="{PY}" width="{B}" height="56" rx="4" fill="none" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 4"/>')
ex = PX + PW + 8 + B // 2
d.arrow([(ex, 316), (ex, PY + 56 + 4)], BAD, "bad", 1.6)
d.t(ex, 336, "data_end++ · pkt_end prohibited", 12, BAD, MONO, "end")

d.legend(H - 56, [("맵 값 안", ACC), ("허용 접근", OK), ("거부 접근", BAD), ("패킷", INFO)])
d.save("06-02.map-value-bounds.svg")
