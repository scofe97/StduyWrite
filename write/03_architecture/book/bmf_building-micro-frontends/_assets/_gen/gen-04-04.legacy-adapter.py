# 04-04 §1 — 레거시 애플리케이션을 어댑터 조각으로 감싸는 배치 (원문 Figure 4-6).
# 셸을 오염시키지 않으려고 조각 하나를 어댑터로 세우고, 그 조각이 iframe 을 조종하며 메시지를 이벤트로 옮긴다.
# 타입 스펙: type-architecture — 논리 경계(셸 / 어댑터 / 레거시)로 묶은 구성요소와 그 사이 연결.
#           accent 는 두 세계를 옮겨 주는 단 하나의 상자.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1200
Z_X, Z_W = 40, 1120
ZONES = [("APPLICATION SHELL · 도메인을 모른다", 104, 96),
         ("ADAPTER MICRO-FRONTEND · 새 세계와 옛 세계 사이", 244, 104),
         ("LEGACY IN IFRAME · 손대지 않는다", 392, 96)]
LEGEND_Y = 392 + 96 + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-04 §1",
      "어댑터 조각이 두 세계를 옮겨 준다",
      "셸을 레거시와 직접 잇지 않는다. 가운데 조각이 쿼리 스트링으로 iframe 을 조종하고 돌아온 메시지를 이벤트로 번역한다.",
      "위아래로 오가는 것이 서로 다른 언어입니다")

for label, y, h in ZONES:
    d.o.append(f'<rect x="{Z_X}" y="{y}" width="{Z_W}" height="{h}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{Z_X + 14}" y="{y - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(Z_X + 20, y + 4, label, 8, SOFT, MONO, "start")

def node(x, y, w, h, name, sub, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + 18, y + 28, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 48, sub, 10, MUTED, KR, "start")

node(380, 118, 440, 68, "애플리케이션 셸", "이벤트 이미터와 알림 시스템을 갖는다")
node(380, 258, 440, 76, "어댑터 조각", "iframe 을 조종하고 메시지를 번역한다", focal=True)
node(380, 406, 440, 68, "옛 커스터마이저", "예전 Angular 로 만든 도구")

d.arrow([(540, 186), (540, 258)], INFO, "info", 1.4)
d.t(526, 226, "loadRemote", 8.5, INFO, MONO, "end")
d.arrow([(500, 334), (500, 406)], INFO, "info", 1.4)
d.t(486, 374, "query string", 8.5, INFO, MONO, "end")
d.arrow([(700, 406), (700, 334)], ACC, "acc", 1.4)
d.t(714, 374, "message → event", 8.5, ACC, MONO, "start")
d.arrow([(660, 258), (660, 186)], ACC, "acc", 1.4)
d.t(674, 226, "emit(...)", 8.5, ACC, MONO, "start")

d.t(160, 292, "안티커럽션 계층", 12, ACC, KR, "middle", 600)
d.t(160, 312, "바깥 시스템의 말이", 10, MUTED, KR)
d.t(160, 330, "셸까지 오지 않는다", 10, MUTED, KR)

d.legend(LEGEND_Y, [("두 세계를 옮겨 주는 자리", ACC), ("아래로 내려가는 지시", INFO)])
d.save("04-04.legacy-adapter.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
