# 11-03 §1 — 줄어든 것은 저장량이 아니라 퍼지는 넓이다
# 본문이 '저장량 이득이 아니다'를 명시한다. 그래서 총량이 같음을 아래 산문으로 못박고,
# 도식은 전송 단위(오브젝트 하나 vs 조각 하나)의 차이만 보이게 했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 636, "KUBERNETES IN ACTION · 11-03",
      "줄어든 것은 저장량이 아니라 퍼지는 넓이다",
      "watch 는 바뀐 부분만 보내지 않고 오브젝트를 통째로 보낸다. 그래서 오브젝트 크기가 곧 전송 단위가 되고, "
      "파드 하나가 죽고 사는 사소한 사건도 담긴 IP 를 전부 다시 실어 나른다.",
      "파드 100 개 서비스 · 파드 하나가 죽음 · 노드 100 대")

def band(y0, label, corridor, total, total_c, focal):
    ddx.band(d, y0, y0 + 200, label, x=24, w=1152)
    d.box(110, y0 + 56, 340, 106, PAPER, RULE, 0.9, 8)
    d.path(f"M 456 {y0+109} L 672 {y0+109}", MUTED, 1.5, m="ar")
    d.t(564, y0 + 95, corridor, 11, SOFT, KR)
    d.t(564, y0 + 132, "× 100 곳", 10, SOFT, KR)
    ddx.node(d, 800, y0 + 109, "노드 100 대", "각자 받는다", 220, 76)
    if focal:
        ddx.focal_tag(d, 1030, y0 + 109, total, 170)
    else:
        ddx.tag(d, 1030, y0 + 109, total, total_c, 170)

band(100, "Endpoints — 명단이 오브젝트 하나", "오브젝트 통째로", "9,900 IP 분", WARN, False)
d.t(280, 188, "99 개 IP 가 담긴 오브젝트 하나", 12, INK, KR)
d.t(280, 100 + 128, "하나가 바뀌면 전부 다시 실린다", 11, MUTED, KR)

band(328, "EndpointSlice — 20 개씩 다섯 조각", "바뀐 조각만", "1,900 IP 분", None, True)
for cx in (156, 218, 280, 342):
    d.box(cx - 26, 328 + 88, 52, 46, PAPER2, RULE, 1.0, 5)
    d.t(cx, 328 + 116, "20", 13, SOFT, KR)
d.o.append(f'<rect x="{404-26}" y="{328+88}" width="52" height="46" rx="5" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(404, 328 + 116, "19", 13, ACC, KR, "middle", 600)
d.t(280, 328 + 152, "네 조각은 안 바뀌었으니 전송하지 않는다", 11, MUTED, KR)

d.t(24, 556, "총 IP 는 어느 쪽이나 99 개로 같고 최종 상태도 같다. 달라진 것은 변경 하나가 건드리는 범위가 "
             "오브젝트 전체에서 조각 하나로 좁혀졌다는 점이다.", 11, MUTED, KR, "start")
d.legend(580, [("전송량", WARN), ("바뀐 조각", ACC)])
d.save("11-03-endpointslice-blast-radius.svg")
print("ok")
