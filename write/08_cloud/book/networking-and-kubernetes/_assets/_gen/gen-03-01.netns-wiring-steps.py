# 03-01.netns-wiring-steps — 네 단계 + 마지막 함정
# 본문 요구: 런타임이 대신해 주는 배선을 손으로 — 네 단계와 마지막 함정(경로 없음)
# 타입 스펙: type-flowchart.md — 본선 넷을 한 줄로, 함정은 아래 가지로 뺀다.
#           마지막에야 ping 이 되는 그 한 걸음에 focal.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 632
d = D(W, H, "netns WIRING BY HAND · FOUR STEPS",
      "런타임이 대신해 주는 배선을 손으로 — 네 단계와 마지막 함정",
      "격리 공간을 만들고 선을 걸고 주소를 줘도 아직 안 된다. 기본 경로를 넣는 마지막 한 줄에서야 ping 이 통한다.",
      lead="주소까지 줘도 안 된다 — 기본 경로를 넣는 마지막 한 줄에서야 통한다")

ddx.band(d, 104, 568, "새 netns 는 라우팅 테이블이 비어 있다 — 그것이 마지막 함정이다")
CX = ddx.stage_chain(d, 300,
  ["①② 격리", "③④ 선 걸기", "⑤~⑨ 주소·브리지", "⑩ 기본 경로"],
  [("격리 공간", "ip netns add net1", "ip_forward=1 선행", None),
   ("선 걸기", "veth0 ↔ veth1", "한쪽만 net1 로", None),
   ("주소·연결", "192.168.1.101/24", "up 해도 NO-CARRIER", None),
   ("기본 경로", "default via .100", "그제야 ping 성공", ACC)],
  ["빈 스택에", "한쪽만", "마지막"])

SKIP = (CX[2], 464)
d.o.append(f'<rect x="{SKIP[0]-140}" y="{SKIP[1]-46}" width="280" height="92" rx="6" '
           f'fill="{BAD}12" stroke="{BAD}" stroke-width="1.4" stroke-dasharray="6 5"/>')
d.t(SKIP[0], SKIP[1] - 14, "길 없음", 13, BAD, KR, "middle", 600)
d.t(SKIP[0], SKIP[1] + 8, "Host Unreachable", 11, MUTED, MONO)
d.t(SKIP[0], SKIP[1] + 28, "새 netns 는 테이블이 빔", 11, BAD, KR)
d.path(f"M {CX[2]} {300+58+6} L {CX[2]} {SKIP[1]-46-10}", BAD, 1.4, m="bad", dash="6 5")
d.t(CX[2] + 14, (300 + 58 + SKIP[1] - 46) // 2 + 4, "경로가 없으면", 11, BAD, KR, "start")

d.t(36, 540, "런타임은 이 열 줄을 대신 쳐 준다 — 손으로 해 보면 CNI 가 무엇을 자동화하는지가 드러난다",
     12, MUTED, KR, "start")
d.legend(584, [("그제야 통하는 한 줄", ACC), ("빠뜨리면 여기", BAD)])
d.save("03-01.netns-wiring-steps.svg")
print("ok netns-wiring-steps")
