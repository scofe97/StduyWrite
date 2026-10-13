# 타입 스펙: type-process — 같은 레코드 배치가 복사되며 자리를 옮기는 단계. 칸 사이를 건너가는 것은 데이터 하나(복사본 개수)이고, 두 줄을 겹쳐 read·write 길과 sendfile 길을 견준다.
# 사실 출처: Kafka 4.3 설계 문서 Efficiency 절 https://kafka.apache.org/43/design/design/#efficiency (디스크→페이지 캐시→사용자 버퍼→소켓 버퍼→NIC 네 번 복사와 시스템 콜 두 번, sendfile 은 최종 NIC 복사만). sendfile(2) https://man7.org/linux/man-pages/man2/sendfile.2.html
# Layout conventions: 상자 폭 120·높이 56, 가로 stride 180(x=48+180k), 두 줄 y=128 · y=260(stride 132), 복사 번호 칩은 화살표 위. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 420
d = D(W, H, "BYTEBYTEGO · 05-01 §2",
      "복사 네 번이 두 번으로 준다",
      "같은 레코드 배치가 read·write 길에서는 사용자 버퍼를 거치고 sendfile 길에서는 건너뜁니다",
      "상자 안 작은 막대가 레코드 배치의 복사본입니다")

BW, BH, STRIDE, X0 = 120, 56, 180, 48
names = ["디스크", "페이지 캐시", "사용자 버퍼", "소켓 버퍼", "NIC"]
ZONE = [INFO, INFO, WARN, INFO, INFO]


def box(x, y, name, c, held):
    if held:
        d.tone(x, y, BW, BH, c, 6, "14", 1.2)
        d.tone(x + 16, y + 34, 32, 10, ACC, 2, "55", 1.0)
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(x + BW / 2, y + 22, name, 12, INK if held else SOFT, KR, "middle", 600 if held else 400)


# 줄 A — read · write 길: 복사 4회
YA = 128
d.t(X0, YA - 16, "read · write", 13, WARN, MONO, "start", 600)
d.t(X0 + 140, YA - 16, "복사 4회 · 시스템 콜 2회", 12, MUTED, KR, "start")
for k, n in enumerate(names):
    box(X0 + k * STRIDE, YA, n, ZONE[k], True)
for k in range(4):
    x1 = X0 + k * STRIDE + BW + 2
    x2 = X0 + (k + 1) * STRIDE - 4
    d.arrow([(x1, YA + BH / 2), (x2, YA + BH / 2)], WARN, "warn", 1.6)
    d.chip((x1 + x2) / 2, YA + BH / 2 - 16, str(k + 1), WARN)

# 줄 B — sendfile 길: 복사 2회
YB = 260
d.t(X0, YB - 16, "sendfile", 13, OK, MONO, "start", 600)
d.t(X0 + 140, YB - 16, "복사 2회 · 시스템 콜 1회", 12, MUTED, KR, "start")
for k, n in enumerate(names):
    box(X0 + k * STRIDE, YB, n, OK if k in (0, 1, 4) else INFO, k in (0, 1, 4))
x1 = X0 + BW + 2
x2 = X0 + STRIDE - 4
d.arrow([(x1, YB + BH / 2), (x2, YB + BH / 2)], OK, "ok", 1.6)
d.chip((x1 + x2) / 2, YB + BH / 2 - 16, "1", OK)
cx1 = X0 + 1 * STRIDE + BW / 2
cx2 = X0 + 4 * STRIDE + BW / 2
yd = YB + BH + 28
d.arrow([(cx1, YB + BH + 2), (cx1, yd), (cx2, yd), (cx2, YB + BH + 4)], OK, "ok", 1.6)
d.chip((cx1 + cx2) / 2, yd - 14, "2", OK)

d.legend(H - 56, [("read · write 의 복사", WARN), ("sendfile 의 복사", OK), ("건너뛴 버퍼", SOFT)])
d.save("05-01.zero-copy-process.svg")
