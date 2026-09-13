# 09-02 §4 — 전통 LRU 의 두 리스트와 MGLRU 의 세대별 리스트를 같은 눈금에 나란히 세운다.
# 본문이 요구한 형태: "generation 0(가장 젊음·active)부터 generation N-1(가장 오래됨·LRU)까지".
# 주의: kernel.org v6.1 MGLRU 문서는 MAX_NR_GENS 의 구체적 값도, kswapd CPU 절감 백분율도 적지 않는다.
#       둘 다 원서가 든 수치이므로 라벨에 출처를 밝힌다(2026-09-13 축자 인용 확인).
# 타입 스펙: type-layers — 위가 젊은 페이지, 아래가 오래된 페이지. 회수 후보는 아래쪽에서 나온다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 672
AX, AW = 80, 384
BX, BW = 520, 384
RH, RS, Y0 = 64, 76, 168

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-02 §4",
       "두 칸이던 나이를 네 칸으로 나눕니다",
       "전통 LRU 는 active 와 inactive 두 리스트뿐이라 페이지 나이를 두 단계로만 구분했다. MGLRU 는 그 사이에 세대별 리스트를 여럿 두어 page age 로 정렬하고, 가장 오래된 세대부터 회수 후보로 삼는다. 6.1 커널에 병합됐다. 여기 그린 네 세대는 원서가 든 값이고, 커널 문서는 MAX_NR_GENS 의 값을 못 박지 않는다.",
       "세대 수와 절감 수치는 원서가 든 값입니다 — 커널 문서는 그 값을 못 박지 않습니다")

d.t(AX, 136, "전통 LRU", 14, MUTED, KR, "start", 600)
d.t(AX + AW, 136, "두 리스트", 13, SOFT, KR, "end")
d.t(BX, 136, "MGLRU (6.1)", 14, INK, KR, "start", 600)
d.t(BX + BW, 136, "원서 기준 4세대", 13, SOFT, KR, "end")

# 전통 LRU — 두 칸이 네 칸 높이를 나눠 가진다
for i, (name, sub, c) in enumerate([("active", "최근에 쓴 페이지", INFO), ("inactive", "회수 후보", WARN)]):
    y = Y0 + i * (RS * 2)
    h = RH + RS
    d.tone(AX, y, AW, h, c, 8, "14", 1.1)
    d.t(AX + 20, y + 40, name, 14, c, MONO, "start", 600)
    d.t(AX + 20, y + 64, sub, 13, MUTED, KR, "start")

# MGLRU — 세대 넷
GENS = [("generation 0", "가장 젊음 · active 쪽", INFO),
        ("generation 1", "", INFO),
        ("generation 2", "", WARN),
        ("generation 3", "가장 오래됨 · 회수 후보", ACC)]
for i, (name, sub, c) in enumerate(GENS):
    y = Y0 + i * RS
    focal = c is ACC
    d.tone(BX, y, BW, RH, c, 8, "12" if focal else "14", 1.4 if focal else 1.1)
    d.t(BX + 20, y + 28, name, 13, c, MONO, "start", 600)
    if sub:
        d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")

BOT = Y0 + 4 * RS
d.arrow([(48, Y0 + 16), (48, BOT - 16)], SOFT, "soft", 1.2, "4 6")
d.t(48, Y0 - 12, "젊다", 12, SOFT, KR)
d.t(48, BOT + 16, "오래됐다", 12, SOFT, KR)

d.t(24, BOT + 56, "전통 LRU 는 큰 파일을 순차로 읽으면 active 에 올라간 페이지가 다시 안 쓰이는 식으로 어긋나곤 했습니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 80, "MGLRU 는 비싼 rmap 대신 프로세스 PTE 를 직접 스캔해 recent bit 을 봅니다. 원서는 kswapd CPU 51% 절감을 듭니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 104, "대신 메모리를 약간 더 씁니다. CONFIG_LRU_GEN 설정 기능이라 배포판에 따라 기본 비활성일 수 있습니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("최근에 쓴 쪽", INFO), ("중간", WARN), ("가장 오래된 세대 — 먼저 회수", ACC)])
d.save("09-02.mglru-generations.svg")
print("ok 09-02.mglru-generations")
