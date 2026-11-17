# 09-01 §3 「Firecracker — HTTP 로 다루는 microVM」 — HTTP API 로 microVM 을 다루는 VMM 과, 그 VMM 이 묶는 격리 장치·가상 장치·관측 통로.
# 1차 자료: 본문 §3 「Firecracker」 문단 —
#       "Firecracker 는 KVM 인스턴스를 관리하는 Rust 기반 VMM 이고, 이 VMM 이 관리하는 VM 을 microVM 이라 부릅니다."
#       "호스트에 HTTP API 를 열어 microVM 을 띄우고 조회하고 멈출 수 있게 합니다."
#       "설계 목표는 같은 물리 기계에서 여러 테넌트의 워크로드를 안전하게 돌리는 것입니다."
#       "Amazon Web Services 에서 주로 서버리스 제품인 AWS Lambda 와 AWS Fargate 를 위해 개발했습니다."
#       "네트워크 인터페이스는 호스트의 TUN/TAP 장치로 흉내 냅니다. 블록 장치는 호스트의 파일이 뒤를 받치며 Virtio 장치를 지원합니다."
#       "seccomp 필터를 써서 자신이 쓸 수 있는 호스트 시스템 콜을 제한하며, cgroups 도 함께 쓸 수 있습니다."
#       "관측 쪽에서는 로그와 메트릭을 §2 의 명명 파이프로 모을 수 있습니다."
# 타입 스펙: type-architecture — 호스트 위의 실제 구성요소(Firecracker 프로세스 · microVM · KVM · TUN/TAP ·
#           호스트 파일 · 명명 파이프)와 그 사이 연결. microVM 의 가상 장치가 호스트의 어느 객체로 내려가는지,
#           그 길이 seccomp 필터를 지난다는 것을 수직 연결로 보인다. accent 는 Firecracker 프로세스 하나.
# 축약: 호출하는 쪽은 본문이 이름을 대지 않아 점선 "(예)" 로 두었다. cgroups 는 본문이 "함께 쓸 수
#       있다" 고만 해서 점선이다. microVM 은 하나만 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §3",
      "HTTP API 로 microVM 을 띄우고 격리와 가상 장치를 묶는다",
      "Firecracker 를 호스트 위의 실제 구성요소로 나눈 것. 호스트의 호출자가 HTTP API 로 microVM 의 "
      "생성, 조회, 중지를 요청하고, Firecracker 프로세스는 microVM 을 KVM 인스턴스로 돌린다. microVM 의 "
      "네트워크는 호스트 TUN/TAP 장치로, 블록 장치는 호스트 파일과 Virtio 로 이어진다. 호스트로 내려가는 "
      "시스템 콜은 seccomp 필터가 제한하고, 로그와 메트릭은 명명 파이프로 모은다.",
      "microVM 의 장치는 하나씩 호스트의 실제 객체로 내려갑니다")

LX, X0, X1 = 24, 136, 836
PX0 = 336                      # Firecracker 프로세스 왼쪽
for y0, y1, name, sub in ((100, 352, "유저 공간", "호스트"), (396, 492, "호스트", "커널 · 파일")):
    d.o.append(f'<rect x="{LX}" y="{y0}" width="{X1 + 20 - LX}" height="{y1 - y0}" rx="8" '
               f'fill="{PAPER2}" fill-opacity="0.45" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(LX + 14, y0 + 26, name, 13, INK, KR, "start", 600)
    d.t(LX + 14, y0 + 44, sub, 12, SOFT, KR, "start")

KX = (396, 536, 696)           # KVM · TUN/TAP · 호스트 파일 중심

# 선 먼저
d.arrow([(276, 176), (348, 176)], MUTED, "ar", 1.3)
d.arrow([(PX0, 284), (280, 284)], MUTED, "ar", 1.3)
d.arrow([(KX[0], 332), (KX[0], 408)], OK, "ok", 1.4)
d.arrow([(KX[1], 324), (KX[1], 408)], INFO, "info", 1.4)
d.arrow([(KX[2], 324), (KX[2], 408)], INFO, "info", 1.4)
d.line(368, 374, X1, 374, WARN, 1.4, "6 4")

# 왼쪽 — 호출자 · 명명 파이프 · cgroups
d.o.append(f'<rect x="{X0}" y="152" width="140" height="48" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(X0 + 70, 172, "호출자 (예)", 12, SOFT, KR)
d.t(X0 + 70, 190, "호스트 쪽", 12, SOFT, KR)
d.box(X0 + 4, 260, 140, 48, PAPER, MUTED, 1.0, 6)
d.t(X0 + 74, 280, "명명 파이프", 12, INK, KR, "middle", 600)
d.t(X0 + 74, 298, "로그 · 메트릭", 12, MUTED, KR)
d.o.append(f'<rect x="{X0}" y="420" width="160" height="48" rx="6" fill="none" '
           f'stroke="{WARN}" stroke-width="1" stroke-dasharray="4 3"/>')
d.t(X0 + 80, 440, "cgroups", 12, WARN, MONO, "middle", 600)
d.t(X0 + 80, 458, "함께 쓸 수 있음", 12, MUTED, KR)

# Firecracker 프로세스
d.tone(PX0, 116, X1 - PX0, 228, ACC, 8, "10", 1.4)
d.t(PX0 + 16, 138, "Firecracker 프로세스", 13, ACC, KR, "start", 600)
d.t(PX0 + 168, 138, "Rust VMM", 12, INK, MONO, "start")
d.box(352, 152, 220, 48, PAPER, ACC, 1.0, 6)
d.t(366, 172, "HTTP API", 12, INK, MONO, "start", 600)
d.t(366, 190, "생성 · 조회 · 중지", 12, MUTED, KR, "start")
d.tone(352, 212, X1 - 368, 120, OK, 6, "10", 1.2)
d.t(368, 234, "microVM", 13, OK, MONO, "start", 600)
d.t(440, 234, "KVM 인스턴스 · 테넌트 워크로드", 12, MUTED, KR, "start")
for cx, lab in ((KX[1], "네트워크 장치"), (KX[2], "Virtio 블록")):
    d.box(cx - 68, 280, 136, 44, PAPER, INFO, 1.0, 6)
    d.t(cx, 307, lab, 12, INK, KR)

# seccomp
d.t(X0, 379, "seccomp · 시스템 콜 제한 (기본)", 12, WARN, KR, "start")

# 호스트 객체
for cx, name, sub, c, fam in ((KX[0], "KVM", "microVM 실행", OK, MONO),
                              (KX[1], "TUN/TAP", "가상 네트워크", INFO, MONO),
                              (KX[2], "호스트 파일", "블록 장치 뒤", INFO, KR)):
    d.box(cx - 60, 412, 120, 56, PAPER, c, 1.1, 6)
    d.t(cx, 436, name, 12, c, fam, "middle", 600)
    d.t(cx, 456, sub, 12, MUTED, KR)

d.t(LX, 520, "AWS 가 Lambda · Fargate 용으로 개발 · 목표 = 한 물리 기계에서 다중 테넌트 격리 · 점선 = 예시 또는 선택",
    11, SOFT, KR, "start")
d.legend(548, [("Firecracker", ACC), ("microVM · KVM", OK), ("호스트 장치", INFO), ("격리 장치", WARN)])
d.save("09-01.firecracker.svg")
print("ok 09-01.firecracker")
