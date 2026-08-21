# 12-01 §2 — 판단은 목적지를 정하는 자리까지 살아남아야 한다
# 본문의 결론 문장("판단하는 주체와 목적지를 정하는 주체가 갈리면, 판단은 버려집니다")이
# 도식의 형태를 정한다. 같은 판단을 두 경로에 태워 어디서 사라지는지를 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, KR
import ddx

d = D(1160, 656, "KUBERNETES IN ACTION · 12-01",
      "프록시의 판단이 어디까지 살아남는가",
      "프록시가 요청을 파싱해 '이건 카나리로'라고 정했다. 그 판단이 목적지에 그대로 닿는지는 "
      "다음 홉이 그 판단을 읽을 수 있느냐에 달렸다.",
      "카나리로 보내기로 정한 요청 하나")

def route(y0, label, mid, mid_sub, mid_focal, dest, dest_sub, dest_c, verdict, verdict_c, focal_verdict):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1112)
    cy = y0 + 116
    ddx.node(d, 160, cy, "L7 프록시", "카나리로 보낸다", 200, 84, ACC)
    if mid:
        ddx.node(d, 470, cy, mid, mid_sub, 240, 84)
        d.path(f"M 266 {cy} L 344 {cy}", MUTED, 1.5, m="ar")
        d.path(f"M 596 {cy} L 674 {cy}", MUTED, 1.5, m="ar")
        ddx.node(d, 790, cy, dest, dest_sub, 220, 84, dest_c)
    else:
        d.path(f"M 266 {cy} L 674 {cy}", OK, 1.5, m="ok")
        d.t(470, cy - 14, "EndpointSlice 로 이미 아는 주소", 11, OK, KR)
        ddx.node(d, 790, cy, dest, dest_sub, 220, 84, dest_c)
    if focal_verdict:
        ddx.focal_tag(d, 1000, cy, verdict, 180)
    else:
        ddx.tag(d, 1000, cy, verdict, verdict_c, 180)

route(100, "cluster IP 를 거칠 때", "노드 커널", "L4 — 판단을 읽지 못한다", False,
      "아무 파드", "확률로 다시 고른다", BAD, "판단이 버려진다", BAD, False)
route(340, "파드로 직접 보낼 때", None, None, False,
      "카나리 파드", "10.244.3.4:8080", OK, "판단이 닿는다", None, True)

d.t(24, 588, "부하 분산의 주인이 커널에서 프록시로 옮겨 오면 라운드로빈·쿠키 어피니티·재시도·정밀 카나리가 "
             "함께 따라온다. 파드 개수로 비율을 맞출 필요도 없어진다.", 11, MUTED, KR, "start")
d.legend(608, [("프록시의 판단", ACC), ("닿는 길", OK), ("끊기는 지점", BAD)])
d.save("12-01-proxy-to-pod-direct.svg")
print("ok")
