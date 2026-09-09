# 03-03.pod-shares-the-stack — 기본값은 각자 스택, Pod 는 그것을 일부러 깬다
# 본문 요구: §2 표의 마지막 행이 "이 실험의 백미"이고 저자들이 "이것이 왜 안 되는지 아는 것이
#           Kubernetes 이해에 필수"라고 못 박는데, 그 대비가 산문 한 문단으로만 있었다.
#           2026-09-02 사용자 지적 — "쿠버네티스 관련 설명과 도식이 너무 짧다".
# 타입 스펙: type-nested.md 의 경계 링 — 링 하나가 네트워크 네임스페이스 하나다. 왼쪽은 링이 둘,
#           오른쪽은 링이 하나. 링의 개수 차이가 곧 논지라 두 판을 같은 크기로 나란히 둔다.
# 좌표: Layout conventions 타입이라 공식이 없다. 판 폭 464 대칭, 링 높이 224 공통. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 592
PW, PY, RH = 464, 184, 224
LP, RP = 24, 512

d = D(W, H, "ONE STACK EACH · POD BREAKS THAT ON PURPOSE",
      "컨테이너마다 자기 스택 — Pod 는 그것을 일부러 깬다",
      "같은 호스트의 컨테이너 둘과 Pod 안의 컨테이너 둘을 나란히 둔 대조. 링 하나가 네트워크 "
      "네임스페이스 하나이며, 링이 둘이면 localhost 가 서로 다른 세계이고 하나면 같은 세계다.",
      lead="링의 개수가 전부입니다 · localhost 는 언제나 자기 링 안에서만 되돌아옵니다")


def ring(x, w, y, h, label, sub, c, dash="7 6"):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
    d.t(x + 14, y - 12, label, 12, c, KR, "start", 600)
    d.t(x + w - 14, y - 12, sub, 11, SOFT, MONO, "end")


def box(cx, cy, w, h, t, sub, c=None):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 4, ddx.fit(t, 12, w - 16, t), 12, c or INK,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 15, ddx.fit(sub, 11, w - 14, sub), 11, MUTED, KR)


d.t(LP + 8, 152, "기본값 — 컨테이너 둘", 13, INK, KR, "start", 600)
d.t(RP + 8, 152, "Pod — 네임스페이스를 공유한다", 13, ACC, KR, "start", 600)

# 왼쪽 — 링이 둘
for i, (nm, ip, port) in enumerate((("컨테이너 A", "172.17.0.2", "8080 을 잡고 있다"),
                                    ("컨테이너 B", "172.17.0.3", "여기엔 아무도 없다"))):
    x = LP + 16 + i * 220
    ring(x, 204, PY, RH, nm, f"netns #{i+1}", OK)
    box(x + 102, PY + 72, 172, 52, "eth0", ip, INFO)
    box(x + 102, PY + 156, 172, 52, "lo", port, OK)

d.path(f"M {LP+346} {PY+156+34} L {LP+346} {PY+RH+24} L {LP+126} {PY+RH+24} L {LP+126} {PY+156+34}",
       BAD, 1.4, m="bad", dash="5 5")
d.t(LP + 236, PY + RH + 44, "B 가 localhost:8080 을 불러도 A 에 닿지 않는다", 11, BAD, KR)

# 오른쪽 — 링이 하나
ring(RP + 16, 432, PY, RH, "Pod", "netns 하나", ACC, dash="none")
box(RP + 128, PY + 72, 180, 52, "앱 컨테이너", "8080 을 잡고 있다", INFO)
box(RP + 336, PY + 72, 180, 52, "사이드카", "프록시 · 수집기", INFO)
box(RP + 232, PY + 156, 388, 52, "lo", "둘이 같은 것을 본다", ACC)
d.path(f"M {RP+128} {PY+98} L {RP+128} {PY+130}", MUTED, 1.3, m="ar")
d.path(f"M {RP+336} {PY+98} L {RP+336} {PY+130}", MUTED, 1.3, m="ar")
d.t(RP + 232, PY + RH + 24, "localhost:8080 으로 부른다", 11, ACC, KR)

d.t(24, 480, "왼쪽에서 안 되던 그 통신이 오른쪽에서는 됩니다. 컨테이너가 달라진 게 아니라 "
             "네임스페이스를 몇 개 만들었는지가 달라졌을 뿐입니다.", 12, MUTED, KR, "start")
d.t(24, 504, "그래서 사이드카 패턴이 성립합니다. 프록시가 앱을 localhost 로 부를 수 있으니 "
             "앱은 자기가 프록시 뒤에 있다는 사실도 모릅니다.", 12, ACC, KR, "start")
d.legend(528, [("Pod 가 공유하는 것", ACC), ("컨테이너 경계", OK),
               ("인터페이스", INFO), ("닿지 않는 호출", BAD)])
d.save("03-03.pod-shares-the-stack.svg")
print("ok pod-shares-the-stack")
