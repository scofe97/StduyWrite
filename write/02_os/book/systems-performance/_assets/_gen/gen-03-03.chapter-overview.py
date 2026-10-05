# 03-03 전체 지도 — 비교의 잣대 → 선조 커널 → Linux → 성능에 중요한 세 주제 → 다른 모델과 비교.
# 타입 스펙: type-layers — 일곱 절이 계보(위 셋)에서 Linux 주제(가운데 셋), 판단(아래)으로 내려가는 지도다.
#           축약: 인덱스 태그를 절 번호로 채운다(폴더 개요 관례). focal 은 책 전반의 토대인 §6 Extended BPF.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 928, 660
BX, BW, BH, Y0, STRIDE = 96, 736, 56, 108, 64

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-03",
       "선조 커널에서 Linux, 세 주제, 비교까지",
       "03-03 의 일곱 절. syscall 수로 커널을 가늠하고, Unix·BSD·Solaris 의 성능 기능이 Linux 로 모인 과정과 2.5~5.8 의 발전을 본 뒤, systemd·KPTI·Extended BPF 세 주제와 다른 커널 모델·커널 비교로 끝난다.",
       "Extended BPF 는 15장까지 이어지는 이 책의 토대입니다")

BANDS = [
    ("§1", "커널 비교와 syscall 수", "UNIX V7 48 → Linux 5.3 493", "비교의 잣대", None),
    ("§2", "Unix · BSD · Solaris", "1969 · 1978 · 1982 — 우선순위 · 페이징 · VFS · slab", "선조", None),
    ("§3", "Linux 발전사", "1991 · 선조에게서 물려받음 · 2.5 → 5.8", "물려받고 더한 것", None),
    ("§4", "systemd", "부팅 시간 · critical-chain", "세 주제", INFO),
    ("§5", "KPTI(Meltdown)", "4.14 · syscall 비율에 따라 0.1~6%", "세 주제", INFO),
    ("§6", "Extended BPF", "2014 · 검증기 · map · helper · 이벤트", "세 주제 · 책의 토대", ACC),
    ("§7", "다른 커널 모델과 커널 비교", "PGO · unikernel · microkernel · hybrid · 튜닝 여부", "판단", None),
]
for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 34, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 24, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 44, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 34, role, 13, c if c else SOFT, KR, "end")

d.legend(Y0 + 7 * STRIDE + 24, [("책 전반의 토대", ACC), ("성능에 중요한 Linux 주제", INFO), ("계보 · 판단", MUTED)])
d.save("03-03.chapter-overview.svg")
