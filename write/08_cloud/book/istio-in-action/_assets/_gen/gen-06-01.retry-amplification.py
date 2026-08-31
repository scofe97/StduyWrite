# 06-01 §6 호출 깊이가 다섯일 때 요청이 늘어나는 모양 — 저자의 thundering herd 계산.
# 본문: "호출 사슬이 다섯 단계 깊고 각 단계가 두 번씩 재시도할 수 있으면, 들어온 요청 하나가 사슬 끝에서 32개가 된다."
# 원문 정오는 본문이 병기한다 — 저자 자신의 'attempts: 2 는 최대 3회 전달'과 셈이 어긋난다(3^5 = 243).
# 타입 스펙: type-bar — 범주(호출 단계)별 수치 비교. 막대 6개(4~8), y 축은 0 에서 시작, 초점 막대 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 540
d = D(W, H, "ISTIO IN ACTION · 06-01 §6",
      "호출 깊이가 다섯일 때 요청이 늘어나는 모양",
      "저자의 계산 — 사슬이 다섯 단계 깊고 각 단계가 두 번씩 재시도하면 들어온 요청 하나가 끝에서 32개가 된다. "
      "사슬 끝의 자원이 이미 과부하라면 이 추가 부하가 그 자원을 무너뜨린다.",
      "저자의 셈은 2의 거듭제곱입니다. 자기 설정으로 계산할 때는 (1 + attempts)로 세는 편이 안전합니다")

PL, PR, PT, PB = 80, W - 40, 116, 424
labels = ["들어온 요청", "1단계", "2단계", "3단계", "4단계", "5단계"]
vals = [1, 2, 4, 8, 16, 32]
YMAX, n = 32, len(vals)
pitch = (PR - PL) / n
bw = pitch * 0.62
def Y(v): return PB - v / YMAX * (PB - PT)
for g in range(0, YMAX + 1, 8):
    d.line(PL, Y(g), PR, Y(g), RULE, 1.0 if g == 0 else 0.8)
    d.t(PL - 10, Y(g) + 4, f"{g}", 8, SOFT, MONO, "end")
d.t(PL - 10, PT - 14, "요청 수", 9, SOFT, KR, "end")
d.line(PL, PT, PL, PB, RULE, 0.8)
for i, (lab, v) in enumerate(zip(labels, vals)):
    cx = PL + pitch * (i + 0.5)
    x, y = cx - bw / 2, Y(v)
    focal = (i == n - 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{PB - y}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{PB - y}" rx="4" fill="rgba(139,152,169,0.15)" stroke="{MUTED}" stroke-width="1"/>')
    d.t(cx, y - 10, f"{v}", 9, ACC if focal else MUTED, MONO)
    d.t(cx, PB + 24, lab, 11, ACC if focal else INK, KR, "middle", 600)
d.t((PL + PR) / 2, PB + 48, "저자가 센 요청 수 — 각 단계가 재시도할 때 그 단계에 도착하는 수", 11, SOFT, KR)
d.legend(496, [("사슬 끝에 도착하는 요청", ACC)])
d.save("06-01.retry-amplification.svg")
