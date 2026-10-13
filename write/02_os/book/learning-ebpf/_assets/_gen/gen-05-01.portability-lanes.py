# 타입 스펙: type-swimlane — 레인 셋(BCC 대상 기계 · CO-RE 빌드 기계 · CO-RE 대상 기계) × 열 넷. 같은 열이 같은 시간대다. focal 은 오프셋을 고쳐 싣는 마지막 칸.
# 사실 출처: BCC 쪽은 추출본 src/ebpf5.txt 43~63행(대상 기계에서 런타임 컴파일 · 툴체인과 헤더 설치 · 시작 지연), 예제 저장소 chapter4/hello-buffer-config.py 45행 `b = BPF(text=program)`,
#   CO-RE 쪽은 추출본 ebpf5.txt 21~28행·97~146행, 오브젝트의 .BTF·재배치 정보와 libbpf 비교·수정은 같은 파일 126~136행, 커널 BTF 경로는 linux v5.4 kernel/bpf/sysfs_btf.c.
# Layout conventions: 레인 높이 96 · 열 폭 200 · 상자 168×56, 레인 라벨 x=24, 첫 열 x=140. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 484
d = D(W, H, "LEARNING EBPF · 05-01 §1",
      "BCC 는 기계마다 컴파일하고 CO-RE 는 한 번 컴파일해 고쳐 싣는다",
      "BCC 는 대상 기계마다 clang 과 커널 헤더로 실행할 때 컴파일한다. CO-RE 는 빌드 기계에서 한 번 컴파일한 오브젝트를 대상 기계의 libbpf 가 커널 BTF 와 비교해 오프셋을 고쳐 싣는다.",
      "같은 오브젝트를 여러 대상 기계에 보냅니다")

LANE_Y0, LH = 104, 96
LANES = [("BCC", "대상 기계마다"), ("CO-RE 빌드", "한 번"), ("CO-RE 대상", "기계마다")]
for k, (nm, sub) in enumerate(LANES):
    y = LANE_Y0 + k * LH
    if k % 2 == 0:
        d.o.append(f'<rect x="12" y="{y}" width="{W-24}" height="{LH}" fill="#F5F5F3" fill-opacity="0.025"/>')
    d.line(12, y, W - 12, y, RULE, 0.8)
    d.t(24, y + LH / 2 - 2, nm, 13, INK, KR, "start", 600)
    d.t(24, y + LH / 2 + 16, sub, 13, MUTED, KR, "start")
d.line(12, LANE_Y0 + 3 * LH, W - 12, LANE_Y0 + 3 * LH, RULE, 0.8)

CX0, CWD, BW, BH = 140, 200, 168, 56


def bx(c):
    return CX0 + c * CWD + (CWD - BW) // 2


def by(lane):
    return LANE_Y0 + lane * LH + (LH - BH) // 2


def isko(s):
    return any("가" <= ch <= "힣" for ch in s)


def cell(lane, col, title, sub, c, fill="12", sw=1.2):
    x, y = bx(col), by(lane)
    d.tone(x, y, BW, BH, c, 6, fill, sw)
    d.t(x + BW / 2, y + 22, title, 13, INK, KR if isko(title) else MONO, "middle", 600)
    d.t(x + BW / 2, y + 42, sub, 13 if isko(sub) else 11, MUTED, KR if isko(sub) else MONO)


# BCC 레인 — 대상 기계마다 컴파일
cell(0, 0, "BPF(text=program)", "C 소스 문자열", INFO)
cell(0, 1, "clang · LLVM", "+ 커널 헤더", WARN)
cell(0, 2, "컴파일", "실행할 때마다", WARN)
cell(0, 3, "적재", "bpf()", INFO)
for c in range(3):
    cy = by(0) + BH // 2
    d.arrow([(bx(c) + BW + 2, cy), (bx(c + 1) - 6, cy)], MUTED, "ar", 1.5)

# CO-RE 빌드 레인
cell(1, 0, "clang", "-target bpf -g -O2", OK)
cell(1, 1, ".bpf.o", ".BTF · 재배치 정보", INFO)
cy1 = by(1) + BH // 2
d.arrow([(bx(0) + BW + 2, cy1), (bx(1) - 6, cy1)], MUTED, "ar", 1.5)

# CO-RE 대상 레인
cell(2, 2, "libbpf", "/sys/kernel/btf/vmlinux", OK)
cell(2, 3, "오프셋 수정 · 적재", "bpf()", ACC, "1F", 1.4)
cy2 = by(2) + BH // 2
d.arrow([(bx(2) + BW + 2, cy2), (bx(3) - 6, cy2)], ACC, "acc", 1.8)

# 오브젝트가 대상 기계로 넘어간다 — ㄷ자
mx = bx(1) + BW + 16
d.arrow([(bx(1) + BW + 2, cy1), (mx, cy1), (mx, cy2), (bx(2) - 6, cy2)], OK, "ok", 1.5)

d.legend(H - 56, [("소스·오브젝트·적재", INFO), ("매번 대상 기계에서", WARN), ("한 번만", OK), ("적재 때 보정", ACC)])
d.save("05-01.portability-lanes.svg")
