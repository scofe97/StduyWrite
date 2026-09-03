# 08-01 §4 추적 설정이 놓이는 자리.
# 본문: 저자는 "전역 메시 · 네임스페이스 · 특정 워크로드" 세 수준을 들지만, 그가 드는 두 손잡이
#       (MeshConfig · proxy.istio.io/config)로는 가운데 층을 만들 수 없다. 그 층은 Telemetry API 에만 있다.
#       그래서 가운데 층은 점선 + 흐린 채움으로 두어 "저자의 손잡이에는 없는 자리"임을 드러낸다.
# 타입 스펙: type-layers — 위아래로 쌓인 적용 범위. 층 3, 층 높이 72, 폭 880/1160, 왼쪽 여백에 방향 표시,
#           초점 1층(워크로드 — 이 장의 대부분이 여기에 들어간다).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1160, 520
d = D(W, H, "ISTIO IN ACTION · 08-01 §4",
      "저자가 든 세 수준 중 손잡이가 있는 것은 둘",
      "추적 백엔드 · 샘플링 · 커스텀 태그가 모두 같은 블록에 들어간다. 넣는 자리는 메시 전역 설정과 "
      "워크로드 애노테이션 둘이다. 가운데 네임스페이스 층은 저자가 다루지 않겠다고 한 API 에만 있다.",
      "좁은 쪽이 이기는지는 저자가 적지 않습니다 — 계층 규칙은 Telemetry API 문서에 있습니다")

LX, LW, LH, Y0 = 200, 880, 72, 136
rows = [
    ("MESH", "메시 전역", "MeshConfig · defaultConfig.tracing", "istio-system 의 istio 컨피그맵", "have"),
    ("NS", "네임스페이스", "저자의 두 손잡이에 없다", "Telemetry API 에만 있는 수준", "gap"),
    ("WORKLOAD", "워크로드", "proxy.istio.io/config", "spec.template.metadata.annotations", "focal"),
]
for i, (tag, name, mid, right, kind) in enumerate(rows):
    y = Y0 + i * LH
    if kind == "focal":
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="4" fill="{ACC}10" stroke="{ACC}" stroke-width="1.4"/>')
    elif kind == "gap":
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="4" fill="{INK}04" '
                   f'stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="5 5"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 4)
    c = ACC if kind == "focal" else (SOFT if kind == "gap" else INK)
    d.t(LX + 20, y + 42, tag, 9, SOFT, MONO, "start", 600)
    d.t(LX + 132, y + 42, name, 15, c, KR, "start", 600)
    d.t(LX + 300, y + 42, mid, 11, MUTED if kind != "focal" else ACC, MONO, "start")
    d.t(LX + LW - 20, y + 42, right, 11, MUTED, MONO, "end")

# 방향 표시 — 스택 바깥 왼쪽
d.path(f"M {LX - 44} {Y0 + 8} L {LX - 44} {Y0 + 3 * LH - 8}", MUTED, 1.2, m="ar")
d.t(LX - 60, Y0 + 24, "적용 범위", 11, SOFT, KR, "end")
d.t(LX - 60, Y0 + 3 * LH - 24, "좁아진다", 11, SOFT, KR, "end")

d.t(32, 420, "백엔드 주소 · sampling · customTags 가 전부 이 블록 하나에 들어간다", 11, SOFT, KR, "start")
d.t(32, 444, "설치 시점의 IstioOperator 도 결국 같은 MeshConfig 를 쓰므로 자리는 늘지 않는다", 11, SOFT, KR, "start")
d.legend(476, [("이 장이 주로 쓰는 자리", ACC), ("손잡이가 없는 층", MUTED)])
d.save("08-01.config-layers.svg")
