# 03-02.cnm-driver-split — 조율이 필요한가가 드라이버를 가르고, 그 끝에 CNM 이 안 주는 것이 있다
# 본문 요구: §3 이 드라이버를 local·global 로 가르고 "global 은 libkv 라는 키-값 저장소 추상화에
#           의존한다", "CNM 은 저장소를 제공하지 않아 Consul·etcd·Zookeeper 가 필요하다"까지
#           말하는데 산문에만 있다. §5 에서 Kubernetes 가 갈라서는 이유의 절반이 그 의존이다.
#           2026-09-02 사용자 요청 — 이 축을 도식으로.
# 타입 스펙: type-flowchart.md — 판단 한 곳이 두 갈래를 만들고 한쪽만 CNM 경계 밖으로 나간다.
#           같은 문서의 cnm-structure(type-nested)가 세 부품의 구조를 맡으므로 이 장은 갈림만 본다.
#           비교 행렬(type-dp-security-matrix)은 isolation-spectrum 이 이미 쓰고 있어 피했다.
# 좌표: Layout conventions 타입이라 공식이 없다. 가로 stride 236 하나, 갈래 y 오프셋 ±84. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 516
BW, BH, MID = 188, 80, 244
CX = [116, 352, 616, 856]
ARM = 84

d = D(W, H, "CNM DRIVERS · WHERE THE MODEL STOPS",
      "조율이 필요한가 — 그 한 물음이 드라이버를 가른다",
      "libnetwork 의 드라이버가 local 과 global 로 갈리는 판단과 그 뒤의 결과. "
      "global 갈래만 CNM 경계 밖의 키-값 저장소를 요구하며, 그 빈자리가 Kubernetes 가 갈라서는 지점이다.",
      lead="CNM 은 저장소 인터페이스만 정하고 저장소 자체는 주지 않습니다")


def box(cx, cy, t, sub, tag, c=None, focal=False, w=None):
    w = w or BW
    x, y = cx - w // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, w, BH, PAPER2, c or RULE, 1.1, 6)
        tc = c or INK
    d.t(cx, cy - 18, ddx.fit(t, 13, w - 18, t), 13, tc,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(sub, 11, w - 16, sub), 11, MUTED, KR)
    d.t(cx, cy + 22, ddx.fit(tag, 11, w - 14, tag), 11, c or SOFT,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in tag) else KR)


# CNM 경계 — global 갈래만 이 밖으로 나간다
d.o.append(f'<rect x="24" y="104" width="712" height="288" rx="10" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, 24, 104, "CNM · libnetwork 가 제공하는 범위", 11, INFO, off=16)

box(CX[0], MID, "네트워크를 만든다", "docker network create", "드라이버를 고른다", INFO)
box(CX[1], MID, "노드 간 조율이 필요한가", "옆 노드의 대역을 알아야 하나", "이 물음이 가른다", WARN, w=220)

d.path(f"M {CX[0]+BW//2+8} {MID} L {CX[1]-BW//2-10} {MID}", MUTED, 1.5, m="ar")

BR = CX[1] + BW // 2 + 36
d.path(f"M {CX[1]+BW//2+8} {MID} L {BR} {MID}", MUTED, 1.5)
d.path(f"M {BR} {MID} L {BR} {MID-ARM} L {CX[2]-BW//2-10} {MID-ARM}", OK, 1.5, m="ok")
d.path(f"M {BR} {MID} L {BR} {MID+ARM} L {CX[2]-BW//2-10} {MID+ARM}", BAD, 1.5, m="bad")
# 갈래 라벨은 세로 구간 위에 중앙 정렬로 — 왼쪽 상자(…462)와 오른쪽 상자(522…) 사이 통로에만 든다
d.t(BR, MID - ARM - 16, "아니오", 11, OK, KR, "middle")
d.t(BR, MID + ARM + 24, "예", 11, BAD, KR, "middle")

box(CX[2], MID - ARM, "local 드라이버", "bridge · host · none", "한 호스트에서 끝난다", OK)
box(CX[2], MID + ARM, "global 드라이버", "overlay", "libkv 추상화에 기댄다", BAD)

d.path(f"M {CX[2]+BW//2+8} {MID+ARM} L {CX[3]-BW//2-10} {MID+ARM}", ACC, 1.6, m="acc")
box(CX[3], MID + ARM, "키-값 저장소", "Consul · etcd · Zookeeper", "CNM 이 주지 않는다", focal=True)
d.t(CX[3], MID - ARM, "밖에서 가져올 것이 없다", 12, OK, KR)

d.t(24, 436, "오버레이 하나를 쓰려고 분산 저장소를 따로 세워 운영해야 한다는 뜻입니다. "
             "이미 etcd 로 도는 Kubernetes 에게는 순수한 중복이었습니다.", 12, MUTED, KR, "start")
d.legend(460, [("CNM 밖에서 가져올 것", ACC), ("자족한다", OK), ("밖을 요구한다", BAD),
               ("가르는 물음", WARN), ("CNM 경계 안", INFO)])
d.save("03-02.cnm-driver-split.svg")
print("ok cnm-driver-split")
