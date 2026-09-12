# 05-03 §1 — 같은 요청이 두 설계에서 밟는 정거장.
# 원문 5.5: SDN 의 특징 넷 중 "흐름 기반 전달" 과 "프로그래밍 가능한 제어 평면" — 라우팅 앱 말고
#       "another might perform server load balancing" 이 같은 장비 위에서 돈다.
#       4장 §4.4.3 세 번째 예제가 흐름 표 항목으로 부하 분산을 만드는 자리다.
# 노트의 읽기: 2026-09-10 학습자가 "왜 장비가 병목인가, 스위치도 장비 아닌가" 라고 물어 추가했다.
#       전통 방식의 정거장 다섯은 원문이 그림으로 그린 것이 아니라 그 물음에 답하려고 세운 것이다.
# 타입 스펙: type-swimlane — 레인마다 정거장을 놓고 같은 가로축으로 견준다.
#       축약: 레인이 주체가 아니라 두 설계다. 빈 칸이 곧 사라진 홉이라 레인마다 정거장 수가 다르다.
import sys; sys.path.insert(0, ".")
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, KR, MONO

W, H = 1000, 560
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 05-03 §1",
      "장비를 끼우느냐, 지나던 스위치가 가르느냐",
      "같은 부하 분산을 전통 방식과 SDN 방식으로 했을 때 요청이 밟는 정거장. 전통은 경로에 상자 "
      "하나가 더 끼고, SDN 은 어차피 지나는 스위치가 흐름 표로 그 일을 한다.",
      "스위치는 둘 다 지납니다 — 다른 것은 그 스위치가 무엇을 보느냐입니다")

BW, BH = 144, 60
COL = [48, 232, 416, 600, 784]

def lane(label, y, stops, focal=None):
    d.t(12, y - 14, label, 13, SOFT, KR, "start", 600)
    placed = []
    for i, stop in stops.items():
        x = COL[i]
        hot = focal == i
        d.box(x, y, BW, BH, PAPER2, ACC if hot else RULE, 1.4 if hot else 1.0, 7)
        d.t(x + BW / 2, y + 26, stop[0], 14, ACC if hot else INK, KR, "middle", 600)
        d.t(x + BW / 2, y + 46, stop[1], 12, MUTED, KR)
        placed.append(i)
    for a, b in zip(placed, placed[1:]):
        d.path(f"M {COL[a] + BW} {y + BH / 2} L {COL[b] - 6} {y + BH / 2}",
               OK if b - a > 1 else MUTED, 1.5, m="ok" if b - a > 1 else "ar")

lane("전통 — 경로에 상자 하나가 더 낍니다 · 거치는 자리 다섯", 152,
     {0: ("클라이언트", "요청 하나"), 1: ("스위치", "목적지만 보고 나릅니다"),
      2: ("로드밸런서", "여기서 고릅니다"), 3: ("스위치", "목적지만 보고 나릅니다"),
      4: ("서버", "고른 백엔드")}, focal=2)

d.line(12, 268, W - 12, 268, RULE, 0.9)

lane("SDN — 지나던 스위치가 가릅니다 · 거치는 자리 셋", 316,
     {0: ("클라이언트", "요청 하나"), 1: ("스위치", "흐름 표가 가릅니다"),
      4: ("서버", "표가 고른 백엔드")})

d.t(12, 424, "두 방식 모두 스위치를 지납니다. 갈리는 것은 그 스위치가 무엇을 보느냐입니다.",
    13, MUTED, KR, "start")
d.t(12, 446, "목적지 주소만 보는 장비는 고르는 일을 못 하니, 고르는 상자가 경로에 따로 서야 합니다.",
    13, MUTED, KR, "start")
d.t(12, 468, "헤더 여러 필드로 일치를 걸고 동작으로 헤더를 고칠 수 있으면 그 일이 지나가는 자리에서 끝납니다.",
    13, MUTED, KR, "start")

d.legend(504, [("경로에 새로 낀 상자", ACC), ("사라진 두 홉", OK), ("그대로인 구간", MUTED)])
d.save("05-03.lb-hop-compare.svg")
print("ok 05-03.lb-hop-compare")
