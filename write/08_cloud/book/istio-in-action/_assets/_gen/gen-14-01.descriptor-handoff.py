# 14-01 §5 두 설정이 디스크립터 값에서 만난다 — 원문 14.3.1.
# 본문(원문 14.3.1): RLS 설정은 key header_match 와 value no_loyalty / gold_request / silver_request /
#       bronze_request 에 대해 분당 1 / 10 / 5 / 3 을 정한다. 저자가 "우리는 실제 요청 헤더를 직접
#       다루지 않고 요청의 일부로 보내진 속성만 다룬다"고 못 박는다. 어떤 속성을 보낼지는 Envoy 용어로
#       레이트 리밋 액션이고 특정 라우트 설정의 rate_limit 항목으로 지정하는데, Istio 에 아직 그것을 위한
#       API 가 없어 EnvoyFilter 를 쓴다. 첫 액션은 expect_match: false 라 x-loyalty 헤더가 없을 때
#       no_loyalty 를 만든다. 나머지 셋은 exact_match 로 등급 문자열을 본다.
# 타입 스펙: type-data-flow — 값이 칸 사이를 건너간다. 존 3 · 행 4 · 화살표 8,
#           accent 는 두 설정이 같은 문자열로 만나는 열 하나 — 네 상자가 아니라 그 열 전체를
#           한 요소로 읽는다. 값이 여기서 만들어져 저쪽으로 건너가는 것이 이 도식의 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 616
d = D(W, H, "ISTIO IN ACTION · 14-01 §5",
      "서버는 헤더를 모르고 값만 안다",
      "데이터 플레인이 헤더를 디스크립터 값으로 바꿔 보내고, 서버는 그 값에 붙은 한도만 안다. 색이 붙은 "
      "가운데 열이 두 설정이 만나는 유일한 자리이고, 여기가 어긋나면 아무것도 세어지지 않는다.",
      "저자는 실제 요청 헤더를 직접 다루지 않는다고 못 박습니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 11, SOFT, MONO, "start", 600)

AX, AW = 36, 300
BX, BW = 440, 300
CX_, CW = 844, 360
TOP, RH = 152, 84

zone(AX - 8, TOP - 20, AW + 16, 4 * RH + 4, "REQUEST · 클라이언트가 보내는 것")
zone(BX - 8, TOP - 20, BW + 16, 4 * RH + 4, "ENVOYFILTER · 액션이 만드는 값")
zone(CX_ - 8, TOP - 20, CW + 16, 4 * RH + 4, "RLS CONFIG · 서버가 아는 한도")

rows = [
    ("x-loyalty 헤더 없음", "expect_match: false", "no_loyalty", "분당 1 회"),
    ("x-loyalty: bronze", "exact_match: bronze", "bronze_request", "분당 3 회"),
    ("x-loyalty: silver", "exact_match: silver", "silver_request", "분당 5 회"),
    ("x-loyalty: gold", "exact_match: gold", "gold_request", "분당 10 회"),
]
for i, (req, how, val, lim) in enumerate(rows):
    y = TOP + i * RH
    hh = RH - 20
    d.box(AX, y, AW, hh, PAPER2, RULE, 1.0, 6)
    d.t(AX + 16, y + 28, req, 11.5, INK, MONO, "start")
    d.t(AX + 16, y + 48, "헤더를 붙이지 않은 경우" if i == 0 else "등급 문자열을 붙인 경우", 11, MUTED, KR, "start")
    d.o.append(f'<rect x="{BX}" y="{y}" width="{BW}" height="{hh}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(BX + 16, y + 28, val, 12, ACC, MONO, "start", 600)
    d.t(BX + 16, y + 48, how, 9, MUTED, MONO, "start")
    d.box(CX_, y, CW, hh, PAPER2, RULE, 1.0, 6)
    d.t(CX_ + 16, y + 28, lim, 12, INK, KR, "start", 600)
    d.t(CX_ + 16, y + 48, "key: header_match", 9, MUTED, MONO, "start")
    d.path(f"M {AX + AW} {y + hh / 2} H {BX - 2}", INFO, 1.2, m="info")
    d.path(f"M {BX + BW} {y + hh / 2} H {CX_ - 2}", ACC, 1.5, m="acc")

d.t(36, 512, "액션 설정을 EnvoyFilter 로 쓰는 이유 — Istio 에 아직 이것을 위한 API 가 없다", 11, SOFT, KR, "start")
d.t(36, 536, "제한이 안 걸릴 때 점검 셋 — 리소스가 다 적용됐는가 · 서버 로그에 오류가 없는가 · routes 출력에 actions 가 있는가", 11, MUTED, KR, "start")
d.legend(556, [("두 설정이 만나는 유일한 자리", ACC), ("프록시가 헤더에서 읽는 것", INFO)])
d.save("14-01.descriptor-handoff.svg")
