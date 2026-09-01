# 05-05 §4 — 저자가 "쉽고 값지다"고 한 성능 예산 검사. PR 을 열면 훅이 빌드해 산출물 크기를 잰다.
# 저자가 적은 단계와 판정만 옮긴다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, PAPER, RULE, KR, MONO

W, H = 1180, 580
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 05-05 §4",
        "PR 을 열면 산출물 크기를 잰다",
        "성능 예산을 문서가 아니라 파이프라인에 둔다. 임계를 넘으면 머지를 막거나 팀에 알린다.",
        "왼쪽이 사람이고 오른쪽 둘이 자동으로 도는 것입니다")

d.lanes([("개발자", "pull request"),
         ("버전 관리 훅", "VCS hook"),
         ("빌드 서비스", "clone · build · measure")], y0=104, lane_w=290)
d.rails(456)
d.msg("개발자", "버전 관리 훅", "open PR", 210, MUTED, sub="평소처럼 PR 을 연다")
d.msg("버전 관리 훅", "빌드 서비스", "trigger", 272, MUTED, sub="훅이 서비스를 부른다")
d.selfmsg("빌드 서비스", "clone & build", 336, MUTED, sub="최종 조각 산출물을 만든다")
d.selfmsg("빌드 서비스", "size > threshold ?", 396, ACC, sub="정해 둔 예산과 견준다")
d.msg("빌드 서비스", "개발자", "block or notify", 452, ACC, "acc",
      sub="머지를 막거나 팀에 알린다")
d.state("개발자", "프로덕션 전에 안다", 496, OK)
d.legend(524, [("예산이 강제되는 자리", ACC), ("그 밖의 단계", MUTED)])
d.save("05-05.budget-hook.svg")
print("h 필요:", 524 + 40, " 실제:", H)
