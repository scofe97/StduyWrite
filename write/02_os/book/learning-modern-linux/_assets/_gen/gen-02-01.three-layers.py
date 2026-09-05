# 02-01 §1 — 리눅스 아키텍처 세 층과 그 사이의 인터페이스.
# 원문("Linux Architecture"): 세 층은 Hardware("From CPUs and main memory to disk drives, network
#       interfaces, and peripheral devices such as keyboards and monitors"), The kernel, User land
#       ("Where the majority of apps are running, including operating system components such as shells,
#       utilities like ps or ssh, and graphical user interfaces such as X Window System–based desktops").
#       커널과 유저 랜드 사이는 "the interface called system calls" 하나이고, 하드웨어 쪽은 "not a single
#       one. It consists of a collection of individual interfaces, usually grouped by hardware" 다섯이다.
#       init 시스템과 시스템 서비스는 커널과 유저 랜드 사이에 있지만 엄밀히는 커널이 아니다.
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. accent 는 저자가 가장 중요하다고 적은 한 층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 644
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §1",
      "세 층과 그 사이를 잇는 인터페이스",
      "원서가 그린 리눅스 아키텍처를 추상 수준으로 쌓은 것. 위와 아래를 잇는 두 인터페이스의 성격이 "
      "다르다는 것이 이 그림의 논점이다. 위쪽은 하나이고 아래쪽은 하드웨어별로 다섯 갈래다.",
      "셸과 ps 는 커널이 아니라 유저 랜드에 있습니다")

X, BOX_W = 76, 728
rows = [
    ("box", "유저 랜드", "셸 · ps · ssh · X Window 기반 데스크톱", 76, False),
    ("iface", "시스템 콜 — 인터페이스 하나", "저자가 가장 중요하다고 적은 경계", 48, True),
    ("box", "커널", "프로세스 · 메모리 · 네트워킹 · 파일시스템 · 문자 장치", 76, False),
    ("iface", "하드웨어 인터페이스 — 다섯 갈래", "CPU · 주 메모리 · 네트워크 · 파일시스템과 블록 장치 · 문자 장치", 48, False),
    ("box", "하드웨어", "CPU · 주 메모리 · 디스크 · 네트워크 인터페이스 · 주변 장치", 76, False),
]

y = 112
for kind, name, note, h, focal in rows:
    if focal:
        d.tone(X, y, BOX_W, h, ACC, r=6)
        d.t(X + 20, y + 26, name, 15, ACC, KR, "start", 600)
        d.t(X + 20, y + 42, note, 12, MUTED, KR, "start")
    elif kind == "iface":
        d.box(X, y, BOX_W, h, PAPER, INFO, 1.0, 6)
        d.t(X + 20, y + 28, name, 14, INFO, KR, "start", 600)
        d.t(X + 20, y + 44, note, 12, MUTED, KR, "start")
    else:
        d.box(X, y, BOX_W, h, PAPER2, RULE, 1.0, 6)
        d.t(X + 20, y + 32, name, 16, INK, KR, "start", 600)
        d.t(X + 20, y + 56, note, 12, MUTED, KR, "start")
    y += h + 12

for _k, _line in enumerate([
        "init 시스템과 네트워킹 같은 시스템 서비스는 커널과 유저 랜드 사이에 앉습니다.",
        "저자는 그것들이 엄밀히 말해 커널의 일부가 아니라고 적습니다.",
        "유저 모드는 느린 대신 안전하고 편한 추상을, 커널 모드는 빠른 대신 얇은 추상을 줍니다."]):
    d.t(X, 512 + _k * 22, _line, 12, MUTED if _k < 2 else SOFT, KR, "start")

d.legend(580, [("인터페이스", INFO), ("가장 중요한 경계", ACC), ("층", MUTED)])
d.save("02-01.three-layers.svg")
print("ok 02-01.three-layers")
