# 03-02.cnm-structure — CNM 세 부품과 CNM 이 제공하지 않는 것
# 본문 요구: libnetwork 안의 세 부품 + 밖에 있어야 하는 KV 저장소
# 타입 스펙: type-nested.md 경계 링. '제공하지 않는 것'이 요점이라 링 밖에 두고 focal 을 건다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "CNM · THREE PARTS AND ONE GAP",
      "CNM 세 부품과 CNM 이 제공하지 않는 것",
      "sandbox·endpoint·network 셋은 libnetwork 안에 있다. 여러 호스트를 묶으려면 밖에 KV 저장소를 따로 세워야 한다.",
      lead="세 부품은 안에 있고, 여러 호스트를 묶는 저장소는 밖에서 따로 세워야 한다")

BW, BH = 200, 104
RING = (40, 216, 706, 268)
CTRL, SBOX, EPT, NET = (150, 292), (150, 424), (400, 358), (630, 358)
KV = (866, 358)

def box(cx, cy, t, s, tag, c=None, dash=False, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{ACC}12" '
                   f'stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 5"/>'); tc = ACC
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="{PAPER2}" '
                   f'stroke="{c or RULE}" stroke-width="1.1"{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
        tc = c or INK
    d.t(cx, cy - 20, ddx.fit(t, 13, BW - 18, t), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(s, 11, BW - 16, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in s) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 11, BW - 14, tag), 11, SOFT, KR)

ddx.band(d, 104, 552, "부품 셋으로 한 호스트는 되고, 여러 호스트는 밖의 저장소가 있어야 된다")
rx, ry, rw, rh = RING
d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, rx, ry, "libnetwork — Docker 의 CNM 구현", 11, INFO, off=16)

box(*CTRL, "네트워크 컨트롤러", "Docker engine API", "배선을 지휘")
box(*SBOX, "sandbox", "컨테이너 하나의", "네트워크 스택")
box(*EPT, "endpoint", "sandbox 를 network 에 잇는", "가상 인터페이스", INFO)
box(*NET, "network", "endpoint 의 집합", "global 드라이버가 조율", INFO)
box(*KV, "외부 KV 저장소", "Consul·etcd·Zookeeper", "CNM 이 제공하지 않음", focal=True)

# 왼쪽 두 상자(오른쪽 변 250)와 endpoint(왼쪽 변 300) 사이 통로는 50px 뿐이라
# 꺾는 열을 나눌 자리가 없다. 한 열(275)을 같이 쓰되 도착 행을 336 / 380 으로 갈라
# 세로 구간이 292~336 · 380~424 로 서로 떨어지게 했다.
for a, ey in ((CTRL, 336), (SBOX, 380)):
    d.path(f"M {a[0]+BW//2+6} {a[1]} L 275 {a[1]} L 275 {ey} L {EPT[0]-BW//2-10} {ey}",
           MUTED, 1.4, m="ar")
d.path(f"M {EPT[0]+BW//2+6} {EPT[1]} L {NET[0]-BW//2-10} {NET[1]}", MUTED, 1.4, m="ar")
d.path(f"M {NET[0]+BW//2+6} {NET[1]} L {KV[0]-BW//2-10} {KV[1]}", ACC, 1.6, m="acc", dash="6 5")
d.t(KV[0], KV[1] - BH // 2 - 14, "libkv 의존", 11, ACC, KR)

d.t(36, 524, "여러 호스트를 하나의 오버레이로 묶으려면 Consul 같은 저장소를 따로 세워야 한다 — "
             "그 빈칸이 CNI 와 갈리는 지점 중 하나다", 12, MUTED, KR, "start")
d.legend(568, [("libnetwork 안", INFO), ("CNM 이 제공하지 않는 것", ACC)])
d.save("03-02.cnm-structure.svg")
print("ok cnm-structure")
