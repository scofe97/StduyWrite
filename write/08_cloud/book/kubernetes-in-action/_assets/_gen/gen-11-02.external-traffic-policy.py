# 11-02 §3 — Local 의 대가는 둘, 장치가 푸는 것은 하나
# 설정 셋을 같은 배치로 반복하는 소규모 다중(small multiples). 숫자만 표로 옮기면
# '노드 3 개 vs 파드 3:1:0'이라는 어긋남의 뿌리가 안 보여, 노드 안에 파드를 그려 넣었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1280, 794, "KUBERNETES IN ACTION · 11-02",
      "Local 의 대가는 둘, 장치가 푸는 것은 하나",
      "노드 A 에 파드 3 개, B 에 1 개, C 에 0 개인 클러스터에 요청 100 개가 들어온다. 로드밸런서는 노드 단위로 "
      "공평하지만 노드마다 파드 수가 달라, 파드 단위로는 공평해지지 않는다.",
      "요청 100 개 · 파드 3 : 1 : 0")

def row(y0, label, shares, pods_a, pod_b, pod_b_c, c_note, c_note_c, srcip, srcip_c, ratio, ratio_c):
    ddx.band(d, y0, y0 + 170, label, x=24, w=1232)
    for (x0, w, nm), sh in zip(((110, 360, "노드 A"), (500, 190, "노드 B"), (720, 190, "노드 C")), shares):
        d.box(x0, y0 + 40, w, 110, PAPER, RULE, 0.9, 8)
        d.t(x0 + w // 2, y0 + 62, nm, 11, SOFT, KR)
        d.t(x0 + w // 2, y0 + 80, sh, 10, SOFT, KR)
    for cx, v in zip((190, 290, 390), pods_a):
        ddx.tag(d, cx, y0 + 118, v, OK, 84)
    ddx.tag(d, 595, y0 + 118, pod_b, pod_b_c, 84)
    d.t(815, y0 + 124, c_note, 11, c_note_c, KR)
    d.t(960, y0 + 70, "소스 IP", 10, SOFT, KR, "start")
    d.t(960, y0 + 90, srcip, 11, srcip_c, KR, "start")
    if ratio_c is None:
        ddx.focal_tag(d, 1130, y0 + 128, ratio, 152)
    else:
        ddx.tag(d, 1130, y0 + 128, ratio, ratio_c, 152)

row(110, "externalTrafficPolicy: Cluster  (기본)", ("몫 33", "몫 33", "몫 33"),
    ("25", "25", "25"), "25", OK, "남의 노드 파드로 넘긴다", SOFT,
    "노드 IP 로 위조된다", WARN, "파드마다 균등", OK)
row(296, "externalTrafficPolicy: Local", ("몫 33", "몫 33", "몫 33"),
    ("11", "11", "11"), "33", WARN, "33 개가 유실된다", BAD,
    "클라이언트 IP 가 남는다", OK, "3 배 어긋남", BAD)
row(482, "Local + healthCheckNodePort", ("몫 50", "몫 50", "몫 0"),
    ("16.7", "16.7", "16.7"), "50", ACC, "분배에서 빠진다", OK,
    "클라이언트 IP 가 남는다", OK, "3 배는 그대로", None)

d.t(24, 692, "장치가 푸는 것은 유실뿐이다. 어긋남의 뿌리는 로드밸런서가 노드 단위로 나누는데 "
             "노드마다 파드 수가 다르다는 데 있다.", 11, MUTED, KR, "start")
d.t(24, 714, "노드별 파드 수를 고르게 맞춰야 줄어들고, DaemonSet 이나 topologySpreadConstraints 가 그 수단이다.",
     11, MUTED, KR, "start")
d.legend(738, [("정상 몫", OK), ("주의", WARN), ("잃는다", BAD), ("장치로 안 풀리는 것", ACC)])
d.save("11-02-external-traffic-policy.svg")
print("ok")
