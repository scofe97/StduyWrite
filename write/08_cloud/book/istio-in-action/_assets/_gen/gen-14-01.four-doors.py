# 14-01 §1 커스텀 Envoy 빌드를 피하는 네 층.
# 본문(원문 14.1.3 이 넷을 나열한다): Istio API 의 EnvoyFilter 로 Envoy HTTP 필터 설정 · 레이트 리밋 서버로
#       콜아웃 · Lua 스크립트를 구현해 Lua HTTP 필터에 싣기 · Wasm 모듈을 구현해 Wasm HTTP 필터에 올리기.
#       원문 14.5.2 가 네이티브 필터의 단점 둘을 정리한다 — 반드시 C++ 이어야 하고, 변경을 새 Envoy
#       바이너리에 정적으로 빌드해야 해서 사실상 Envoy 의 "커스텀" 빌드가 된다. 원문 14.1.2 는 그것을
#       "이 책의 범위 밖" 이라 적는다. 원문 14.1.1 은 Istio 의 proxy 와 Gloo Edge 가 그 길을 갔다고 적는다.
# 타입 스펙: type-pyramid — 층마다 드묾과 손이 드는 정도가 달라지는 위계. 층 4(4~6) · 층 높이 일정 ·
#           너비는 밑에서 위로 선형 감소 · coral 은 꼭대기 한 층에만 · 왼쪽 여백에 방향 축.
#           축은 원문이 실제로 가르는 것으로 둔다 — 앞의 셋은 기본 제공 필터를 설정하는 일이고
#           Wasm 만 새 필터를 만드는 일이다. 빈도는 원문이 말하지 않으므로 축으로 쓰지 않는다.
#           축약: 저자가 범위 밖이라 잘라 낸 "C++ 정적 빌드" 는 이 사다리의 위가 아니라 밖이므로,
#           층으로 그리지 않고 꼭대기 위에 점선 띠로 따로 둔다. 없는 층을 만들지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 14-01 §1",
      "네 층 모두가 커스텀 빌드를 피하려는 우회다",
      "밑의 셋은 이미 있는 필터를 쓰는 일이고 꼭대기만 없는 것을 만드는 일이다. 위로 갈수록 손이 많이 가며, "
      "그 위의 점선은 저자가 이 책의 범위 밖이라 잘라 낸 길이다.",
      "네 층이 얻는 것은 같습니다 — Envoy 를 새로 빌드하지 않아도 된다는 것")

BASE_W, TOP_W, LH, CX, Y0 = 732, 332, 68, 516, 236
layers = [
    ("EnvoyFilter 로 기존 필터를 켠다", "이미 있는 것 · Istio 가 노출하지 않은 자리", "설정만"),
    ("외부 서비스로 판정을 뺀다", "레이트 리밋 · 외부 인가", "서버 하나 더"),
    ("Lua 스크립트를 심는다", "envoy_on_request · httpCall", "코드 한 조각"),
    ("Wasm 으로 필터를 만든다", "언어를 골라 런타임에 올린다", "툴체인 · ABI"),
]
N = len(layers)

def wid(i):  # i=0 이 밑변
    return BASE_W - (BASE_W - TOP_W) * i / N
for i, (name, sub, side) in enumerate(layers):
    y = Y0 + (N - 1 - i) * LH
    wb, wt = wid(i), wid(i + 1)
    focal = (i == N - 1)
    pts = f"{CX - wb / 2} {y + LH} {CX - wt / 2} {y} {CX + wt / 2} {y} {CX + wb / 2} {y + LH}"
    if focal:
        d.o.append(f'<polygon points="{pts}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(CX, y + 30, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(CX, y + 50, sub, 9.5, MUTED, MONO)
    d.t(CX + wb / 2 + 20, y + 40, side, 11, SOFT, KR, "start")

TOPY = Y0 - 56
d.o.append(f'<rect x="{CX - TOP_W / 2}" y="{TOPY}" width="{TOP_W}" height="40" rx="4" '
           f'fill="{INK}04" stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 5"/>')
d.t(CX, TOPY + 18, "C++ 로 써서 정적으로 빌드한다", 12, SOFT, KR, "middle", 600)
d.t(CX, TOPY + 33, "이 책의 범위 밖 — 커스텀 Envoy 빌드가 된다", 11, MUTED, KR)

AX = 140
d.path(f"M {AX} {Y0 + N * LH - 8} L {AX} {Y0 + 8}", MUTED, 1.2, m="ar")
d.t(AX - 16, Y0 + N * LH - 24, "있는 것을 쓴다", 11, SOFT, KR, "end")
d.t(AX - 16, Y0 + 28, "없는 것을 만든다", 11, SOFT, KR, "end")

d.t(28, 540, "저자가 든 확장 예 — 레이트 리미팅 · 외부 인가 연동 · 헤더 조작 · 페이로드를 채우는 콜아웃 · HMAC · 비표준 토큰", 11, SOFT, KR, "start")
d.t(28, 564, "네이티브 필터의 두 단점 — 반드시 C++ 이어야 하고, 변경을 새 Envoy 바이너리에 정적으로 빌드해야 한다", 11, MUTED, KR, "start")
d.legend(584, [("없는 것을 만드는 층", ACC), ("있는 것을 쓰는 층", MUTED)])
d.save("14-01.four-doors.svg")
