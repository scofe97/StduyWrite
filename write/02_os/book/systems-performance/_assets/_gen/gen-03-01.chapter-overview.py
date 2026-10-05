# 03-01 전체 지도 — 커널이 깨어나는 세 길(syscall·인터럽트·tick)과 그 일의 주인(프로세스·스택).
# 타입 스펙: type-layers — 여덟 절이 어휘 → 무대 → 경계 → 세 진입 → 주체 → 흔적으로 내려가는 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다(폴더 개요 관례, 10-04 와 같은 stride).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 928, 724
BX, BW, BH, Y0, STRIDE = 96, 736, 56, 108, 64

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-01",
       "커널이 깨어나는 세 길과 그 일의 주인",
       "03-01 의 여덟 절. 어휘와 커널·두 모드를 세운 뒤, 커널에 들어가는 세 길(시스템 콜·인터럽트·tick)을 보고, 그 일을 하는 프로세스와 지나온 길을 남기는 스택으로 내려간다.",
       "모든 진입은 유저·커널 경계를 넘고, 넘을 때마다 비용이 듭니다")

BANDS = [
    ("§1", "핵심 용어", "프로세스 · 스레드 · 태스크 · 두 전환", "어휘", None),
    ("§2", "커널", "monolithic · 요청이 올 때만 실행", "무대", None),
    ("§3", "커널 모드와 유저 모드", "privilege ring · 모드 전환 · 컨텍스트 전환", "모든 진입이 넘는 경계", ACC),
    ("§4", "시스템 콜", "프로세스가 부른다 · ioctl · mmap · futex", "진입 1", INFO),
    ("§5", "인터럽트", "장치가 알린다 · top half · bottom half", "진입 2", INFO),
    ("§6", "클럭과 idle", "타이머가 울린다 · tick · tickless", "진입 3", INFO),
    ("§7", "프로세스", "fork · exec · COW · 수명주기", "일의 주인", None),
    ("§8", "스택", "호출 경로 · 유저 스택 · 커널 스택", "지나온 길", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 34, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 24, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 44, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 34, role, 13, c if c else SOFT, KR, "end")

d.legend(Y0 + 8 * STRIDE + 24, [("모든 진입이 넘는 경계", ACC), ("커널에 들어가는 길", INFO), ("어휘 · 주체 · 흔적", MUTED)])
d.save("03-01.chapter-overview.svg")
