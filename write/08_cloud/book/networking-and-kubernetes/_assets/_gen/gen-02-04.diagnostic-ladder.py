# 02-04.diagnostic-ladder — 실패 문구가 가리키는 계층
# 본문 요구: §4 "같은 '안 된다'인데 문구가 다르면 파야 할 곳이 다릅니다." 실측한 세 실패와
#           02-03 에서 세운 사다리를 한 장에 겹친다.
# 타입 스펙: type-layers.md — 가로 띠를 세로로 쌓고, 왼쪽에 index 태그, 가운데에 이름,
#           오른쪽에 보조 라벨. 왼쪽 여백 밖에 방향 표시. focal 은 한 층.
#           ARP 층에 건다 — 실습에서 건너뛰었다가 오타를 못 찾을 뻔한 자리다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER, PAPER2, KR, MONO

W, H = 1000, 640
d = D(W, H, "DIAGNOSTIC LADDER · WHICH RUNG STOPPED",
      "실패 문구가 어느 단에서 멈췄는지 말해 준다",
      "진단은 아래 단부터 올라갑니다. 아래가 깨져 있으면 위는 볼 필요가 없기 때문입니다. "
      "실패 메시지마다 멈춘 단이 다르므로, 문구를 읽으면 다음에 볼 테이블이 정해집니다.",
      lead="아래 단이 깨져 있으면 위 단은 볼 필요가 없다")

X0, WID, RH = 104, 840, 68
TOP = 176
# 아래에서 위로 오르는 순서라, 배열은 위가 마지막 단이다
BANDS = [("L7", "프로토콜 대화", "제대로 답하는가", "curl -v · nc", False),
         ("L4", "연결 수립",     "Connection refused", "ss -tulpn · nc -vz", False),
         ("L3", "도달",          "무응답 후 timeout", "tcpdump · traceroute", False),
         ("L2", "ARP 해결",      "Destination Host Unreachable", "ip neigh", True),
         ("0",  "라우팅 판단",   "Network is unreachable", "ip route · ip route get", False)]

for i, (tag, name, symptom, cmd, focal) in enumerate(BANDS):
    y = TOP + i * RH
    c = ACC if focal else RULE
    d.o.append(f'<rect x="{X0}" y="{y}" width="{WID}" height="{RH}" rx="0" '
               f'fill="{ACC+"12" if focal else (PAPER2 if i % 2 else PAPER)}" '
               f'stroke="{c}" stroke-width="{1.4 if focal else 1.0}"/>')
    d.t(X0 + 20, y + RH // 2 + 4, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(X0 + 76, y + RH // 2 + 5, ddx.fit(name, 15, 180, name), 15,
        ACC if focal else INK, KR, "start", 600)
    d.t(X0 + 268, y + RH // 2 + 5, ddx.fit(symptom, 12, 300, symptom), 12,
        ACC if focal else MUTED, MONO if symptom[0].isupper() else KR, "start")
    d.t(X0 + WID - 20, y + RH // 2 + 4, cmd, 11, SOFT, MONO, "end")

# 방향 표시 — 스택 바깥 왼쪽 여백
BOT = TOP + len(BANDS) * RH
d.path(f"M 72 {BOT-12} L 72 {TOP+12}", MUTED, 1.4, m="ar")
d.t(56, (TOP + BOT) // 2, "진", 11, MUTED, KR, "middle")
d.t(56, (TOP + BOT) // 2 + 14, "단", 11, MUTED, KR, "middle")
d.t(56, (TOP + BOT) // 2 + 28, "순", 11, MUTED, KR, "middle")
d.t(56, (TOP + BOT) // 2 + 42, "서", 11, MUTED, KR, "middle")

d.t(40, BOT + 40, "실습에서 아래 두 단을 연달아 맞았습니다. 라우팅 줄이 없어 한 번, br0 주소를 10.0.1.1 로 "
                  "잘못 적어 ARP 가 실패해 또 한 번입니다.", 12, MUTED, KR, "start")
d.t(40, BOT + 62, "둘 다 '못 간다'는 말이지만 문구가 달랐고, 그래서 볼 테이블도 달랐습니다.",
    12, MUTED, KR, "start")
d.legend(BOT + 78, [("실습에서 건너뛸 뻔한 단", ACC)])
d.save("02-04.diagnostic-ladder.svg")
print("ok diagnostic-ladder")
