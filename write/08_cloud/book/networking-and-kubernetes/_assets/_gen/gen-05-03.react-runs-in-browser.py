# 05-03.react-runs-in-browser — 정적 파일은 클러스터에, 실행은 브라우저에 있다
# 본문 요구(05-03 §1 "리액트 앱은 클러스터에 있는데 왜 밖에서 들어옵니까"): 클러스터에 있는 것은
#           그 앱의 정적 파일이지 실행이 아니다. 브라우저가 번들을 받아 간 순간 코드는 사용자 쪽에서
#           돌고, 그래서 리액트가 부르는 API 는 클러스터에서 나가는 요청이 아니라 다시 들어오는 요청이다.
#           서버가 대신 부르는 구성(SSR·BFF·Route Handler·rewrite 프록시)만 Pod 사이 통신이다.
# 타입 스펙: type-deployment — "소프트웨어가 어디서 도는가"를 존·노드·아티팩트로 배치한다.
#           존 둘(클러스터 안 · 사용자 브라우저), 노드 셋, 아티팩트 칩 넷, 경로 셋으로 예산 안이다.
#           focal 은 "다시 들어오는" API 호출 하나 — 본문이 짚는 단 하나의 논점이다.
# 이력: 2026-09-16 신설. gen-05-03.request-two-segments.py 하단 띠를 떼어 독립 도식으로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 520
d = D(W, H, "WHERE THE CODE RUNS",
      "정적 파일은 클러스터에, 실행은 브라우저에",
      "리액트 앱의 배치도. 클러스터 안 존에는 정적 파일을 서빙하는 프런트 Pod 와 API 를 받는 백엔드 Pod 가 "
      "있고, 실행되는 번들 JS 는 사용자 브라우저 존에 있다. 브라우저가 부르는 API 가 클러스터 밖에서 "
      "다시 들어오는 요청이라는 것을 초점으로 강조했다. 서버가 대신 부르는 구성만 Pod 사이 통신이다.",
      lead="클러스터에 있는 것은 파일이고, 코드가 도는 자리는 브라우저입니다")

# ── 존 둘. 노드는 ZY+56 에서 시작해 높이 108 이라 아래 76px 이 경로 자리로 남는다
ZY, ZH = 128, 236
d.box(32, ZY, 536, ZH, PAPER2, RULE, 1.0, 8)
d.t(52, ZY + 26, "클러스터 안", 12, SOFT, KR, "start", 600)
d.box(632, ZY, 336, ZH, PAPER2, RULE, 1.0, 8)
d.t(652, ZY + 26, "사용자 브라우저", 12, SOFT, KR, "start", 600)

# ── 노드와 아티팩트 칩
def node(x, y, w, title, sub, chips, c=None, focal=False):
    if focal:
        d.tone(x, y, w, 108, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, w, 108, PAPER, RULE, 1.0, 6)
    d.t(x + 16, y + 28, title, 13, c or INK, KR, "start", 600)
    d.t(x + 16, y + 48, sub, 11, MUTED, KR, "start")
    cx = x + 16
    for txt in chips:
        w_chip = ddx.textw_tight(txt, 11) + 20
        d.box(cx, y + 64, w_chip, 24, PAPER2, MUTED, 0.9, 4)
        d.t(cx + w_chip / 2, y + 80, txt, 11, MUTED, MONO if all(ord(ch) < 128 for ch in txt) else KR)
        cx += w_chip + 8

NY, NH = ZY + 56, 108
node(56, NY, 216, "프런트 Pod", "정적 파일 서빙", ["index.html", "bundle.js"])
node(336, NY, 208, "백엔드 Pod", "API 를 받는 자리", ["api"])
node(656, NY, 288, "브라우저 탭", "번들 JS 가 도는 자리", ["실행 중 JS"], c=INFO)

# ── 경로 셋. 전부 직각이고 노드 상자를 가로지르지 않는다
d.arrow([(164, NY), (164, ZY + 44), (800, ZY + 44), (800, NY)], MUTED, "ar", 1.5)
d.t(482, ZY + 36, "GET / · 파일 내려받기", 12, MUTED, KR)

d.arrow([(800, NY + NH), (800, NY + NH + 104), (440, NY + NH + 104), (440, NY + NH)], ACC, "acc", 1.7)
d.t(620, NY + NH + 124, "API 호출 — 클러스터 밖에서 다시 들어옴", 13, ACC, KR)

d.arrow([(272, NY + 54), (336, NY + 54)], INFO, "info", 1.5)
d.t(304, NY + 42, "Pod 사이", 11, INFO, KR)

d.legend(H - 52, [("다시 들어오는 요청", ACC), ("브라우저에서 도는 것", INFO), ("그 밖의 걸음", MUTED)])
d.save("05-03.react-runs-in-browser.svg")
print("ok react-runs-in-browser")
