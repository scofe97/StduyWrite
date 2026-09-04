# a0-03 §3 SPIFFE ID 의 조각 둘과 그 안의 구조.
# 본문(부록 C.2.1): "A SPIFFE ID is an RFC 3986 compliant URI in the following format:
#       spiffe://trust-domain/path." 변수는 둘이고 path 의 내부 구조는 구현자가 정한다.
#       Istio 는 쿠버네티스 서비스 어카운트를 쓴다.
# 타입 스펙: type-nested — 조각 안에 조각이 든 포함 관계가 논점이다. 바깥에서 안으로 링을 좁히고
#           링 라벨은 왼쪽 위 종이색 마스크 위에 둔다.
#           축약: 규격의 변수는 둘이므로 링도 둘까지만 규격이고, 가장 안쪽은 Istio 의 선택으로 표시한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · A0-03 §3",
      "규격이 정한 변수는 둘뿐이다",
      "spiffe://trust-domain/path 에서 발급자와 워크로드 이름이 갈린다. 그 안쪽 구조는 규격이 열어 "
      "두었고 구현자가 채운다. 색이 붙은 링이 Istio 가 채워 넣은 자리다.",
      "ns/ 와 sa/ 는 세 번째 조각이 아니라 path 의 내부 구조입니다")

def ring(x, y, w, h, tag, sub, stroke, fill, focal=False):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{1.4 if focal else 1.0}"/>')
    tw = int(sum(11 if '가' <= c <= '힣' else 6.9 for c in tag)) + 20
    d.o.append(f'<rect x="{x + 20}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 28, y + 3, tag, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 28, y + 30, sub, 11, ACC if focal else MUTED, KR, "start")

ring(40, 132, 920, 300, "URI · RFC 3986", "spiffe:// 스킴 아래 조각 둘", f"{INK}30", f"{INK}04")
ring(84, 192, 300, 200, "TRUST-DOMAIN", "신원의 발급자 — 개인 또는 조직", INFO, f"{INFO}0E")
ring(432, 192, 484, 200, "PATH", "그 도메인 안에서 워크로드를 가리킨다", MUTED, f"{INK}07")
ring(476, 256, 396, 116, "ISTIO 의 선택 · 서비스 어카운트", "규격이 열어 둔 자리를 이렇게 채운다", ACC, f"{ACC}0E", focal=True)

d.t(120, 336, "cluster.local", 13, INK, MONO, "start", 600)
d.t(512, 320, "ns/istioinaction", 13, INK, MONO, "start", 600)
d.t(512, 344, "sa/catalog", 13, INK, MONO, "start", 600)

d.t(40, 476, "spiffe://cluster.local/ns/istioinaction/sa/catalog", 12, INK, MONO, "start", 600)
d.t(40, 500, "path 가 워크로드를 어떻게 가리킬지는 규격이 정하지 않고 구현하는 쪽이 정한다", 11, SOFT, KR, "start")
d.legend(520, [("구현자가 채우는 자리", ACC), ("발급자를 나타내는 조각", INFO)])
d.save("a0-03.spiffe-id.svg")
