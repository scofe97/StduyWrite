# 02-02 §1 — 네임스페이스의 모든 Pod 에서 나가는 트래픽 중 메타데이터 서버 주소 한 곳만 NetworkPolicy 가 끊는다.
# 근거 문장: "Pods in the namespace a12 should not be able to reach the metadata endpoints anymore."
#           (NetworkPolicy 의 egress 규칙은 ipBlock 0.0.0.0/0 에서 169.254.169.254/32 를 except 로 뺀다)
# 타입 스펙: type-architecture — 신뢰 경계(네임스페이스 / 클러스터 밖)와 그 경계를 넘는 연결이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, BAD, OK, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    """한글이 섞인 라벨은 한글 스택으로 — mono 에 넣으면 자간이 벌어진다(스타일 계약 §타이포그래피)."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


W, H = 880, 440
d = D(W, H, "CKS STUDY GUIDE · 02-02 §1",
      "egress 정책이 메타데이터 서버 한 곳만 끊는다",
      "NAMESPACE a12 의 Pod 에서 나가는 연결 중 0.0.0.0/0 은 허용되고, "
      "NetworkPolicy default-deny-egress-metadata-server 가 169.254.169.254/32 만 except 로 뺀다.",
      "이 정책은 메타데이터 서버로 가는 길만 막고 나머지 주소는 허용합니다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}08" stroke="{RULE}" '
               f'stroke-width="0.9" stroke-dasharray="5 4"/>')
    lw = len(label) * 7.2 + 16
    d.o.append(f'<rect x="{x + 14}" y="{y - 7}" width="{lw}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(x + 22, y + 4, label, 9, SOFT, MONO, "start")


def node(x, y, w, h, lines, tone=None):
    """lines: [(텍스트, 크기, 색, 굵기)] 위에서 아래로. 첫 줄이 제목."""
    if tone:
        d.tone(x, y, w, h, tone)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0)
    cx = x + w / 2
    ys = {2: (28, 52), 3: (26, 50, 70)}[len(lines)] if h >= 90 else (28, 50)
    for (txt, size, col, wt), dy in zip(lines, ys):
        d.t(cx, y + dy, txt, size, col, _kr(txt), "middle", wt)


# 1) 경계 → 2) 연결선 → 3) 노드 (연결선이 노드 뒤로 들어가도록)
zone(24, 100, 548, 260, "NAMESPACE a12")
zone(628, 100, 236, 260, "OUTSIDE CLUSTER")

# Pod → NetworkPolicy (egress)
d.arrow([(220, 235), (290, 235)], MUTED, "ar", 1.5)
d.t(255, 226, "egress", 11, MUTED, MONO)

# NetworkPolicy → 그 밖의 모든 주소 (허용)
d.path("M 550 215 H 576 Q 584 215 584 207 V 175 Q 584 167 592 167 H 656", OK, 1.6, m="ok")
d.t(592, 193, "허용", 12, OK, KR, "start", 600)

# NetworkPolicy → 메타데이터 서버 (차단: 화살촉 대신 ✕)
d.path("M 550 255 H 576 Q 584 255 584 263 V 295 Q 584 303 592 303 H 628", BAD, 1.6, dash="5 4")
d.line(630, 297, 642, 309, BAD, 1.8)
d.line(630, 309, 642, 297, BAD, 1.8)
d.t(592, 287, "차단", 12, BAD, KR, "start", 600)

node(40, 187, 180, 96, [("침해된 Pod", 13, INK, 600), ("podSelector: {}", 11, MUTED, 400)])
node(290, 187, 260, 96, [("NetworkPolicy", 13, INK, 600),
                         ("default-deny-egress-metadata-server", 11, MUTED, 400),
                         ("except 169.254.169.254/32", 11, ACC, 400)], tone=ACC)
node(660, 132, 188, 70, [("그 밖의 모든 주소", 13, INK, 600), ("0.0.0.0/0", 11, MUTED, 400)])
node(660, 268, 188, 70, [("메타데이터 서버", 13, INK, 600), ("169.254.169.254/32", 11, BAD, 400)], tone=BAD)

d.legend(392, [("허용 경로", OK), ("차단 경로", BAD), ("정책 객체", ACC)])
d.save("02-02.metadata-egress.svg")
