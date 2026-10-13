# 타입 스펙: type-swimlane — 레인 넷(로더 · BPF 파일시스템 · 훅 · 커널 참조) × 사건 여섯. 사건마다 참조 증감만 그린다. focal 은 참조가 0 이 되어 해제되는 마지막 칸.
# 사실 출처: 추출본 src/ebpf4.txt 450~456행(fd 닫힘 → 참조 감소 → 없으면 제거)·487~494행(부착이 참조를 더함, 추적 부착은 프로세스 종료 시 감소)·1102~1111행(연습 4: bpftool prog pin name hello /sys/fs/bpf/hi, rm /sys/fs/bpf/hi)
#   고정이 참조를 유지하고 unlink 로 풀린다는 설명은 linux v7.2 include/uapi/linux/bpf.h 줄 276~290(BPF_OBJ_PIN). 값은 절대 개수가 아니라 증감.
# Layout conventions: 레인 높이 84·열 폭 128·단계 상자 132×44, 레인 라벨 x=24, 첫 열 x=170. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 04-01 §4",
      "프로그램 참조가 늘고 주는 사건의 순서",
      "BPF_PROG_LOAD·kprobe 부착·prog pin 이 참조를 하나씩 더하고, 프로세스 종료는 fd 와 추적 부착의 참조를 줄이며, 고정 경로를 지우면 0 이 되어 해제된다.",
      "고정이 참조를 하나 쥐고 있는 동안 프로그램이 남습니다")

LANE_Y0, LH = 104, 84
LANES = ["로더 프로세스", "BPF 파일시스템", "훅 · 링크", "커널 참조 증감"]
for k, nm in enumerate(LANES):
    y = LANE_Y0 + k * LH
    if k % 2 == 0:
        d.o.append(f'<rect x="12" y="{y}" width="{W-24}" height="{LH}" fill="#F5F5F3" fill-opacity="0.025"/>')
    d.line(12, y, W - 12, y, RULE, 0.8)
    d.t(24, y + LH/2 + 4, nm, 13, INK, KR, "start", 600)
d.line(12, LANE_Y0 + 4 * LH, W - 12, LANE_Y0 + 4 * LH, RULE, 0.8)

CX0, CWD, BW, BH = 170, 128, 132, 44
def cx(c): return CX0 + c * CWD + CWD // 2

# (열, 레인, 제목, 부제, 증감 텍스트, 색)
EV = [
    (0, 0, "BPF_PROG_LOAD", "fd 6", "+1", OK),
    (1, 2, "kprobe 부착", "추적 부착", "+1", OK),
    (2, 1, "prog pin", "/sys/fs/bpf/hi", "+1", OK),
    (3, 0, "프로세스 종료", "fd 닫힘", "−1", WARN),
    (4, 2, "부착 해제", "추적 부착", "−1", WARN),
    (5, 1, "rm", "/sys/fs/bpf/hi", "−1 · 해제", ACC),
]
MKN = {OK: "ok", WARN: "warn", ACC: "acc"}
RL = 3
for col, lane, ttl, sub, delta, c in EV:
    y = LANE_Y0 + lane * LH + (LH - BH) // 2
    ry = LANE_Y0 + RL * LH + (LH - BH) // 2
    x = cx(col) - BW // 2
    # 세로 화살표 — 단계 상자 아래에서 증감 칩 위까지
    d.arrow([(cx(col), y + BH + 2), (cx(col), ry - 6)], c, MKN[c], 1.5)
for col, lane, ttl, sub, delta, c in EV:
    y = LANE_Y0 + lane * LH + (LH - BH) // 2
    ry = LANE_Y0 + RL * LH + (LH - BH) // 2
    x = cx(col) - BW // 2
    d.tone(x, y, BW, BH, c if c != ACC else MUTED, 6, "12", 1.2)
    d.t(cx(col), y + 19, ttl, 13, INK, KR if any("가" <= ch <= "힣" for ch in ttl) else MONO, "middle", 600)
    d.t(cx(col), y + 36, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
    w = 112
    x = cx(col) - w // 2
    d.tone(x, ry, w, BH, c, 6, "1F" if c == ACC else "12", 1.4 if c == ACC else 1.2)
    d.t(cx(col), ry + 28, delta, 14, c, MONO if all(ord(ch) < 128 or ch in "−" for ch in delta) else KR, "middle", 600)

d.legend(H - 56, [("참조 +1", OK), ("참조 −1", WARN), ("0 · 해제", ACC)])
d.save("04-01.reference-lifetime.svg")
