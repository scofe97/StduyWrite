# 04-01 §3 Gateway 가 맡는 층과 VirtualService 가 맡는 층.
# 본문: "L4(전송)·L5(세션) 속성을 L7(애플리케이션) 라우팅에서 떼어 냈다. Gateway 가 L4·L5 를, VirtualService 가 L7 을.
# 색이 붙은 맨 아래 층이 Ingress v1 과 갈라지는 자리 — 80·443 밖의 포트를 여는 일."
# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 층 3(L7·L5·L4), 폭 840/1000, 높이 72, 초점 1층(L4).
#           L6 은 저자가 언급하지 않아 비워 두고 그 사실을 아래 한 줄로 밝힌다(번호 건너뜀 안티패턴 회피).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 448
d = D(W, H, "ISTIO IN ACTION · 04-01 §3",
      "Gateway가 맡는 층과 VirtualService가 맡는 층",
      "OSI 계층으로 쌓은 두 리소스의 책임. 아래 두 층(L4 전송 · L5 세션)은 Gateway 리소스 하나에, 맨 위 L7 은 VirtualService 에 들어간다. "
      "색이 붙은 L4 에서 80·443 밖 포트가 열린다.",
      "원문은 L4·L5 를 Gateway 가, L7 을 VirtualService 가 맡는다고만 쓴다. tls 의 층 배치는 노트의 정리")

X, LW, LH, STRIDE, Y0 = 96, 816, 72, 80, 112     # 오른쪽 묶음 라벨 자리를 남긴다
layers = [
    ("L7", "애플리케이션", "VirtualService", "Host · 경로 매칭 → 목적지 · 재시도 · 타임아웃", False),
    ("L5", "세션 속성", "Gateway · tls", "SIMPLE · MUTUAL · PASSTHROUGH · SNI", False),
    ("L4", "전송", "Gateway · port · protocol", "80 HTTP · 443 HTTPS · 31400 TCP", True),
]
for i, (idx, osi, name, note, focal) in enumerate(layers):
    y = Y0 + i * STRIDE
    if focal:
        d.o.append(f'<rect x="{X}" y="{y}" width="{LW}" height="{LH}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(X, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 1.0, 4)
    d.t(X + 20, y + 42, idx, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(X + 64, y + 42, osi, 12, MUTED, KR, "start")
    d.t(X + 200, y + 44, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(X + LW - 20, y + 43, note, 12, ACC if focal else MUTED, KR, "end")

# 왼쪽 여백 방향 표시 — 요청은 아래(L4)에서 위(L7)로 처리된다
d.path(f"M 64 {Y0 + 3 * STRIDE - 12} V {Y0 + 12}", SOFT, 1.2, m="soft")
d.t(64, Y0 + 3 * STRIDE + 8, "처리 순서", 9, SOFT, MONO)
# 오른쪽은 리소스 묶음 — 아래 두 층이 한 리소스
d.line(X + LW + 16, Y0 + STRIDE + 4, X + LW + 16, Y0 + 3 * STRIDE - 12, MUTED, 1.2)
d.t(X + LW + 24, Y0 + 2 * STRIDE, "Gateway", 9, MUTED, MONO, "start")
d.t(X + LW + 24, Y0 + 2 * STRIDE + 12, "리소스", 9, MUTED, MONO, "start")

d.t(X, Y0 + 3 * STRIDE + 28, "L6 표현 계층은 저자가 언급하지 않아 비웠고, tls 를 L5 에 둔 것은 노트의 배치입니다", 12, SOFT, KR, "start")
d.legend(404, [("80·443 밖 포트가 열리는 층", ACC)])
d.save("04-01.l4-l7-split.svg")
print("h 필요:", 404 + 22 + 16, " 실제:", H)
