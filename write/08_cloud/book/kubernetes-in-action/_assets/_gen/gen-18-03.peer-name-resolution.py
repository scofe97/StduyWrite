# 18-03 §2 — 이름을 조립할 재료가 이미 손에 있다
# 캡션이 "자기 인덱스와 completions 로 peer 이름을 조립한다"고 한다. 그러니 DNS 조회만
# 그리면 절반이고, 그 이름이 어디서 나왔는지가 함께 있어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 660, "KUBERNETES IN ACTION · 18-03",
      "이름을 조립해 서로를 찾는다",
      "인덱스 Job 의 파드는 자기 번호와 총 개수를 안다. 그 둘로 다른 파드의 이름을 만들 수 있고, "
      "headless Service 의 DNS 가 그 이름을 IP 로 바꿔 준다.",
      "중앙 조율자 없이 서로를 찾는 길")

d.box(60, 176, 320, 200, PAPER, RULE, 0.9, 8)
d.t(220, 204, "파드 0 이 아는 것", 11, SOFT, KR)
for i, (k, v) in enumerate((("JOB_COMPLETION_INDEX", "0 — 나는 0 번"),
                            ("completions", "3 — 전부 셋"))):
    d.t(84, 250 + i * 44, k, 11, INFO, MONO, "start")
    d.t(84, 272 + i * 44, v, 10, MUTED, KR, "start")
d.t(220, 356, "이 둘이면 이름을 만들 수 있다", 10, SOFT, KR)

d.o.append(f'<rect x="{640-180}" y="232" width="360" height="88" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(640, 262, "이름을 조립한다", 13, ACC, KR, "middle", 600)
d.t(640, 288, "job-1-{index}.headless-svc", 10, MUTED, MONO)
d.path("M 384 276 L 454 276", ACC, 1.5, m="acc")

ddx.node(d, 1050, 276, "headless Service DNS", "이름 → 파드 IP", 300, 88, OK)
d.path("M 824 276 L 894 276", OK, 1.5, m="ok")

d.box(60, 412, 1120, 108, PAPER2, RULE, 1.0, 8)
d.t(620, 440, "그래서 파드 0 은 이렇게 만든다", 11, SOFT, KR)
for i, nm in enumerate(("job-1-0.headless-svc  (자기 자신)", "job-1-1.headless-svc", "job-1-2.headless-svc")):
    d.t(300 + i * 320, 480, nm, 11, ACC if i else SOFT, MONO)

d.t(24, 576, "16-01 의 StatefulSet 이 ordinal 로 신원을 준 것과 같은 수다. 다른 점은 그 신원이 "
             "영구적이지 않고 Job 이 도는 동안만 필요하다는 것이다.", 11, MUTED, KR, "start")
d.legend(604, [("파드가 아는 값", INFO), ("조립한 이름", ACC), ("이름을 푸는 곳", OK)])
d.save("18-03-peer-name-resolution.svg")
print("ok")
