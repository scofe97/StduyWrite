# 09-04 §1 — 도구는 통계에서 트레이싱으로, 마지막에 하드웨어까지 내려간다.
# 타입 스펙: type-layers — 관측 깊이가 내려갈수록 자세해지고 비싸지는 층 지도다.
#           축약: OSI 층이 아니라 관측 대상이라 인덱스 태그를 깊이 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 624
BX, BW, BH, Y0, STRIDE = 156, 668, 60, 116, 68

d = DK(W, H, "SYSTEMS PERFORMANCE · 09-04 §1",
       "디스크 도구는 통계에서 하드웨어로 내려간다",
       "무엇을 알고 싶은지가 깊이를 정한다. 위쪽은 싸고 요약이며, 아래로 갈수록 자세하지만 비싸거나 장치에 직접 묻는다.",
       "가능하면 위에서 끝내고, 아래로는 필요할 때만 내려갑니다")

BANDS = [
    ("01", "디스크별 통계", "iostat", "분석의 출발점", None),
    ("02", "추세 · 압박 · 책임자", "sar · PSI · pidstat", "언제 · 얼마나 · 누가", None),
    ("03", "분포와 이상치", "biolatency · biosnoop", "평균이 가린 것을 본다", ACC),
    ("04", "유발 스택 · 저수준", "biotop · biostacks · blktrace", "왜 났는지까지", None),
    ("05", "커스텀 추적", "bpftrace", "질문을 직접 짠다", None),
    ("06", "컨트롤러 · 펌웨어", "MegaCli · smartctl", "OS 밖에 묻는다", WARN),
]
for i, (n, name, tools, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 36, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 46, tools, 13, MUTED, MONO, "start")
    d.t(BX + BW - 20, y + 36, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 128, Y0 + 4, "싸다 · 요약", 13, SOFT, KR, "start")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 5 * STRIDE + BH - 28)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 128, Y0 + 5 * STRIDE + BH - 4, "비싸다 · 자세", 13, SOFT, KR, "start")

YB = Y0 + 6 * STRIDE + 24
d.t(BX - 128, YB, "RAID 컨트롤러 뒤나 디스크 펌웨어 안에서 벌어지는 일은 OS 통계에 잡히지 않아 별도 도구가 필요합니다", 13, MUTED, KR, "start")

d.legend(YB + 28, [("평균이 가린 것을 보는 층", ACC), ("OS 밖", WARN), ("전통 통계", MUTED)])
d.save("09-04.disk-tools-flow.svg")
