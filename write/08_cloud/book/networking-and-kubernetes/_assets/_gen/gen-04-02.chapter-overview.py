# 04-02.chapter-overview — 04-02 의 키워드 개념도. 본문 정리의 ### 묶음 넷(명세 · 구현체 · 프록시 · 점검)을 4행 × 3열로 잇는다.
# 본문 요구: 핵심 요약의 "CNI 는 Pod 가 주소를 받아 연결되는 계약이고 kube-proxy 는 서비스 주소를 Pod 주소로 바꾸는 규칙을 깐다"
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자, 화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄의 묶음.
#           focal 은 서비스 주소가 Pod 주소로 바뀌는 DNAT 노드. 2026-11-08 새 ### 배치에 맞춰 다시 그렸다.
import ddx
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 100, 320, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 1000, 664


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-02 OVERVIEW",
      "CNI 가 Pod 를 잇고 kube-proxy 가 서비스 주소를 Pod 주소로 바꿉니다",
      "04-02 의 키워드 개념도. 첫 줄은 CNI 명세 1.1 이 IPAM 에 주소 할당을 맡기고 flat 이나 overlay 로 배선하는 흐름이다. "
      "둘째 줄은 4대 CNI 가 conflist 로 선택되고 Cilium 이 교체 사례가 되는 흐름이다. "
      "셋째 줄은 EndpointSlice 의 명단을 kube-proxy 모드가 읽어 KUBE-SEP 체인의 DNAT 로 서비스 주소를 Pod 주소로 바꾸는 흐름이다. "
      "넷째 줄은 아홉 번 확인에서 Calico 경로를 거쳐 끊긴 자리를 찾는 흐름이다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄의 묶음입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "1F" if c == ACC else "14", 1.6 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, ddx.fit(title, 13, NW - 16, title), 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, ddx.fit(sub, 12, NW - 16, sub), 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, ddx.fit(label, 12, x2 - x1 - 8, label), 12, MUTED, kr(label), "middle", 600)


def wrap(i, label):
    # 오른쪽 끝 노드 아래에서 내려와 왼쪽 끝 노드 위로 들어가는 줄 바꿈 화살표
    xa, xb = nx(2) + NW / 2, nx(0) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    ym = y1 + 32
    d.arrow([(xa, y1 + 2), (xa, ym), (xb, ym), (xb, y2 - 4)], SOFT, "soft", 1.3)
    d.t((xa + xb) / 2, ym - 7, label, 12, MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("명세", "구현체", "프록시", "점검")):
    d.chip(48, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, "CNI 명세 1.1", "연산 여섯 · 환경 변수", INFO)
node(0, 1, "IPAM 위임", "host-local", INFO)
node(0, 2, "flat · overlay", "VXLAN 헤더 50바이트", WARN)
harrow(0, 0, "주소는")
harrow(0, 1, "배선은")
wrap(0, "구현체를 고른다")

node(1, 0, "4대 CNI", "캡슐화 대 라우팅", INFO)
node(1, 1, "conflist", "첫 파일 하나만 읽음", WARN)
node(1, 2, "Cilium", "kube-proxy 대체는 선택", OK)
harrow(1, 0, "설정 파일로")
harrow(1, 1, "교체 사례")
wrap(1, "서비스 쪽으로")

node(2, 0, "EndpointSlice", "백엔드 명단", INFO)
node(2, 1, "프록시 모드", "iptables 기본", WARN)
node(2, 2, "KUBE-SEP · DNAT", "서비스 주소 → Pod 주소", ACC)
harrow(2, 0, "명단을 읽어")
harrow(2, 1, "체인으로")
wrap(2, "예측대로인지 점검")

node(3, 0, "아홉 번 확인", "배선 · 규칙 · 상태 · 경로", OK)
node(3, 1, "Calico 경로", "169.254.1.1 · proxy_arp", OK)
node(3, 2, "끊긴 자리", "컴포넌트를 가림", OK)
harrow(3, 0, "경로 예측")
harrow(3, 1, "증상 대조")

d.legend(600, [("구조·흐름", INFO), ("선택·한계", WARN), ("주소 변환", ACC), ("점검·결과", OK)])
d.save("04-02.chapter-overview.svg")
print("ok 04-02 overview")
