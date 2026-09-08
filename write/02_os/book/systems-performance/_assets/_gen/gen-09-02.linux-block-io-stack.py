# 09-02 §5 — 앱의 I/O 가 디스크에 닿기까지 커널이 다시 배치한다.
# 타입 스펙: type-layers — 위에서 아래로 내려가는 커널 블록 I/O 경로의 층 지도다.
#           축약: OSI 층이 아니라 커널 컴포넌트라 인덱스 태그를 단계 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 612
BX, BW, BH, Y0, STRIDE = 148, 676, 60, 116, 68

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-02 §5",
       "커널 블록 I/O 스택",
       "앱이 낸 I/O 는 그대로 디스크에 가지 않는다. 커널이 병합하고 순서를 바꾸고 큐에 나눠 담은 뒤에야 장치로 내려간다.",
       "그래서 앱이 발행한 I/O 수와 디스크가 받은 수가 다릅니다")

BANDS = [
    ("01", "애플리케이션 · VFS", "read() · write()", "논리 I/O", None),
    ("02", "파일 시스템", "페이지 캐시가 상당수를 흡수", "미스만 아래로", None),
    ("03", "블록 층 — 병합", "인접 I/O 를 하나로 합침", "수가 줄어든다", ACC),
    ("04", "I/O 스케줄러", "none · mq-deadline · bfq · kyber", "순서를 바꾼다", None),
    ("05", "blk-mq", "CPU 별 큐로 락 경합을 줄임", "병렬로 내보낸다", None),
    ("06", "장치 드라이버 · 디스크", "온디스크 큐로 들어감", "물리 I/O", None),
]
for i, (n, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 36, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 46, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 36, role, 13, c if c else SOFT, KR, "end")

d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 5 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")

YB = Y0 + 6 * STRIDE + 12
d.t(BX - 116, YB, "blk-mq 는 단일 큐의 락 경합을 없애 SSD·NVMe 의 높은 IOPS 를 받아냅니다", 13, MUTED, KR, "start")

d.legend(YB + 28, [("I/O 수를 바꾸는 자리", ACC), ("나머지 단계", MUTED)])
d.save("09-02.linux-block-io-stack.svg")
