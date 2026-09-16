# 06-01.sg-vs-nacl — 층도 성격도 다르다
# 타입 스펙: type-dp-security-matrix.md — 행이 보안 그룹·NACL, 열이 층과 성격 — 연결 장애 때 볼 곳이 갈린다
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 540
d = D(W, H, "SECURITY GROUP vs NACL",
      "층도 성격도 다르다 — 연결 장애 때 볼 곳이 갈린다",
      "SG 는 회신을 자동으로 열어 주고 NACL 은 안 열어 준다. 한쪽만 열고 끝냈다가 막히는 사고가 여기서 난다.",
      lead="SG 는 회신을 자동으로 열고, NACL 은 양방향을 따로 열어야 한다")
ddx.band(d, 104, 480, "장애의 성격을 가르는 축 · 회신 경로")
ddx.matrix(d, 44,
  [(284, "어디에 붙나"), (304, "규칙 종류"), (292, "돌아오는 길")],
  [([("보안 그룹", "인스턴스·ENI 수준"), ("allow 규칙만", "전 규칙 평가 후 결정"),
     ("stateful", "인바운드 허용이면 회신 자동")], OK),
   ([("NACL", "서브넷 수준"), ("allow 와 deny 둘 다", "낮은 번호부터 첫 매치"),
     ("stateless", "양방향 각각 명시")], WARN)],
  hdr_y=224, row_h=96, gap=16, focal_col=2, sizes=(13, 12))
d.legend(496, [("회신 자동 허용", OK), ("양방향 각각 허용", WARN)])
d.save("06-01.sg-vs-nacl.svg"); print("ok sg-vs-nacl")
