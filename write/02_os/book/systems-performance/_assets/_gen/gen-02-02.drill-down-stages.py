# 02-02 §6 — 드릴다운 세 단계와 분석 단계의 Five Whys.
# 타입 스펙: type-process — Stage framework with semantic slots. 단계마다 하는 일·범용 도구·Netflix 가 같은 칸에 반복된다.
#           축약: 주체(lane) 대신 카드 stride. 아래 줄 Five Whys 는 원서 2.5.12 의 실화 다섯 단계.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 928, 560
X0, CW, GAP, Y0, CH = 24, 272, 36, 120, 208
STAGES = [
    ("1", "모니터링", "장기 통계 기록 · 경고", "SNMP · exporter", "Atlas"),
    ("2", "식별", "자원·영역으로 좁힘", "vmstat · iostat · mpstat", "perfdash"),
    ("3", "분석", "근본 원인 정량화", "strace · perf · bpftrace", "FlameCommander"),
]
SLOTS = ["하는 일", "범용 도구", "Netflix"]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-02 §6",
       "넓게 보고, 좁히고, 파고든다",
       "드릴다운 세 단계마다 하는 일·범용 도구·Netflix 구현을 같은 칸에 놓았다. 아래 줄은 분석 단계에서 \"왜?\"를 다섯 번 물은 실화다.",
       "원서 2.5.12 · McDougall 06a 의 세 단계")

for i, (n, name, job, tool, nf) in enumerate(STAGES):
    x = X0 + i * (CW + GAP)
    focal = name == "분석"
    if focal: d.tone(x, Y0, CW, CH, ACC, 8)
    else: d.box(x, Y0, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y0 + 30, f"{n}  {name}", 15, ACC if focal else INK, KR, "start", 600)
    d.line(x + 16, Y0 + 46, x + CW - 16, Y0 + 46, RULE, 0.8)
    for k, (slot, val) in enumerate(zip(SLOTS, (job, tool, nf))):
        y = Y0 + 72 + k * 46
        d.t(x + 16, y, slot, 12, SOFT, KR, "start")
        d.t(x + 16, y + 20, val, 13, INK, KR if any("가" <= ch <= "힣" for ch in val) else MONO, "start")
    if i < 2:
        d.arrow([(x + CW + 4, Y0 + CH / 2), (x + CW + GAP - 6, Y0 + CH / 2)], MUTED, "ar", 1.4)

WHYS = ["DB 쿼리가 느림", "페이징 디스크 I/O", "DB 메모리 과다", "할당자 과소비", "메모리 단편화"]
yw, ww, wg = Y0 + CH + 72, 160, 18
d.t(X0, yw - 18, "분석 단계의 Five Whys — 매 칸 다음이 \"왜?\"의 답", 13, MUTED, KR, "start")
for k, w in enumerate(WHYS):
    x = X0 + k * (ww + wg)
    last = k == len(WHYS) - 1
    if last: d.tone(x, yw, ww, 48, INFO, 6)
    else: d.box(x, yw, ww, 48, PAPER2, RULE, 1.0, 6)
    d.t(x + ww / 2, yw + 29, w, 13, INK, KR, "middle", 600 if last else 400)
    if not last:
        d.arrow([(x + ww + 2, yw + 24), (x + ww + wg - 4, yw + 24)], MUTED, "ar", 1.2)

d.legend(yw + 72, [("파고드는 단계", ACC), ("근본 원인", INFO), ("나머지", MUTED)])
d.save("02-02.drill-down-stages.svg")
