# 03-02 §4 — 원서 표 3.2 의 캐시 열다섯 층과, 9번 페이지 캐시에서 적중해 아래로 내려가지 않는 읽기 요청 하나.
# 타입 스펙: type-layers — 확인되는 순서대로 위아래로 쌓인 캐시 층이다.
#           축약: 층이 열다섯이라 스펙 범위(56–72px)보다 얇은 높이 28 · stride 32 로 쌓고, 인덱스 태그를 표 순서로 채운다.
#           세 구역(클라이언트·앱·서버 / 커널 / 장치) 묶음은 본문의 읽기용 구분이며 원서 표에는 없다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 724
LX, LW, LH, Y0, ST = 176, 520, 28, 116, 32
HIT = 8   # 0-index → 9번

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-02 §4",
       "캐시 열다섯 층 — 위에서 적중하면 디스크까지 내려가지 않는다",
       "원서 표 3.2 의 캐시 층을 확인되는 순서대로 쌓았다. 오른쪽 읽기 요청은 9번 파일시스템 1차 캐시(페이지 캐시)에서 적중해 그 아래 여섯 층과 디스크에 닿지 않는다.",
       "요청이 멈추는 층이 위일수록 건너뛰는 층이 많습니다")

C = [("클라이언트 캐시", "웹 브라우저 캐시"), ("애플리케이션 캐시", "—"), ("웹 서버 캐시", "Apache 캐시"),
     ("캐싱 서버", "memcached"), ("데이터베이스 캐시", "MySQL 버퍼 캐시"), ("디렉터리 캐시", "dcache"),
     ("파일 메타데이터 캐시", "inode 캐시"), ("OS 버퍼 캐시", "버퍼 캐시"), ("파일시스템 1차 캐시", "페이지 캐시 · ZFS ARC"),
     ("파일시스템 2차 캐시", "ZFS L2ARC"), ("장치 캐시", "ZFS vdev"), ("블록 캐시", "버퍼 캐시"),
     ("디스크 컨트롤러 캐시", "RAID 카드 캐시"), ("스토리지 어레이 캐시", "—"), ("온디스크 캐시", "—")]
for i, (name, ex) in enumerate(C):
    y = Y0 + i * ST
    below = i > HIT
    if i == HIT: d.tone(LX, y, LW, LH, ACC, 4)
    else: d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 4)
    fc = ACC if i == HIT else (SOFT if below else INK)
    d.t(LX - 12, y + 19, f"{i + 1:02d}", 12, SOFT, MONO, "end")
    d.t(LX + 16, y + 19, name, 13, fc, KR, "start", 600 if i == HIT else 400)
    d.t(LX + LW - 16, y + 19, ex, 12, SOFT if below else MUTED, KR, "end")

# 구역 괄호 — 왼쪽
def zone(i1, i2, label, c):
    x = LX - 52
    y1, y2 = Y0 + i1 * ST, Y0 + i2 * ST + LH
    d.path(f"M {x + 8} {y1} L {x} {y1} L {x} {y2} L {x + 8} {y2}", c, 1.4)
    d.t(x - 8, (y1 + y2) / 2 + 5, label, 13, c, KR, "end", 600)
zone(0, 4, "앱 · 서버", OK)
zone(5, 11, "커널", INFO)
zone(12, 14, "장치", WARN)

# 읽기 요청 — 오른쪽에서 위→아래, 9번에서 멈춤
rx = LX + LW + 36
d.t(rx, Y0 - 14, "읽기 요청", 13, INK, KR, "middle", 600)
d.arrow([(rx, Y0), (rx, Y0 + HIT * ST + LH / 2 - 2)], MUTED, "ar", 1.5)
d.arrow([(rx, Y0 + HIT * ST + LH / 2), (LX + LW + 6, Y0 + HIT * ST + LH / 2)], ACC, "acc", 1.7)
d.t(rx + 16, Y0 + HIT * ST + LH / 2 + 5, "적중", 13, ACC, KR, "start", 600)
d.line(rx, Y0 + (HIT + 1) * ST, rx, Y0 + 15 * ST - 4, SOFT, 1.0, "3 6")
d.t(rx + 16, Y0 + 12 * ST + 19, "닿지 않음", 13, SOFT, KR, "start")

d.legend(Y0 + 15 * ST + 20, [("요청이 멈춘 층", ACC), ("앱 · 서버", OK), ("커널", INFO), ("장치", WARN)])
d.save("03-02.cache-layers.svg")
