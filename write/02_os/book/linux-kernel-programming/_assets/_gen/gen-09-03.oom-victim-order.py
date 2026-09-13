# 09-03 §5 — OOM killer 가 victim 을 고르는 순위. 위가 먼저 죽고 아래로 갈수록 보호된다.
# 본문이 요구한 형태: "OOM score(0~1000) + oom_score_adj" + "root·커널 스레드·HW 디바이스 보유 task 는 선택하지 않는다".
# 타입 스펙: type-pyramid — 순위 계층. 좁은 위가 먼저 선택되고 넓은 아래가 보호되는 다수다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 748
CX, TOPW, BOTW = 470, 336, 816
Y0, BH, GAP = 132, 60, 12

TIERS = [
    ("oom_score_adj = +1000", "거의 확실히 먼저 죽습니다", BAD),
    ("높은 OOM score", "가용 메모리를 가장 많이 쓴 쪽", BAD),
    ("보통 프로세스", "점수 순서대로 후보가 됩니다", WARN),
    ("root 소유 · HW 디바이스 보유", "휴리스틱이 고르지 않습니다", OK),
    ("커널 스레드", "아예 대상이 아닙니다", OK),
    ("oom_score_adj = -1000", "절대 victim 이 되지 않습니다", OK),
]

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-03 §5",
       "누가 먼저 죽는지는 점수가 정합니다",
       "커널은 프로세스마다 OOM score 를 0~1000 으로 유지한다. 0 은 가용 메모리를 전혀 안 쓰는 쪽, 1000 은 전부 쓰는 쪽이다. 거기에 oom_score_adj 를 더한 값이 가장 큰 프로세스가 victim 이 되고, 그 아래로는 커널 휴리스틱이 중요한 task 를 보호한다.",
       "위가 먼저 죽고 아래로 갈수록 보호됩니다 — 폭이 곧 그 층의 두께입니다")

for i, (name, sub, c) in enumerate(TIERS):
    w = TOPW + (BOTW - TOPW) * i / (len(TIERS) - 1)
    y = Y0 + i * (BH + GAP)
    x = CX - w / 2
    focal = i == 0
    if focal:
        d.tone(x, y, w, BH, ACC, 6, "12", 1.4)
    else:
        d.tone(x, y, w, BH, c, 6, "14", 1.1)
    d.t(CX, y + 26, name, 13, ACC if focal else c, MONO if "oom_score_adj" in name else KR, "middle", 600)
    d.t(CX, y + 46, sub, 13, MUTED, KR)

BOT = Y0 + len(TIERS) * (BH + GAP)
d.arrow([(40, Y0 + 8), (40, BOT - 20)], SOFT, "soft", 1.2, "4 6")
d.t(40, Y0 - 10, "먼저", 12, SOFT, KR)
d.t(40, BOT + 4, "나중", 12, SOFT, KR)

d.t(24, BOT + 40, "최종 점수는 oom_score + oom_score_adj 입니다. 조회와 설정은 choom(1) 유틸로 합니다(root 필요).", 13, MUTED, KR, "start")
d.t(24, BOT + 64, "커널 로그의 OOM 진단은 oom_dump_tasks 가 켜져 있어, 살아 있는 모든 thread 와 rss 를 표로 보여 줍니다.", 13, MUTED, KR, "start")
d.t(24, BOT + 88, "합산에는 앱 메모리뿐 아니라 pgtables_bytes 와 swapents 도 들어갑니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("먼저 고르는 쪽 — 이 절의 논점", ACC), ("후보", BAD), ("점수 순서", WARN), ("보호되는 쪽", OK)])
d.save("09-03.oom-victim-order.svg")
print("ok 09-03.oom-victim-order")
