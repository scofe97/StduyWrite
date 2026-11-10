# 05-02 §3 — LVM CoW 스냅숏의 생명주기와 Data% 증가 및 복구/삭제 상태 전이.
# 타입 스펙: type-state — 스냅숏 생성 -> 쓰기 발생에 따른 Data% 증가 -> 병합(merge) 또는 삭제(remove) 전이.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 580
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §3",
      "LVM 스냅샷의 CoW 생명주기와 Data% 상태 전이",
      "스냅숏은 바뀐 블록이 없는 상태에서 시작해, 원본에 쓰기가 일어날 때마다 바뀌기 전 블록을 COW 영역에 복사하므로 Data% 가 오릅니다. "
      "작업 후에는 롤백 병합(merge)하거나 삭제(remove)해 쓰기 오버헤드를 제거합니다.",
      "COW 영역이 가득 차면 스냅숏은 무효(Invalid)가 된다 · man·커널 문서 기준, 이 환경에서는 못 잼")

# 상태 1: 스냅숏 생성
S1X, S1Y, SW, SH = 32, 140, 240, 150
d.box(S1X, S1Y, SW, SH, PAPER2, INFO, 1.2, 8)
d.t(S1X + 16, S1Y + 28, "1. 스냅숏 생성 (초기 상태)", 13.5, INFO, KR, "start", 600)
d.t(S1X + 16, S1Y + 50, "lvcreate -s -L 50M -n snap ...", 11, INK, MONO, "start")
d.line(S1X + 14, S1Y + 62, S1X + SW - 14, S1Y + 62, RULE, 1)
d.t(S1X + 16, S1Y + 84, "Data% : 거의 0", 13, OK, MONO, "start", 600)
d.t(S1X + 16, S1Y + 106, "아직 복사된 블록이 없음", 11, MUTED, KR, "start")
d.t(S1X + 16, S1Y + 126, "COW 영역이 비어 있음", 11, SOFT, KR, "start")

# 상태 2: 쓰기 발생 및 Data% 상승
S2X, S2Y = 320, 140
d.box(S2X, S2Y, SW, SH, PAPER2, WARN, 1.2, 8)
d.t(S2X + 16, S2Y + 28, "2. 원본 쓰기 및 CoW 누적", 13.5, WARN, KR, "start", 600)
d.t(S2X + 16, S2Y + 50, "원본 LV 에 쓰기", 11, INK, MONO, "start")
d.line(S2X + 14, S2Y + 62, S2X + SW - 14, S2Y + 62, RULE, 1)
d.t(S2X + 16, S2Y + 84, "Data% : 바뀐 양만큼 증가", 13, WARN, MONO, "start", 600)
d.t(S2X + 16, S2Y + 106, "수정 직전 원본 블록을 스냅숏으로 복사", 11, MUTED, KR, "start")
d.t(S2X + 16, S2Y + 126, "쓰기마다 복사가 더해져 느려짐", 11, SOFT, KR, "start")

# 전이 화살표 1 -> 2
d.arrow([(S1X + SW, S1Y + SH / 2), (S2X - 2, S2Y + SH / 2)], MUTED, "ar", 1.4)
d.t((S1X + SW + S2X) / 2, S1Y + SH / 2 - 10, "쓰기", 11, MUTED, KR, "middle")

# 상태 3A: 병합 (롤백)
S3AX, S3AY, S3W, S3H = 608, 118, 240, 104
d.box(S3AX, S3AY, S3W, S3H, PAPER2, OK, 1.2, 8)
d.t(S3AX + 16, S3AY + 26, "3A. 스냅숏 시점 롤백 (Merge)", 13, OK, KR, "start", 600)
d.t(S3AX + 16, S3AY + 46, "lvconvert --merge vg0/snap", 11, INK, MONO, "start")
d.line(S3AX + 14, S3AY + 56, S3AX + S3W - 14, S3AY + 56, RULE, 1)
d.t(S3AX + 16, S3AY + 76, "보존한 원래 블록을 원본에 되씀", 11, MUTED, KR, "start")
d.t(S3AX + 16, S3AY + 94, "병합이 끝나면 스냅숏은 제거됨", 11, MUTED, KR, "start")

# 상태 3B: 정상 삭제
S3BX, S3BY = 608, 234
d.box(S3BX, S3BY, S3W, S3H, PAPER2, ACC, 1.2, 8)
d.t(S3BX + 16, S3BY + 26, "3B. 작업 완료 후 삭제 (Remove)", 13, ACC, KR, "start", 600)
d.t(S3BX + 16, S3BY + 46, "lvremove -y vg0/snap", 11, INK, MONO, "start")
d.line(S3BX + 14, S3BY + 56, S3BX + S3W - 14, S3BY + 56, RULE, 1)
d.t(S3BX + 16, S3BY + 76, "스냅숏 전용 PE 회수, 원본 최신본 유지", 11, MUTED, KR, "start")

# 전이 화살표 2 -> 3A, 2 -> 3B
d.arrow([(S2X + SW, S3AY + S3H / 2), (S3AX - 2, S3AY + S3H / 2)], OK, "ok", 1.4)
d.arrow([(S2X + SW, S3BY + S3H / 2), (S3BX - 2, S3BY + S3H / 2)], ACC, "acc", 1.4)

# 하단 경고 영역: 100% 소진 시
WY = 370
d.tone(32, WY, W - 64, 56, BAD)
d.t(48, WY + 24, "COW 영역이 가득 차면: 스냅숏 무효", 13, BAD, KR, "start", 600)

d.t(48, WY + 44, "lvs 상태 칸 I(Invalid snapshot) · 크기는 예상 변경량보다 넉넉히", 11, INK, KR, "start")

# 환경 한계 주석: OrbStack dm-snapshot 부재 사실
EY = 446
d.box(32, EY, W - 64, 50, PAPER2, RULE, 1.0, 6)
d.t(48, EY + 20, "이 노트의 실측 환경 (OrbStack 커널, dm 타깃 striped·linear·error 뿐)", 11, SOFT, KR, "start", 600)
d.t(48, EY + 36, "lvcreate -s → snapshot: Required device-mapper target(s) not detected in your kernel. (exit 3)", 11, MUTED, MONO, "start")

d.legend(524, [("정상 초기 / 롤백 상태", OK), ("쓰기 누적 주의 상태", WARN), ("삭제 종료 상태", ACC), ("무효 위험", BAD)])
d.save("05-02.snapshot.svg")
print("ok 05-02.snapshot")
