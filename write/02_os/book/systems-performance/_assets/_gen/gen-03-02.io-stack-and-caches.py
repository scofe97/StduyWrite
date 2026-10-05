# 03-02 §3 — 원서 그림 3.15 의 일반 I/O 스택 여덟 층과 시스템 콜 → 블록 장치 인터페이스 우회 경로.
# 타입 스펙: type-layers — 애플리케이션부터 디스크 장치까지 위아래로 쌓인 층이다.
#           옛 손 SVG(I/O 스택 + 캐시 층, 블록 아래 두 층 누락)를 대체한다. 파일명은 지휘 결정으로 유지하고
#           캐시 층은 03-02.cache-layers 로 옮겼다. VFS · 파일시스템은 원서 그림처럼 오른쪽으로 들여 우회 화살표 자리를 낸다.
#           층 높이 56 · stride 64. focal 은 VFS.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 732
LX, LW, LH, Y0, ST, IND = 168, 560, 56, 108, 64, 176

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-02 §3",
       "일반 I/O 스택 — 여덟 층과 파일시스템 우회 경로",
       "원서 그림 3.15. 애플리케이션의 요청은 시스템 콜, VFS, 파일시스템을 지나 블록 장치 인터페이스에 닿고, 볼륨 매니저와 HBA 드라이버를 거쳐 디스크 장치에 도착한다. 관리 도구와 데이터베이스는 시스템 콜에서 블록 장치 인터페이스로 바로 내려가기도 한다.",
       "파일시스템을 건너뛰는 길은 시스템 콜 바로 아래에서 갈라집니다")

LAYERS = [("Application", "애플리케이션", 0, None),
          ("System Calls", "시스템 콜", 0, None),
          ("VFS", "파일시스템 유형 추상화", IND, ACC),
          ("File System", "파일시스템", IND, None),
          ("Block Device Interface", "블록 장치 인터페이스", 0, None),
          ("Volume Manager", "볼륨 매니저", 0, INFO),
          ("Host Bus Adapter Driver", "HBA 드라이버", 0, INFO),
          ("Disk Devices", "디스크 장치", 0, None)]
for i, (name, sub, ind, c) in enumerate(LAYERS):
    y = Y0 + i * ST
    x, w = LX + ind, LW - ind
    if c: d.tone(x, y, w, LH, c, 6)
    else: d.box(x, y, w, LH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, y + 34, name, 14, c if c else INK, MONO, "start", 600)
    d.t(x + w - 20, y + 34, sub, 13, MUTED, KR, "end")
    d.t(LX - 20, y + 34, f"{i + 1:02d}", 12, SOFT, MONO, "end")
    if i < 7:
        ax = LX + IND + (LW - IND) / 2 if i in (1, 2, 3) else LX + LW / 2
        if i == 1: ax = LX + IND + (LW - IND) / 2
        d.arrow([(ax, y + LH), (ax, y + ST - 2)], MUTED, "ar", 1.2)

# 우회 — System Calls 아래에서 Block Device Interface 로
bx = LX + 48
d.arrow([(bx, Y0 + ST + LH), (bx, Y0 + 4 * ST - 2)], WARN, "warn", 1.7)
d.t(bx + 12, Y0 + 2 * ST + 34, "우회", 13, WARN, KR, "start", 600)
d.t(bx + 12, Y0 + 2 * ST + 52, "관리 도구 · DB", 12, MUTED, KR, "start")

# 오른쪽 구역 괄호
def bracket(i1, i2, label, c):
    x = LX + LW + 20
    y1, y2 = Y0 + i1 * ST, Y0 + i2 * ST + LH
    d.path(f"M {x - 8} {y1} L {x} {y1} L {x} {y2} L {x - 8} {y2}", c, 1.4)
    d.t(x + 12, (y1 + y2) / 2 + 5, label, 13, c, KR, "start", 600)
bracket(2, 3, "파일시스템 경로", ACC)
bracket(5, 6, "블록 아래 두 층", INFO)

d.legend(Y0 + 8 * ST + 16, [("유형을 감추는 VFS", ACC), ("블록 장치 아래의 두 층", INFO), ("파일시스템 우회", WARN)])
d.save("03-02.io-stack-and-caches.svg")
