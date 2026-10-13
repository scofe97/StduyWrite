# 타입 스펙: type-layers — 하드웨어부터 커널 각 훅 및 사용자 공간 앱·컨테이너까지 eBPF 프로그램이 부착되는 계층 구조
# 사실 출처: 원문 ebpf1.txt 4-22·108-150·204-213, docs.kernel.org bpf
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "LEARNING EBPF · 01-01", "커널 계층과 훅에 부착되는 eBPF 아키텍처",
      "애플리케이션 수정 없이 커널 각 훅에서 이벤트를 관측하고 제어합니다",
      "사용자 공간 격리 · 커널 주요 서브시스템 훅 · 하드웨어 중재")

LX, LW, LH, STRIDE, Y0 = 36, 848, 48, 56, 108
layers = [
    ("L1", "사용자 공간", "컨테이너 및 애플리케이션 프로세스", "네임스페이스 격리", None),
    ("L2", "시스템 콜 경계", "bpf() · openat · execve · write", "sys_enter 진입점 관측", "ebpf"),
    ("L3", "커널 이벤트 계측", "kprobe", "커널 함수 동적 추적", "ebpf"),
    ("L4", "네트워크 데이터패스", "XDP · 커널 네트워크 스택", "패킷 필터링", "ebpf"),
    ("L5", "보안 모듈 계층", "LSM(Linux Security Module) 훅", "보안 연산 허용·거부", "ebpf"),
    ("L6", "하드웨어 계층", "CPU · 메모리 · 디스크 · 네트워크", "하드웨어 자원 중재", None),
]

for i, (tag, name, sub, note, mark) in enumerate(layers):
    y = Y0 + i * STRIDE
    if mark == "ebpf":
        d.tone(LX, y, LW, LH, ACC, r=6, op="12", sw=1.3)
        nc = ACC
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 0.9, 6)
        nc = INK
    d.t(LX + 16, y + 22, tag, 10, SOFT, MONO, "start")
    d.t(LX + 54, y + 30, name, 14, nc, KR, "start", 600)
    d.t(LX + 220, y + 30, sub, 12, INK if mark else MUTED, MONO if "." in sub or "(" in sub else KR, "start")
    d.t(LX + LW - 16, y + 30, note, 12, MUTED, KR, "end")
    if mark == "ebpf":
        d.chip(LX + LW - 280, y + 24, "eBPF 훅 부착", ACC, size=12)

d.legend(450, [
    ("일반 실행 계층", SOFT),
    ("eBPF 훅 부착 지점", ACC),
])
d.save("01-01.chapter-overview.svg")
