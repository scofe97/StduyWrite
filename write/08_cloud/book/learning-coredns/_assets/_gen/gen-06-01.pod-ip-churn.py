# 06-01 §3 — 파드 IP 를 클라이언트에 그대로 나눠 주면, 파드가 바뀔 때마다 클라이언트 목록이 낡는다.
# 본문 근거: 이 노트 §3(파드는 뜨고 지고, 다시 만들어질 때마다 새 IP 가 할당된다 · 여럿이면 목록을 계속 고쳐야 한다).
#            주소는 이 노트 frontmatter allow 목록에 있는 원서 예제 주소를 빌려 쓴 설명용 값이다.
# 타입 스펙: type-process — 세 시점이 열로 진행하고, 실제 목록과 클라이언트 목록이 갈라지는 단계가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, KR, MONO

W, H = 880, 430
d = D(W, H, "LEARNING COREDNS · 06-01 §3",
      "파드 IP 를 그대로 나눠 주면 목록이 낡는다",
      "Deployment 의 파드는 죽거나 업그레이드되면 새 IP 로 다시 뜬다. 처음 받은 주소 목록을 들고 있는 클라이언트는 "
      "파드가 하나 바뀌면 셋 중 둘만, 전부 바뀌면 하나도 맞추지 못한다.",
      "주황 칸이 고정된 이름이 필요한 이유입니다")

COLS = [(20, 180, ""), (210, 210, "처음"), (430, 210, "파드 하나 죽음"), (650, 210, "업그레이드 뒤")]
rows = [
    ("실제 파드 IP", ["10.5.88.4", "10.5.88.5", "10.5.88.6"], ["10.5.88.4", "10.5.88.6", "10.5.88.7"],
     ["10.5.105.4", "10.5.105.5", "10.5.105.6"]),
    ("클라이언트 목록", ["10.5.88.4", "10.5.88.5", "10.5.88.6"], ["10.5.88.4", "10.5.88.5", "10.5.88.6"],
     ["10.5.88.4", "10.5.88.5", "10.5.88.6"]),
]
verdict = [("3 / 3", OK), ("2 / 3", WARN), ("0 / 3", BAD)]

for x, w, head in COLS[1:]:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (nm, *cols) in enumerate(rows):
    y = 132 + i * 92
    d.t(20, y + 44, nm, 14, INK, KR, "start", 600)
    for k, ips in enumerate(cols, start=1):
        x, w, _ = COLS[k]
        d.box(x, y, w, 84, PAPER2, RULE, 1.0, 6)
        for j, ip in enumerate(ips):
            stale = (i == 1 and ip not in rows[0][k])
            d.t(x + 14, y + 24 + j * 22, ip, 13, BAD if stale else INK, MONO, "start")

y = 132 + 2 * 92
d.t(20, y + 30, "맞는 주소", 14, INK, KR, "start", 600)
for k, (txt, c) in enumerate(verdict, start=1):
    x, w, _ = COLS[k]
    if k == 3:
        d.tone(x, y, w, 48, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, 48, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, y + 31, txt, 15, c, MONO, "start", 600)

d.t(20, 400, "붉은 주소 · 이미 없는 파드 · 주소는 설명용 예시 값", 12, SOFT, KR, "start")
d.save("06-01.pod-ip-churn.svg")
