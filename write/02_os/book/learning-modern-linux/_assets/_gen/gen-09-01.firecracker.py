# 09-01 §3 「Firecracker — HTTP 로 다루는 microVM」 — HTTP API 로 microVM 을 다루는 VMM 과, 그 VMM 이 묶는 격리 장치·가상 장치·관측 통로.
# 1차 자료: 본문 §3 「Firecracker」 문단 —
#       "Firecracker 는 KVM 인스턴스를 관리하는 Rust 기반 VMM 이고, 이 VMM 이 관리하는 VM 을 microVM 이라 부릅니다."
#       "호스트에 HTTP API 를 열어 microVM 을 띄우고 조회하고 멈출 수 있게 합니다."
#       "설계 목표는 같은 물리 기계에서 여러 테넌트의 워크로드를 안전하게 돌리는 것입니다."
#       "Amazon Web Services 에서 주로 서버리스 제품인 AWS Lambda 와 AWS Fargate 를 위해 개발했습니다."
#       "네트워크 인터페이스는 호스트의 TUN/TAP 장치로 흉내 냅니다. 블록 장치는 호스트의 파일이 뒤를 받치며 Virtio 장치를 지원합니다."
#       "seccomp 필터를 써서 자신이 쓸 수 있는 호스트 시스템 콜을 제한하며, cgroups 도 함께 쓸 수 있습니다."
#       "관측 쪽에서는 로그와 메트릭을 §2 의 명명 파이프로 모을 수 있습니다."
# 타입 스펙: type-architecture — 호스트 제어, VMM 핵심과 통제 장치, microVM 실행 영역의 구성요소 연결.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 480
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §3",
      "HTTP API 로 microVM 을 띄우고 격리와 가상 장치를 묶는다",
      "Firecracker 의 구성. 호스트는 HTTP API 로 VMM 에 요청하고, VMM 은 seccomp·cgroups 와 "
      "가상 장치·관측 통로를 묶어 KVM 위의 microVM 을 띄웁니다.",
      "호스트는 HTTP API 로 요청하고 VMM 이 microVM 을 띄웁니다")

# 존 3개 (호스트 제어, Firecracker VMM, microVM 실행)
# 1. 왼쪽: 호스트 제어
ZX1, ZY, ZW, ZH = 24, 110, 176, 290
d.box(ZX1, ZY, ZW, ZH, PAPER, RULE, 1.0, 8)
d.t(ZX1 + 16, ZY + 28, "호스트 제어", 13, SOFT, KR, "start", 600)

BX1, BY1, BW1, BH1 = ZX1 + 14, ZY + 48, ZW - 28, 80
d.box(BX1, BY1, BW1, BH1, PAPER2, RULE, 1.1, 6)
d.t(BX1 + BW1 / 2, BY1 + 26, "HTTP API", 14, INK, MONO, "middle", 600)
d.t(BX1 + BW1 / 2, BY1 + 48, "microVM 띄우기", 12, MUTED, KR, "middle")
d.t(BX1 + BW1 / 2, BY1 + 66, "조회 · 멈춤 제어", 12, MUTED, KR, "middle")

BX1_sub, BY1_sub = ZX1 + 14, ZY + 148
d.box(BX1_sub, BY1_sub, BW1, 120, PAPER2, RULE, 0.9, 6)
d.t(BX1_sub + 12, BY1_sub + 24, "개발 배경", 12, SOFT, KR, "start", 600)
d.t(BX1_sub + 12, BY1_sub + 48, "• AWS 가 개발", 11.5, MUTED, KR, "start")
d.t(BX1_sub + 12, BY1_sub + 72, "• 주로 서버리스용", 11.5, MUTED, KR, "start")
d.t(BX1_sub + 12, BY1_sub + 94, "  Lambda · Fargate", 11.5, MUTED, MONO, "start")

# 2. 가운데: Firecracker VMM (FOCAL)
ZX2, ZW2 = 248, 384
d.box(ZX2, ZY, ZW2, ZH, PAPER, ACC, 1.2, 8)
d.t(ZX2 + 16, ZY + 28, "Firecracker VMM (Rust)", 14, ACC, MONO, "start", 600)

# 보안 격리 (상단 2개)
SW, SH = 168, 62
SX1, SY1 = ZX2 + 16, ZY + 44
d.tone(SX1, SY1, SW, SH, WARN, 6, "12", 1.1)
d.t(SX1 + SW / 2, SY1 + 24, "seccomp 필터", 13, WARN, KR, "middle", 600)
d.t(SX1 + SW / 2, SY1 + 46, "시스템 콜 사용 제한", 11.5, INK, KR, "middle")

SX2 = ZX2 + ZW2 - 16 - SW
d.tone(SX2, SY1, SW, SH, WARN, 6, "12", 1.1)
d.t(SX2 + SW / 2, SY1 + 24, "cgroups", 13, WARN, MONO, "middle", 600)
d.t(SX2 + SW / 2, SY1 + 46, "함께 쓸 수 있음", 11.5, INK, KR, "middle")

# 가상 장치 & 관측 (하단 3개)
DW, DH = 110, 68
DY = ZY + 124
DX1 = ZX2 + 16
d.box(DX1, DY, DW, DH, PAPER2, INFO, 1.0, 6)
d.t(DX1 + DW / 2, DY + 24, "TUN/TAP", 12.5, INFO, MONO, "middle", 600)
d.t(DX1 + DW / 2, DY + 44, "네트워크", 11.5, INK, KR, "middle")
d.t(DX1 + DW / 2, DY + 58, "에뮬레이션", 11.5, MUTED, KR, "middle")

DX2 = DX1 + DW + 11
d.box(DX2, DY, DW, DH, PAPER2, INFO, 1.0, 6)
d.t(DX2 + DW / 2, DY + 24, "Virtio", 12.5, INFO, MONO, "middle", 600)
d.t(DX2 + DW / 2, DY + 44, "호스트 파일 기반", 11.5, INK, KR, "middle")
d.t(DX2 + DW / 2, DY + 58, "블록 장치", 11.5, MUTED, KR, "middle")

DX3 = DX2 + DW + 11
d.box(DX3, DY, DW, DH, PAPER2, INFO, 1.0, 6)
d.t(DX3 + DW / 2, DY + 24, "명명 파이프", 12.5, INFO, KR, "middle", 600)
d.t(DX3 + DW / 2, DY + 44, "로그 · 메트릭", 11.5, INK, KR, "middle")
d.t(DX3 + DW / 2, DY + 58, "수집 통로", 11.5, MUTED, KR, "middle")

# VMM 핵심 설명 줄
d.box(ZX2 + 16, ZY + 208, ZW2 - 32, 66, PAPER2, RULE, 1.0, 6)
d.t(ZX2 + ZW2 / 2, ZY + 232, "KVM 인스턴스를 관리하는 VMM", 13, INK, KR, "middle", 600)
d.t(ZX2 + ZW2 / 2, ZY + 254, "HTTP API 요청을 받아 microVM 을 띄우고 멈춤", 12, MUTED, KR, "middle")

# 3. 오른쪽: microVM 실행
ZX3, ZW3 = 680, 176
d.box(ZX3, ZY, ZW3, ZH, PAPER, OK, 1.2, 8)
d.t(ZX3 + 16, ZY + 28, "microVM 실행", 13, OK, KR, "start", 600)

BX3, BY3, BW3, BH3 = ZX3 + 14, ZY + 48, ZW3 - 28, 114
d.tone(BX3, BY3, BW3, BH3, OK, 6, "12", 1.2)
d.t(BX3 + BW3 / 2, BY3 + 26, "microVM", 13.5, OK, MONO, "middle", 600)
d.t(BX3 + BW3 / 2, BY3 + 48, "KVM 인스턴스", 12, OK, KR, "middle")
d.t(BX3 + BW3 / 2, BY3 + 70, "VMM 이 관리하는 VM", 11.5, INK, KR, "middle")
d.t(BX3 + BW3 / 2, BY3 + 92, "테넌트 워크로드", 11.5, MUTED, KR, "middle")

BX3_sub = ZX3 + 14
BY3_sub = ZY + 178
d.box(BX3_sub, BY3_sub, BW3, 96, PAPER2, RULE, 0.9, 6)
d.t(BX3_sub + 12, BY3_sub + 24, "설계 목표", 12, SOFT, KR, "start", 600)
d.t(BX3_sub + 12, BY3_sub + 48, "• 같은 물리 기계", 11.5, MUTED, KR, "start")
d.t(BX3_sub + 12, BY3_sub + 70, "• 여러 테넌트를 안전하게", 11.5, MUTED, KR, "start")

# 연결 화살표 (수평 직교)
y_arr1 = BY1 + BH1 / 2
d.arrow([(ZX1 + ZW, y_arr1), (ZX2 - 4, y_arr1)], MUTED, "ar", 1.4)
d.t((ZX1 + ZW + ZX2) / 2, y_arr1 - 10, "요청", 11.5, MUTED, KR)

y_arr2 = BY3 + BH3 / 2
d.arrow([(ZX2 + ZW2, y_arr2), (ZX3 - 4, y_arr2)], OK, "ok", 1.4)
d.t((ZX2 + ZW2 + ZX3) / 2, y_arr2 - 10, "띄움", 11.5, OK, KR)

d.legend(428, [("VMM", ACC), ("격리 장치 seccomp·cgroups", WARN),
               ("호스트가 흉내 내는 장치·관측 통로", INFO), ("microVM", OK)])

d.save("09-01.firecracker.svg")
print("ok 09-01.firecracker")
