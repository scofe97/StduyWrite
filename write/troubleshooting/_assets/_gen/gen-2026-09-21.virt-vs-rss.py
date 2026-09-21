# 개념 노트 「힙 밖에서 쌓이는 메모리」 · 잡아 둔 것과 실제로 올라온 것.
# 논지는 "한도와 비교되는 것은 표시된 양이 아니라 붙은 양"이라 길이로 대조한다.
# 타입 스펙: type-bar — 두 값을 길이로 비교. 위 막대는 테두리만(표시), 아래는 채움(점유).
#           type-treemap 을 검토했으나 부분-전체가 아니라 두 정의의 대조라 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 360
d = D(W, H, "TROUBLESHOOTING CONCEPT · VIRT AND RSS",
      "표시만 해 둔 양과 실제로 붙은 양",
      "프로세스가 주소 공간을 잡아 달라고 하면 커널은 표시만 하고 물리 페이지는 붙이지 않는다. "
      "그 주소에 값을 쓰는 순간 페이지가 붙고 그때부터 RSS 에 들어간다. 컨테이너 한도와 비교되는 것은 아래쪽 값이다.",
      lead="같은 프로세스인데 위는 2.0 GB, 아래는 100 MB 입니다")

X0, BAR_W, SCALE = 264, 600, 300.0        # 1 GB = 300px
d.t(48, 152, "주소 공간에 표시", 13, INK, KR, "start", 600)
d.t(48, 172, "VIRT · VSZ", 12, MUTED, MONO, "start")
d.o.append(f'<rect x="{X0}" y="128" width="{BAR_W}" height="52" rx="4" fill="none" '
           f'stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="5,4"/>')
d.t(X0 + BAR_W - 16, 160, "2.0 GB", 13, MUTED, MONO, "end", 600)

d.t(48, 240, "물리 페이지가 붙음", 13, INK, KR, "start", 600)
d.t(48, 260, "RSS · RES · VmRSS", 12, MUTED, MONO, "start")
d.tone(X0, 216, int(0.1 * SCALE), 52, OK, 4)
d.t(X0 + int(0.1 * SCALE) + 16, 248, "100 MB", 13, OK, MONO, "start", 600)
d.chip(X0 + BAR_W - 96, 248, "한도와 비교되는 쪽", ACC, 12)

d.legend(296, [("표시만 된 자리", MUTED), ("페이지가 붙은 양", OK), ("한도가 보는 값", ACC)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.virt-vs-rss.svg"))
print("ok")
