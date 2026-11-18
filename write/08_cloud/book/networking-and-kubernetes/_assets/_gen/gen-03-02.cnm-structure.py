# 03-02.cnm-structure — CNM 세 부품이 서로 물리는 모양
# 본문 요구: §3 이 "sandbox 는 컨테이너 하나의 네트워크 스택, endpoint 는 sandbox 를 network 에 잇는
#           연결점, network 는 서로 직접 통신하는 endpoint 의 묶음"이라고 정의한다. 세 정의가 한 그림에서
#           물려야 "한 sandbox 가 여러 network 에 걸칠 수 있고 endpoint 는 한 network 에만 속한다"가 읽힌다.
# 타입 스펙: type-nested.md 경계 링 — sandbox 링 안에 endpoint 가 들어 있고, endpoint 가 링 밖의
#           network 로 내려간다.
# 근거: moby/moby docker-v29.10.0 daemon/libnetwork/docs/design.md 「The Container Network Model」.
# 이력: 2026-11-18 재제작. 옛 판은 컨트롤러 → endpoint → network → 외부 KV 저장소를 한 줄 사슬로 이었는데
#       화살표가 무엇을 나르는지 없었고, KV 저장소는 cnm-driver-split 과 겹쳤다. 설계 문서의 모델 그림
#       (sandbox 셋 · endpoint 넷 · network 둘)로 바꿨다.
# 좌표: sandbox 폭 264, 중심 180 · 500 · 820. network 폭 392, 중심 276 · 724. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 500
SB_Y, SB_H, SB_W = 128, 148, 264
EP_Y, EP_W, EP_H = 228, 108, 44
NET_Y, NET_H, NET_W = 348, 64, 392
SBX = [(180, "컨테이너 A"), (500, "컨테이너 B"), (820, "컨테이너 C")]
NETS = [(276, "network 1", INFO), (724, "network 2", OK)]
# (endpoint 중심 x, 속한 network 번호)
EPS = [(180, 0), (436, 0), (564, 1), (820, 1)]

d = D(W, H, "CNM · SANDBOX, ENDPOINT, NETWORK",
      "sandbox 는 endpoint 를 통해서만 network 에 닿는다",
      "컨테이너 셋의 sandbox 와 그 안의 endpoint 넷, 그리고 network 둘. 가운데 sandbox 는 endpoint 를 둘 가져 "
      "두 network 에 함께 걸치고, endpoint 하나는 network 하나에만 속한다.",
      lead="endpoint 하나는 network 하나에만 속합니다 · sandbox 는 endpoint 를 여럿 가질 수 있습니다")

for cx, name in SBX:
    x = cx - SB_W // 2
    focal = (cx == 500)
    c = ACC if focal else MUTED
    d.o.append(f'<rect x="{x}" y="{SB_Y}" width="{SB_W}" height="{SB_H}" rx="10" '
               f'fill="{c}06" stroke="{c}" stroke-width="{1.4 if focal else 1.1}" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, x, SB_Y, "sandbox", 11, c, off=16)
    d.t(cx, SB_Y + 36, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, SB_Y + 56, "인터페이스 · 라우팅 · DNS", 11, MUTED, KR)

for ex, ni in EPS:
    nc = NETS[ni][2]
    d.box(ex - EP_W // 2, EP_Y - EP_H // 2, EP_W, EP_H, PAPER2, nc, 1.1, 6)
    d.t(ex, EP_Y - 2, "endpoint", 12, nc, MONO, "middle", 600)
    d.t(ex, EP_Y + 14, "veth 한쪽", 11, MUTED, KR)
    d.path(f"M {ex} {EP_Y + EP_H // 2 + 6} L {ex} {NET_Y - 10}", nc, 1.4, m="info" if ni == 0 else "ok")

for cx, name, c in NETS:
    d.box(cx - NET_W // 2, NET_Y, NET_W, NET_H, PAPER2, c, 1.1, 6)
    d.t(cx, NET_Y + 28, name, 13, c, MONO, "middle", 600)
    d.t(cx, NET_Y + 48, "서로 직접 통신하는 endpoint 의 묶음 · 예: 리눅스 브리지", 11, MUTED, KR)

# 구현 예(netns · veth · 브리지)와 컨트롤러 설명은 본문 §3 이 맡는다
d.legend(NET_Y + NET_H + 28, [("두 network 에 걸친 sandbox", ACC), ("network 1 에 속함", INFO),
                              ("network 2 에 속함", OK)])
d.save("03-02.cnm-structure.svg")
print("ok cnm-structure")
