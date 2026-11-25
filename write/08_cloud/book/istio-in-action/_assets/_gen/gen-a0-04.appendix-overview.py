# a0-04 전체 지도 — 누가 여는가(사이드카 / istiod) x 누구를 향해 열려 있는가(다른 서비스 / 사람·도구) + 질의 경로
# 본문 요구(a0-04 「학습 목표」): 사이드카 여덟 포트(§1)와 istiod 여섯 포트(§4)를 두 축의 한 장으로 가르고,
#   도구 -> 에이전트 15004 -> istiod 디버그 엔드포인트(§3·§5)로 닿는 질의 경로 한 건을 얹는다.
# 값 근거: appendix-D.txt L71-108 (사이드카 15020·15021·15053·15001·15006 / 15000·15090·15004·15020),
#   L253-270 (istiod 15010·15012·15014·15017 / 8080·9876), L162-175 (15004 xDS 전달).
# 타입 스펙: type-architecture — 두 행위자(사이드카 · istiod)와 두 대상(서비스 · 사람)의 경계 구역을 나누고
#   직각 화살표로 에이전트 경유 질의 경로를 잇는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 960, 624
d = D(W, H, "ISTIO IN ACTION · A0-04 OVERVIEW",
      "포트 열넷의 두 축과 컨트롤 플레인 질의 경로",
      "사이드카 여덟 포트와 istiod 여섯 포트를 다른 서비스용과 사람·도구용으로 가르고, "
      "도구가 에이전트 15004 를 거쳐 istiod 의 xDS 15012 에 닿는 질의 경로를 함께 보인다. 15020 은 두 구역에 나오는 한 포트라 합은 열넷이다.",
      lead="가로 축은 누구를 향해 열렸는가, 세로 축은 누가 여는가, 칩은 해당 절이며 15020 은 한 포트라 합은 열넷입니다")

d.t(294, 112, "다른 서비스 · 워크로드용", 14, INFO, KR, "middle", 600)
d.t(626, 112, "사람 · 디버그 도구용", 14, INK, KR, "middle", 600)

def row_zone(y, h, name, sub, chip_txt):
    d.o.append(f'<rect x="16" y="{y}" width="928" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(32, y + 36, name, 14, INK, KR, "start", 600)
    d.t(32, y + 58, sub, 13, MUTED, KR, "start")
    d.chip(60, y + 88, chip_txt, SOFT, 11)

row_zone(132, 204, "사이드카", "에이전트 · Envoy", "§1~§3")
row_zone(356, 180, "istiod", "컨트롤 플레인", "§4~§6")

def card(x, y, w, h, title, sec, rows, c=None):
    if c:
        d.tone(x, y, w, h, c, 6, "10", 1.1)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 26, title, 13, c or INK, KR, "start", 600)
    d.chip(x + w - 28, y + 20, sec, c or SOFT, 11)
    for i, (port, desc, hl) in enumerate(rows):
        ry = y + 52 + i * 28
        if hl == "acc":
            d.tone(x + 12, ry - 16, w - 24, 24, ACC, 4, "16", 1.2)
            pc, dc = ACC, INK
        elif hl == "ok":
            d.tone(x + 12, ry - 16, w - 24, 24, OK, 4, "12", 1.0)
            pc, dc = OK, INK
        else:
            pc, dc = (c or INK), MUTED
        d.t(x + 20, ry, port, 13, pc, MONO, "start", 600)
        d.t(x + 84, ry, desc, 13, dc, KR, "start")

# 좌상: 사이드카 x 서비스용 5개
card(152, 144, 284, 180, "워크로드 통신 · 준비 확인 (5)", "§1·§2", [
    ("15020", "메트릭 병합 · 헬스 체크 (겸용)", None),
    ("15021", "준비 확인 (15020 전달)", None),
    ("15053", "로컬 DNS 프록시", None),
    ("15001", "아웃바운드 리디렉션", None),
    ("15006", "인바운드 리디렉션", None),
], c=INFO)

# 우상: 사이드카 x 사람·도구용 4개 (15004 단일 focal)
card(484, 144, 284, 180, "프록시 · 에이전트 조회 (4)", "§1~§3", [
    ("15000", "Envoy 관리 인터페이스", None),
    ("15090", "Envoy 프록시 메트릭", None),
    ("15004", "istiod 디버그 중계 (xDS)", "acc"),
    ("15020", "에이전트 디버그 (겸용)", None),
])

# 좌하: istiod x 서비스용 4개 (15012 OK)
card(152, 368, 284, 156, "컨트롤 플레인 · 웹훅 노출 (4)", "§4", [
    ("15010", "xDS · 인증서 평문 (비권장)", None),
    ("15012", "xDS · 인증서 TLS / mTLS", "ok"),
    ("15014", "컨트롤 플레인 메트릭", None),
    ("15017", "사이드카 주입 · 검증 웹훅", None),
], c=INFO)

# 우하: istiod x 사람·도구용 2개
card(484, 368, 284, 156, "디버그 · 인트로스펙션 (2)", "§4~§6", [
    ("8080", "Pilot 디버그 (운영 비활성)", None),
    ("9876", "ControlZ 웹 (localhost)", None),
])

# 오른쪽 질의 경로 레인 (x=768..936)
d.box(808, 144, 124, 64, PAPER2, RULE, 1.0, 6)
d.t(870, 172, "운영 도구", 13, INK, KR, "middle", 600)
d.t(870, 192, "istioctl · curl", 11, MUTED, MONO, "middle")

# 1. 도구 -> 15004
d.arrow([(808, 188), (788, 188), (788, 252), (770, 252)], ACC, "acc", 1.5)
d.t(804, 228, "1 요청", 13, ACC, KR, "start", 600)

# 2. 15004 -> istiod 15012 (xDS, 두 열 사이 x=460 통로)
d.arrow([(484, 260), (460, 260), (460, 441), (438, 441)], ACC, "acc", 1.6)
d.t(468, 350, "2 xDS 중계", 13, ACC, KR, "start", 600)

# 3. 도구 -> 9876 ControlZ (우측 끝 x=916 통로 — 글자와 겹치지 않음)
d.arrow([(916, 208), (916, 464), (770, 464)], MUTED, "ar", 1.4, "4 3")
d.t(848, 488, "dashboard 9876", 11, MUTED, MONO, "middle")

d.legend(564, [("에이전트 경유 질의 경로", ACC), ("서비스 통신용 포트", INFO), ("mTLS 권장 · 안전 경로", OK), ("port-forward 직접 조회", MUTED)])
d.save("a0-04.appendix-overview.svg")
print("ok a0-04.appendix-overview")
