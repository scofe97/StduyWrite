# 04-03.networkpolicy-decision — 네 단계 판정 + 차단 가지
# 본문 요구: "정책은 선택되는 순간부터 판정을 시작한다"
# 타입 스펙: type-flowchart.md — 본선 넷 + 매칭 없음 가지. 선택 판정이 첫 관문이라 거기에 focal.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "NetworkPolicy · WHEN IT LOCKS",
      "정책은 선택되는 순간부터 판정을 시작한다",
      "선택되지 않은 Pod 는 아무 제한도 받지 않는다. 선택된 순간 기본값이 차단으로 뒤집히고, 규칙은 허용만 더한다.",
      lead="선택되지 않으면 무제한 · 선택된 순간 기본값이 차단으로 뒤집힌다")

ddx.band(d, 104, 568, "규칙은 막는 게 아니라 예외로 여는 것이다 — 합집합으로 더해진다")
CX = ddx.stage_chain(d, 300,
  ["① 선택 판정", "② 방향 판정", "③ 규칙 대조", "④ 결과"],
  [("선택 판정", "spec.podSelector", "안 걸리면 무제한", ACC),
   ("방향 판정", "policyTypes", "없는 방향은 제한 없음", None),
   ("규칙 대조", "전 정책 합집합", "허용만 더해짐", None),
   ("허용", "규칙이 매칭됨", "예외로 열린 것", OK)],
  ["걸리면", "그 방향", "매칭되면"])

DENY = (700, 470)                                                # 우단을 넘지 않게 안으로
d.o.append(f'<rect x="{DENY[0]-140}" y="{DENY[1]-46}" width="280" height="92" rx="6" '
           f'fill="{BAD}12" stroke="{BAD}" stroke-width="1.4" stroke-dasharray="6 5"/>')
d.t(DENY[0], DENY[1] - 14, "차단", 13, BAD, KR, "middle", 600)
d.t(DENY[0], DENY[1] + 8, "매칭 없음", 11, MUTED, KR)
d.t(DENY[0], DENY[1] + 28, "선택된 순간의 기본값", 11, BAD, KR)
# 드롭 x 가 박스 가로 범위 안에 있으므로 수직으로 내린다 — 옆으로 꺾으면 화살표가 거꾸로 읽힌다
d.path(f"M {CX[2]} {300+58+6} L {CX[2]} {DENY[1]-46-10}", BAD, 1.4, m="bad", dash="6 5")
d.t(CX[2] + 14, 300 + 58 + 30, "매칭 없으면", 11, BAD, KR, "start")

d.t(36, 540, "선택되지 않은 Pod 는 정책이 있든 없든 그대로다 — 그래서 '선택되었는가'가 첫 관문이다",
     12, MUTED, KR, "start")
d.legend(584, [("첫 관문", ACC), ("예외로 열림", OK), ("선택된 순간의 기본값", BAD)])
d.save("04-03.networkpolicy-decision.svg")
print("ok networkpolicy-decision")
