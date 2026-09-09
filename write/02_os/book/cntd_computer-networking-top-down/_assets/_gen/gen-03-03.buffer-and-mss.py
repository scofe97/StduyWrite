# 03-03 §1 — MSS 가 왜 1,460 인지는 40바이트가 어디에 붙는지를 보면 끝난다.
# 본문 근거: "보내는 호스트가 내보낼 수 있는 가장 큰 링크 층 프레임의 길이를 봅니다. 이것이 MTU 입니다."
#   "TCP 세그먼트가 IP 데이터그램에 담기고 거기에 TCP/IP 헤더(보통 40바이트)가 붙어도 프레임 하나에
#   들어가도록 MSS 를 정합니다." "이더넷과 PPP 의 MTU 가 1,500바이트이므로 전형적인 MSS 가 1,460바이트입니다."
#   그리고 용어 주의 — "MSS 는 세그먼트 안 애플리케이션 데이터의 최대량이지 헤더를 포함한 세그먼트의 최대 크기가 아닙니다."
# 타입 스펙: type-nested — 바깥 칸이 안쪽 칸의 상한을 정하는 관계. 계단 모양이 곧 헤더가 깎아 먹는 자리다.
#   축약: 헤더 폭은 실제 비율(20/1500)로 그리면 1픽셀이라 보이게 키웠다. 가로 길이는 눈금이 아니다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 648
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §1",
      "40바이트가 어디에 붙는지가 MSS 를 정합니다",
      "버퍼에서 한 번에 집을 수 있는 양은 링크 층 프레임에 들어가야 한다는 조건에서 나온다. "
      "MTU 1,500 에서 IP 헤더 20 과 TCP 헤더 20 을 빼면 남는 것이 1,460 이다.",
      "MSS 는 데이터만 세는 값입니다 — 세그먼트 전체가 아닙니다")

d.tone(24, 150, 268, 158, INFO, 6, "10", 1.3)
d.t(44, 178, "송신 버퍼", 12.5, INFO, KR, "start", 600)
d.t(44, 200, "3-way 핸드셰이크 때 마련됩니다", 11, MUTED, KR, "start")
for i in range(5):
    x = 44 + i * 44
    d.o.append(f'<rect x="{x}" y="{224}" width="36" height="26" rx="3" '
               f'fill="{INFO}22" stroke="{INFO}" stroke-width="1.0"/>')
d.t(44, 274, "여기서 한 번에 집을 수 있는 최대량이", 11, MUTED, KR, "start")
d.t(44, 292, "MSS 입니다", 11, ACC, KR, "start", 600)
d.arrow([(296, 230), (322, 230)], INFO, "info", 1.4)

LAYERS = [
    (330, 150, "링크 층 프레임 · MTU 1,500바이트", None, "1,500바이트", WARN),
    (390, 230, "IP 데이터그램", "IP 헤더 20", "1,480바이트", MUTED),
    (450, 310, "TCP 세그먼트", "TCP 헤더 20", "1,460바이트 = MSS", ACC),
]
for x, y, name, hdr, size, col in LAYERS:
    d.t(x, y - 8, name, 11.5, col, KR, "start", 600)
    d.tone(x, y, 976 - x, 60, col, 6, "10", 1.3)
    if hdr:
        d.o.append(f'<rect x="{x}" y="{y}" width="56" height="60" rx="6" '
                   f'fill="{WARN}28" stroke="{WARN}" stroke-width="1.2"/>')
        d.t(x + 28, y + 26, "헤더", 11, WARN, KR)
        d.t(x + 28, y + 44, "20", 11, WARN, MONO)
        d.t((x + 56 + 976) / 2, y + 36, f"페이로드 {size}", 12, INK, KR)
    else:
        d.t((x + 976) / 2, y + 36, f"여기 다 들어가야 합니다 · {size}", 12, INK, KR)

d.t(450, 396, "이 칸의 크기가 곧 MSS 입니다 — 애플리케이션 데이터만 셉니다", 11, ACC, KR, "start")

d.box(24, 424, W - 48, 82, PAPER2, RULE, 0.9, 6)
d.t(44, 450, "이름이 헷갈립니다", 12, INK, KR, "start", 600)
d.t(44, 472, "MSS 는 「최대 세그먼트 크기」인데 실제로 세는 것은 세그먼트가 아니라 그 안의 애플리케이션 데이터입니다. 굳어진 이름이라 그냥 안고 갑니다.",
    11, MUTED, KR, "start")
d.t(44, 492, "그래서 MTU 1,500 과 MSS 1,460 의 차이 40 이 IP 헤더 20 과 TCP 헤더 20 입니다.", 11, WARN, KR, "start")

d.tone(24, 518, W - 48, 62, INFO, 6, "10", 1.2)
d.t(44, 544, "그 버퍼는 양 끝에만 있습니다", 12, INFO, KR, "start", 600)
d.t(44, 566, "연결은 한쪽 호스트의 버퍼·변수·소켓과 다른 쪽의 버퍼·변수·소켓입니다. 사이의 라우터·스위치·중계기에는 어떤 버퍼도 변수도 할당되지 않습니다.",
    11, MUTED, KR, "start")

d.legend(H - 44, [("버퍼와 연결 상태", INFO), ("헤더가 깎는 자리", WARN), ("남는 것 = MSS", ACC)])
d.save("03-03.buffer-and-mss.svg")
print("ok buffer-and-mss")
