# 02-01 §4 — 존 데이터가 파일에서 주 서버로, 존 전송으로 보조 서버로 흐르는 경로와 그 뒤의 재시작 절차.
# 원문 근거: 존 데이터 파일(= 마스터 파일)에서 읽으면 primary, 존 전송으로 받으면 secondary,
#            전송해 준 쪽이 그 secondary 의 master, secondary 는 backup zone data file 로 디스크에 저장,
#            재시작 시 백업을 먼저 읽고 마스터의 버전과 최신인지 확인해 최신이면 전송이 필요 없다,
#            마스터가 불가용이어도 secondary 는 답할 데이터를 갖고 있다, 둘 다 authoritative.
# 타입 스펙: type-swimlane — 두 주체를 가로지르며 넘겨받는 절차이고, 레인을 건너는 존 전송이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 940, 528
d = D(W, H, "LEARNING COREDNS · 02-01 §4",
      "존 데이터가 파일에서 두 서버로 퍼지는 길",
      "주 서버는 존 데이터 파일에서 존을 읽고, 보조 서버는 그 서버에서 존 전송으로 받는다. "
      "레인을 건너는 화살표가 존 전송이며, 이 한 번의 전달이 보조 서버를 권한 있는 서버로 만든다.",
      "두 레인 모두 이 존에 대해 권한을 갖습니다")

LANE_X, LANE_W = 132, 792
for y, nm, sub in [(104, "주 서버", "primary"), (240, "보조 서버", "secondary")]:
    d.line(LANE_X, y + 112, LANE_X + LANE_W, y + 112, RULE, 0.8)
    d.t(20, y + 50, nm, 14, INK, KR, "start", 600)
    d.t(20, y + 70, sub, 12, SOFT, MONO, "start")

def step(x, y, w, nm, sub):
    d.box(x, y, w, 56, PAPER2, RULE, 1.0)
    d.t(x + w / 2, y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 43, sub, 12, MUTED)

step(152, 128, 224, "존 데이터 파일을 읽는다", "master file")
step(444, 128, 224, "존 전체를 들고 답한다", "권한 있는 응답")
step(152, 268, 224, "존을 전송받는다", "이 존에 대한 권한 획득")
step(444, 268, 224, "디스크에 백업으로 저장", "backup zone data file")
step(700, 268, 224, "재시작하면 백업부터", "최신이면 전송 없음")

d.arrow([(376, 156), (436, 156)], MUTED, "ar", 1.4)
d.path("M 556 184 L 556 200 L 264 200 L 264 260", ACC, 1.6, m="acc")
d.t(576, 206, "존 전송", 14, ACC, KR, "start", 600)
d.t(576, 232, "받는 쪽이 secondary, 준 쪽이 그 master", 12, MUTED, KR, "start")
d.arrow([(376, 296), (436, 296)], MUTED, "ar", 1.4)
d.arrow([(668, 296), (692, 296)], MUTED, "ar", 1.4)

d.t(20, 396, "두 서버 모두 이 존에 대해 authoritative — 존 안의 어떤 이름이든 확정적으로 답한다", 14, INK, KR, "start", 600)
d.t(20, 420, "마스터가 불가용이어도 보조 서버는 자기가 가진 존 데이터로 답한다", 13, MUTED, KR, "start")
d.t(20, 442, "캐시를 들고 있는 다른 서버의 답은 최신일 수도 아닐 수도 있다는 점이 이것과 갈린다", 13, MUTED, KR, "start")

d.legend(462, [("레인을 건너는 전달", ACC)])
d.save("02-01.primary-secondary.svg")
