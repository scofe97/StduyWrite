# 06-01.sg-vs-nacl — 층도 성격도 다르다
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 556
d = D(W, H, "SECURITY GROUP vs NACL",
      "층도 성격도 다르다 — 연결 장애 때 볼 곳이 갈린다",
      "SG 는 회신을 자동으로 열어 주고 NACL 은 안 열어 준다. 한쪽만 열고 끝냈다가 막히는 사고가 여기서 난다.",
      lead="SG 는 회신을 자동으로 열고, NACL 은 양방향을 따로 열어야 한다")
ddx.band(d, 104, 500, "돌아오는 길을 누가 열어 주느냐가 장애의 성격을 가른다")
ddx.matrix(d, 44,
  [(300, "어디에 붙나"), (320, "규칙 종류"), (292, "돌아오는 길")],
  [([("보안 그룹", "인스턴스·ENI 수준"), ("allow 규칙만", "전 규칙 평가 후 결정"),
     ("stateful", "인바운드 허용이면 회신 자동")], OK),
   ([("NACL", "서브넷 수준"), ("allow 와 deny 둘 다", "낮은 번호부터 첫 매치"),
     ("stateless", "양방향을 따로 열어야")], WARN)],
  hdr_y=224, row_h=96, gap=16, focal_col=2)
d.t(36, 476, "SG 만 보고 끝내면 NACL 의 아웃바운드에서 막힌다 — 장애가 한쪽 방향에서만 나면 "
             "먼저 의심할 곳이 여기다", 12, MUTED, KR, "start")
d.legend(516, [("회신을 열어 준다", OK), ("따로 열어야 한다", WARN)])
d.save("06-01.sg-vs-nacl.svg"); print("ok sg-vs-nacl")
