# 타입 스펙: type-gantt — conv,tcp 다섯 대화가 시간축 위에 놓인 자리
# 사실 출처: 노트 L293~L304 (io,stat 5칸, conv,tcp 5줄의 Rel Start·Duration), L315 (Duration 4.111640 secs)
# 02-04 §9 — 막대 시작은 Rel Start, 폭은 Duration 이다. 가장 짧은 0.0014초는 140px/초에서 0.2px 라 보이지 않으므로
#           막대 폭은 최소 4px 로 그렸고 정확한 값은 막대 오른쪽 라벨로 적는다(스펙에 없는 축약).
#           focal 은 위쪽 괄호 하나 — 9초를 잡았어도 트래픽 구간은 첫 프레임부터 마지막 프레임까지 4.111640초다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, RULE, KR, MONO

W, H = 880, 524
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-04 §9",
      "1초 간격으로 시작한 다섯 대화",
      "conv,tcp 의 다섯 줄. 연결마다 12프레임 7,430바이트로 같고, 시작 시각이 0 · 1.037 · 2.058 · 3.088 · 4.110초로 1초쯤씩 어긋난다. 각 대화는 0.0014~0.0183초 만에 끝나고, 캡처의 Duration 은 첫 프레임부터 마지막 프레임까지 4.111640초다.",
      "다섯 대화는 모두 12프레임 7,430바이트로 같고 시작만 1초쯤 어긋납니다")

X0, X1, SPAN = 220, 840, 4.4
def X(s): return X0 + s * (X1 - X0) / SPAN

# 괄호 — focal
BY = 132
d.line(X(0), BY, X(4.11164), BY, ACC, 1.6)
d.line(X(0), BY - 6, X(0), BY + 6, ACC, 1.6)
d.line(X(4.11164), BY - 6, X(4.11164), BY + 6, ACC, 1.6)
d.t((X(0) + X(4.11164)) / 2, BY - 12, "Duration 4.111640초 · 첫 프레임부터 마지막 프레임까지", 13, ACC, KR, "middle", 600)

# 시간 눈금
d.line(X0, 164, X1, 164, RULE, 1.0)
for s in range(5):
    d.line(X(s), 164, X(s), 172, RULE, 1.0)
    d.t(X(s), 188, f"{s}", 12, MUTED, MONO)
d.t(24, 188, "첫 프레임 뒤 경과(초)", 12, SOFT, KR, "start")

CONV = [("::1:53094", 0.000000, 0.0183), ("::1:53096", 1.037073, 0.0017),
        ("::1:53098", 2.058556, 0.0064), ("::1:53099", 3.088026, 0.0042),
        ("::1:53100", 4.110289, 0.0014)]
for i, (name, st, du) in enumerate(CONV):
    y = 212 + i * 52
    d.t(24, y + 26, name, 13, INK, MONO, "start", 600)
    w = max(X(du) - X(0), 4)
    d.o.append(f'<rect x="{X(st):.1f}" y="{y + 8}" width="{w:.1f}" height="28" rx="2" fill="{INFO}22" stroke="{INFO}" stroke-width="1.1"/>')
    lab = f"{st:.3f}초 · {du}초"
    if X(st) + w + 10 + len(lab) * 9 > W - 24:         # 오른쪽 끝에 닿으면 막대 왼쪽에 단다
        d.t(X(st) - 10, y + 27, lab, 13, MUTED, MONO, "end")
    else:
        d.t(X(st) + w + 10, y + 27, lab, 13, MUTED, MONO, "start")

d.legend(484, [("대화 하나(시작 · 지속)", INFO), ("트래픽이 있었던 구간", ACC)])
d.save("02-04.conv-timeline.svg")
