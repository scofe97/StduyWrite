# 03-01.netns-wiring-steps — 네 단계마다 바뀌는 veth1 상태 + 기본 경로 함정
# 본문 요구: 배선 단계마다 인터페이스 상태가 어떻게 바뀌는지(재현 값)와, 경로가 없을 때의 실패 메시지
# 타입 스펙: type-flowchart.md — 본선 넷을 한 줄로, 함정은 아래 가지로 뺀다.
#           서브넷 밖 오류가 풀리는 기본 경로 한 줄에 focal.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 604
d = D(W, H, "netns WIRING BY HAND · veth1 STATE",
      "맨손 배선 — 단계마다 바뀌는 veth1 상태와 기본 경로 함정",
      "격리, 안쪽 끝 켜기, 반대쪽 켜기, 기본 경로의 네 단계. 반대쪽을 켜기 전에는 NO-CARRIER 이고, 기본 경로가 없으면 서브넷 밖은 Network is unreachable 이다.",
      lead="양쪽을 켜도 서브넷 밖은 막혀 있다 — 기본 경로를 넣는 마지막 명령에서 풀린다")

ddx.band(d, 104, 532, "새 netns 의 라우팅 테이블은 빈 상태 · 마지막 함정")
CX = ddx.stage_chain(d, 300,
  ["1 격리", "2 한쪽 켜기", "3 양쪽 켜기", "4 기본 경로"],
  [("격리 공간", "ip netns add net1", "route 테이블 비어 있음", None),
   ("안쪽 끝 켜기", "veth1: 주소 + up", "LOWERLAYERDOWN", WARN),
   ("반대쪽 켜기", "br0 연결 + veth0 up", "UP · LOWER_UP", None),
   ("기본 경로", "default via 게이트웨이", "서브넷 밖으로 나감", ACC)],
  ["한쪽만", "양쪽 up", "마지막"])

SKIP = (CX[2], 464)
d.o.append(f'<rect x="{SKIP[0]-140}" y="{SKIP[1]-46}" width="280" height="92" rx="6" '
           f'fill="{BAD}12" stroke="{BAD}" stroke-width="1.4" stroke-dasharray="6 5"/>')
d.t(SKIP[0], SKIP[1] - 14, "길 없음", 13, BAD, KR, "middle", 600)
d.t(SKIP[0], SKIP[1] + 8, "Network is unreachable", 11, MUTED, MONO)
d.t(SKIP[0], SKIP[1] + 28, "서브넷 밖 ping 은 즉시 실패", 11, BAD, KR)
d.path(f"M {CX[2]} {300+58+6} L {CX[2]} {SKIP[1]-46-10}", BAD, 1.4, m="bad", dash="6 5")
d.t(CX[2] + 14, (300 + 58 + SKIP[1] - 46) // 2 + 4, "기본 경로가 없으면", 11, BAD, KR, "start")

# 런타임이 이 명령을 대신 친다는 연결은 본문 §5 도입이 맡는다
d.legend(548, [("오류가 풀리는 한 줄", ACC), ("빠뜨리면 여기", BAD), ("반대쪽이 꺼진 상태", WARN)])
d.save("03-01.netns-wiring-steps.svg")
print("ok netns-wiring-steps")
