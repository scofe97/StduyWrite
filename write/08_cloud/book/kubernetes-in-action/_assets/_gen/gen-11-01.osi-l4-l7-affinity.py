# 11-01 §6 — ClientIP 어피니티가 붙잡는 것
# 캡션이 '첫 연결이 고르고 이후 연결이 재사용'이라는 시간 순서를 말한다 → 시퀀스.
# 기록(상태 칩)이 요점이라 그것만 focal. L4/L7 대비는 아래 산문 한 줄로 내린다.
# 타입 스펙: type-sequence.md — 참여자 넷 사이의 시간순 메시지. 어피니티 기록은 레인 옆 칩이 받는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, INFO, OK, WARN, MUTED, SOFT, INK, KR, MONO
import ddx

d = Seq(1120, 714, "KUBERNETES IN ACTION · 11-01",
        "ClientIP 어피니티가 붙잡는 것",
        "첫 연결이 파드를 고르면 출발지 IP와 그 파드의 관계가 기록되고, 같은 IP의 다음 연결이 그 기록을 탄다. "
        "기록의 열쇠가 출발지 IP인 이유는 데이터패스가 그 아래 계층만 읽기 때문이다.",
        "sessionAffinity: ClientIP · 기본 지속 3시간")

ddx.lanes(d, [("클라이언트 파드", "10.244.1.5"),
              ("노드 데이터패스", "kube-proxy 가 심은 규칙"),
              ("파드 A", "10.244.2.9"),
              ("파드 B", "10.244.3.4")], y0=110, lane_w=230)
d.rails(590)

ddx.msg(d, "클라이언트 파드", "노드 데이터패스", "연결 1", 206, INFO, sub="src 10.244.1.5")
ddx.selfmsg(d, "노드 데이터패스", "키 = 출발지 IP", 258, sub="기록이 없어 새로 고른다")
ddx.msg(d, "노드 데이터패스", "파드 A", "ready endpoint 중 하나", 312, OK, mk="ok")
ddx.state(d, "노드 데이터패스", "10.244.1.5 → 파드 A · 3시간", 364, ACC)
ddx.msg(d, "클라이언트 파드", "노드 데이터패스", "연결 2", 416, INFO, sub="같은 출발지 IP")
ddx.selfmsg(d, "노드 데이터패스", "기록 적중", 468, sub="고르는 단계를 건너뛴다")
ddx.msg(d, "노드 데이터패스", "파드 A", "같은 파드로", 518, OK, mk="ok")

x1, x2 = d.LX["노드 데이터패스"], d.LX["파드 B"]
d.path(f"M {x1+10} 570 L {x2-12} 570", WARN, 1.4, m="warn", dash="6 5")
d.t(800, 561, "None 이면 다른 endpoint 로", 11, WARN, KR)

d.t(24, 630, "데이터패스가 읽는 것은 출발지 IP(L3)와 포트(L4)뿐이다. "
             "HTTP 쿠키는 상자 안, 곧 L7 에 있어 이 판단에 쓰이지 않는다.", 11, MUTED, KR, "start")
d.legend(646, [("기록이 잡아 두는 것", ACC), ("어피니티가 걸린 길", OK), ("None 일 때", WARN)])
d.save("11-01-osi-l4-l7-affinity.svg")
print("ok")
