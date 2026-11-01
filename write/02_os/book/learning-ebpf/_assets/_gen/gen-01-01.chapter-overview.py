# 타입 스펙: type-layers — 하드웨어부터 커널 각 훅 및 사용자 공간 앱·컨테이너까지 eBPF 프로그램이 부착되는 계층 구조
# 사실 출처: 《Learning eBPF》 Ch.1 1~15쪽(PDF 16쪽 중 16쪽은 각주), 본문 §1~§5. 계층별 절 태그는 본문 줄로 확인(2026-11-01 dverifya)
#   L1 §2 비특권 계층(90행)·§5 네임스페이스(174행) / L2 §2 sys_enter(122행)·§4 bpf() 적재(156행) / L3 §1 kprobe Linux 4.1(74행)
#   L4 §1 Katran eBPF/XDP(74행)·§4 XDP 논문(166행)·§5 커널 네트워크 스택(182행) / L5 §1 LSM BPF Linux 5.7(76행) / L6 §2 디스크·네트워크·메모리는 커널만(90행)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "LEARNING EBPF · 01-01", "커널 계층과 훅에 부착되는 eBPF 아키텍처",
      "사용자 공간부터 하드웨어까지 여섯 계층과 eBPF 훅 부착 지점",
      "사용자 공간 · 시스템 콜 경계 · 커널 안 훅 · 하드웨어")

LX, LW, LH, STRIDE, Y0 = 36, 848, 48, 56, 108
layers = [
    ("L1", "사용자 공간", "컨테이너 및 애플리케이션 프로세스", "§2 비특권 계층 · §5 네임스페이스", None),
    ("L2", "시스템 콜 경계", "bpf() · openat · execve · write", "§2 sys_enter · §4 bpf() 적재", "ebpf"),
    ("L3", "커널 이벤트 계측", "kprobe", "§1 추적 (Linux 4.1)", "ebpf"),
    ("L4", "네트워크 데이터패스", "XDP · 커널 네트워크 스택", "§1·§4 XDP · §5 사이드카 경로", "ebpf"),
    ("L5", "보안 모듈 계층", "LSM(Linux Security Module) 훅", "§1 LSM BPF (Linux 5.7)", "ebpf"),
    ("L6", "하드웨어 계층", "메모리 · 디스크 · 네트워크", "§2 커널만 직접 접근", None),
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
    d.t(LX + 220, y + 30, sub, 12, INK if mark else MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "start")
    d.t(LX + LW - 16, y + 30, note, 12, MUTED, KR, "end")
    if mark == "ebpf":
        d.chip(LX + LW - 280, y + 24, "eBPF 훅 부착", ACC, size=12)

d.legend(450, [
    ("일반 실행 계층", SOFT),
    ("eBPF 훅 부착 지점", ACC),
])
d.save("01-01.chapter-overview.svg")
