# 01-02 §8 느린 디스크 — Sumit 이 가설을 하나씩 확인하고 기각하며 원인에 닿은 순서(원서 1.11.1).
# 타입 스펙: type-flowchart — 판단(마름모)마다 예/아니오로 갈리는 진단 논리다.
#           줄기는 위 → 아래, 마름모의 답이 줄기를 잇고, 오른쪽 칩이 그 답의 근거다.
#           축약: 기각된 갈래를 별도 종료 노드로 그리지 않고 근거 칩으로 접었다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 1000
CX, NW, NH, DW, DH = 240, 360, 36, 248, 48
Y0, STRIDE = 112, 68
CHX = 500                               # 근거 칩 시작 x

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02 §8 · SEC 1.11.1",
       "느린 디스크 — 확인하고 기각하며 좁힌 순서",
       "원서 1.11.1 의 사례. 디스크가 느리다는 티켓에서 출발해 USE · iostat · offcputime 으로 디스크가 DB 를 막는 것을 확인하고, 디스크 에러 · 디스크 이상 · DB 부하 증가 · 단편화를 차례로 기각한 뒤 캐시 적중률에서 원인에 닿는다.",
       "마름모가 확인한 질문, 오른쪽 칩이 답의 근거입니다")

STEPS = [   # 종류, 본문, 줄기 다음 칸으로 가는 답, 근거 칩, 강조
    ("start", "티켓 · 디스크가 느리다", None, None, None),
    ("rect", "문제 기술서 · 1초 넘는 쿼리 증가", None, "지난주 시간당 수십 건", None),
    ("rect", "USE · 디스크 80% · CPU·네트워크 낮음", None, "AcmeMon · 1분 간격", None),
    ("dia", "디스크 에러?", "아니오", "/sys 에러 카운터 0", "rej"),
    ("rect", "iostat 1초 · 자주 100% · 포화", None, "지연 증가", None),
    ("dia", "DB 를 막나?", "예", "offcputime · 쿼리 중 FS 읽기 블록", "yes"),
    ("dia", "디스크 자체 이상?", "아니오", "워크로드 특성 · 부하에 맞게 정상", "rej"),
    ("dia", "DB 부하 증가?", "아니오", "쿼리율 일정 · CPU 일정", "rej"),
    ("dia", "FS 단편화?", "아니오", "용량 30%", "rej"),
    ("rect", "cachestat · 캐시 적중 91%", None, "비슷한 서버는 98% 이상", None),
    ("rect", "프로토타입 앱이 캐시 몫을 잠식", None, "메모리 사용 증가", "cause"),
    ("end", "앱 이전 · 느린 쿼리 0", None, None, None),
]

def cy(i): return Y0 + i * STRIDE + 24

for i, (kind, text, ans, chip, tag) in enumerate(STEPS):
    y = cy(i)
    # 줄기 화살표 — 다음 칸으로
    if i < len(STEPS) - 1:
        top = y + (DH / 2 if kind == "dia" else NH / 2)
        nk = STEPS[i + 1][0]
        bot = cy(i + 1) - (DH / 2 if nk == "dia" else NH / 2)
        d.arrow([(CX, top + 2), (CX, bot - 2)], MUTED, "ar", 1.2)
        if ans: d.t(CX + 10, top + 14, ans, 12, OK if ans == "예" else MUTED, KR, "start", 600)
    if kind == "dia":
        pts = f"{CX},{y - DH/2} {CX + DW/2},{y} {CX},{y + DH/2} {CX - DW/2},{y}"
        d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.0"/>')
        d.t(CX, y + 5, text, 13, INK, KR, "middle", 600)
    elif kind in ("start", "end"):
        c = OK if kind == "end" else INK
        if kind == "end": d.tone(CX - NW / 2, y - NH / 2, NW, NH, OK, 18)
        else: d.box(CX - NW / 2, y - NH / 2, NW, NH, PAPER2, MUTED, 1.0, 18)
        d.t(CX, y + 5, text, 13, c, KR, "middle", 600)
    else:
        if tag == "cause": d.tone(CX - NW / 2, y - NH / 2, NW, NH, ACC, 6)
        else: d.box(CX - NW / 2, y - NH / 2, NW, NH, PAPER2, RULE, 1.0, 6)
        d.t(CX, y + 5, text, 13, ACC if tag == "cause" else INK, KR, "middle", 600)
    if chip:
        c = {"rej": SOFT, "yes": INFO}.get(tag, MUTED)
        if tag == "cause": c = ACC
        edge = CX + (DW / 2 if kind == "dia" else NW / 2)
        d.line(edge + 4, y, CHX - 4, y, c, 1.0, "3 4")
        w = 380
        d.box(CHX, y - 14, w, 28, PAPER, c, 1.0, 4)
        pre = "기각 · " if tag == "rej" else ""
        d.t(CHX + 12, y + 5, pre + chip, 12, MUTED if tag != "yes" else INFO, KR, "start")

d.legend(cy(len(STEPS) - 1) + 48, [("원인", ACC), ("확인된 답", INFO), ("기각한 설명", SOFT), ("해결", OK)])
d.save("01-02.case-slow-disks.svg")
