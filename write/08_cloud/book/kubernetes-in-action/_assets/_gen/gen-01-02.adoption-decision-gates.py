# 01-02 §진입 — 네 갈래 판단이 순서대로 좁혀진다
# 본문 근거(01-02.쿠버네티스 도입 판단.md):
#   진입: "네 갈래 판단은 서로 독립적이지 않고 순서대로 좁혀집니다. 위치(§1)를 정하면 관리 주체(§2)
#          선택지가 갈리고, 관리 주체를 정하면 배포판(§3) 선택지가 갈리며, 이 모든 판단에 앞서
#          애초에 쿠버네티스가 필요한지(§4)를 먼저 자문해야 합니다."
#   §4: 모놀리스 하나면 거의 필요 없다 · 5개 미만이면 대체로 좋은 생각이 아니다 · 20개 넘으면 확실히 이득
#   §1: 규정상 사내에서만 돌려야 하면 사실상 유일한 선택지 · 그 경우 직접 관리해야 하는 경우가 많다
#   §2: 커뮤니티에 물으면 거의 예외 없이 "아니오" · GKE·AKS·EKS 등 · "쓰는 것은 관리하는 것보다 열 배 쉽다"
#       · 결정 전 이미 해 본 엔지니어와 상의해야 한다
#   §3: 순정은 최신이지만 안정성·보안 기본값이 약해 튜닝 필요 · 엔터프라이즈(OpenShift·Rancher)는
#       경화된 기본값 + 순정에 없는 오브젝트 타입, 대신 업스트림보다 한두 버전 뒤처진다
# 타입 스펙: type-flowchart.md — 모양이 종류를 진다(타원=시작, 마름모=판정, 사각형=단계, 점=합류).
#   흐름은 위→아래. coral 은 판정 하나에만 — 본문이 "이 모든 판단에 앞서" 라고 못박은 §4 관문에 건다.
#   §3 은 규제로 강제된 직접 관리와 자발적 직접 관리 **양쪽**에 걸리므로 합류점을 둔다.
#   기존 Mermaid(노드 10개)는 §3 을 온프레미스 경로에만 달아 그 합류를 못 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

# 좌표는 stride 하나로만 배치한다 — 관문 간격 132, 모든 값 4의 배수.
CX = 500                      # 관문 열
LX, RX = 160, 840             # 결과 열(좌·우)
GATE = (240, 372, 504)        # D1 · D2 · D3
SELF_Y, MERGE_Y, D4_Y, TERM_Y = 616, 680, 768, 876
BW, BH = 248, 64              # 결과 상자
DX, DY = 140, 48              # 마름모 반폭·반높이
BAND_Y1 = TERM_Y + BH // 2 + 16
LEG_Y = BAND_Y1 + 16
W, H = 1000, LEG_Y + 40

d = D(W, H, "KUBERNETES IN ACTION · 01-02",
      "네 관문이 순서대로 좁힌다",
      "쿠버네티스 도입 판단은 네 갈래가 독립으로 놓인 것이 아니라 순서대로 좁혀지는 관문이다. "
      "가장 앞에 서는 것은 위치도 관리 주체도 아니라 '애초에 필요한가' 다.",
      lead="배포판 판정은 직접 관리하는 두 경로가 모두 지나간다 — 규제로 강제된 쪽과 스스로 고른 쪽")

ddx.band(d, 104, BAND_Y1, "판정을 건너뛰면 뒤 판정의 선택지가 잘못 좁혀진다")


def gate(cy, q, focal=False):
    """마름모 — 판정. focal 은 도식당 한 곳."""
    c = ACC if focal else INFO
    fill = f"{ACC}12" if focal else PAPER2
    sw = 1.4 if focal else 1.1
    d.o.append(f'<path d="M {CX} {cy-DY} L {CX+DX} {cy} L {CX} {cy+DY} L {CX-DX} {cy} Z" '
               f'fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')
    d.t(CX, cy + 4, ddx.fit(q, 12, DX * 1.5, q), 12, c, KR, "middle", 600)


def outcome(cx, cy, t, s, c, w=BW, h=BH):
    """사각형 — 단계·결과."""
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 6, ddx.fit(t, 13, w - 24, t), 13,
        c, MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 10, w - 18, s), 10, SOFT, KR)


# 시작 — 타원
d.o.append(f'<rect x="{CX-124}" y="108" width="248" height="44" rx="22" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
d.t(CX, 136, "쿠버네티스 도입 검토", 13, INK, KR, "middle", 600)
d.path(f"M {CX} 154 L {CX} {GATE[0]-DY-10}", MUTED, 1.5, m="ar")

# §4 — 본문이 "이 모든 판단에 앞서" 라고 못박은 관문. 도식의 focal.
gate(GATE[0], "자동화된 관리가 필요한가?", focal=True)
outcome(RX, GATE[0], "도입 보류", "모놀리스 하나 · 마이크로서비스 5개 미만", BAD)
d.path(f"M {CX+DX+6} {GATE[0]} L {RX-BW//2-10} {GATE[0]}", BAD, 1.6, m="bad")
d.chip((CX + DX + RX - BW // 2) // 2, GATE[0] - 20, "아니다", BAD, 10)
d.t(36, GATE[0] - 6, "마이크로서비스 20개를 넘으면", 10, SOFT, KR, "start")
d.t(36, GATE[0] + 12, "확실히 이득이다", 10, SOFT, KR, "start")

# §1 — 위치
d.path(f"M {CX} {GATE[0]+DY+6} L {CX} {GATE[1]-DY-10}", MUTED, 1.5, m="ar")
gate(GATE[1], "규제상 사내 고정인가?")
outcome(LX, GATE[1], "온프레미스", "규제로 강제 — 직접 관리가 따라온다", WARN)
d.path(f"M {CX-DX-6} {GATE[1]} L {LX+BW//2+10} {GATE[1]}", WARN, 1.6, m="warn")
d.chip((CX - DX + LX + BW // 2) // 2, GATE[1] - 20, "그렇다", WARN, 10)

# §2 — 관리 주체
d.path(f"M {CX} {GATE[1]+DY+6} L {CX} {GATE[2]-DY-10}", MUTED, 1.5, m="ar")
gate(GATE[2], "직접 관리할 여력이 있는가?")
outcome(RX, GATE[2], "매니지드 서비스", "GKE · AKS · EKS — 커뮤니티가 권장한다", OK)
d.path(f"M {CX+DX+6} {GATE[2]} L {RX-BW//2-10} {GATE[2]}", OK, 1.6, m="ok")
d.chip((CX + DX + RX - BW // 2) // 2, GATE[2] - 20, "없다", OK, 10)

outcome(CX, SELF_Y, "직접 관리", "경험자와 먼저 상의한다 — 커뮤니티는 말린다", WARN)
d.path(f"M {CX} {GATE[2]+DY+6} L {CX} {SELF_Y-BH//2-10}", WARN, 1.6, m="warn")
d.chip(CX + 76, (GATE[2] + DY + SELF_Y - BH // 2) // 2, "있다 · 신중히", WARN, 10)

# 합류 — 직접 관리하는 두 경로가 배포판 판정을 함께 지난다
d.o.append(f'<circle cx="{CX}" cy="{MERGE_Y}" r="4" fill="{INK}"/>')
d.path(f"M {CX} {SELF_Y+BH//2} L {CX} {MERGE_Y-6}", MUTED, 1.4)
d.path(f"M {LX} {GATE[1]+BH//2} L {LX} {MERGE_Y} L {CX-8} {MERGE_Y}", WARN, 1.4, m="warn", dash="6 5")

# §3 — 배포판
d.path(f"M {CX} {MERGE_Y+6} L {CX} {D4_Y-DY-10}", MUTED, 1.5, m="ar")
gate(D4_Y, "경화된 기본값이 필요한가?")
outcome(200, TERM_Y, "엔터프라이즈 배포판", "OpenShift · Rancher — 한두 버전 뒤", INFO)
outcome(800, TERM_Y, "순정 오픈소스", "최신이지만 보안 기본값이 약하다 — 튜닝 필요", INFO)
d.path(f"M {CX-DX-6} {D4_Y} L 200 {D4_Y} L 200 {TERM_Y-BH//2-10}", INFO, 1.5, m="info")
d.path(f"M {CX+DX+6} {D4_Y} L 800 {D4_Y} L 800 {TERM_Y-BH//2-10}", INFO, 1.5, m="info")
d.chip(300, D4_Y - 20, "필요하다", INFO, 10)
d.chip(700, D4_Y - 20, "아니다", INFO, 10)

d.legend(LEG_Y, [("먼저 통과할 관문", ACC), ("도입 보류", BAD),
                 ("부담이 큰 길", WARN), ("권장되는 길", OK), ("배포판 선택", INFO)])
d.save("01-02-adoption-decision-gates.svg")
print("ok adoption-decision-gates")
