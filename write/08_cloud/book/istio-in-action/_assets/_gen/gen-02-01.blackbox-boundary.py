# 02-01 §3 프록시가 보는 것과 애플리케이션이 아는 것.
# 본문: 저자는 애플리케이션이 프록시에게 블랙박스라고 적고, 관측은 애플리케이션의 자기 보고가 아니라
#       네트워크에서 실제로 관찰된 동작을 향한다고 못 박는다. 그러나 서비스 *안에서* 추적 메타데이터를
#       이어 주는 일은 애플리케이션의 책임으로 남는다 — 그 자리가 "코드 변경 없이"의 정확한 경계다.
# 타입 스펙: type-venn — 집합의 포함·교집합이 논점이다. 원 둘, 라벨은 원 밖, 교집합 라벨은 겹침 안,
#           초점은 겹치지 않는 쪽 하나(애플리케이션만 아는 인과).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 02-01 §3",
      "코드 변경 없이가 어디까지인가",
      "프록시는 네트워크에서 관찰된 것을 보고, 애플리케이션은 자기가 한 일을 압니다. 둘이 어긋날 때 "
      "진실은 프록시 쪽입니다. 다만 색이 붙은 조각은 프록시가 볼 수 없어 애플리케이션이 넘겨야 합니다.",
      "레질리언스와 상위 메트릭은 정말 코드 변경이 없고, 분산 추적만 협조를 요구합니다")

PX, PY, PR = 388, 316, 176   # 프록시가 보는 것
AX, AY, AR = 612, 316, 176   # 애플리케이션이 아는 것

d.o.append(f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="{INK}08" stroke="{MUTED}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{AX}" cy="{AY}" r="{AR}" fill="{INK}08" stroke="{MUTED}" stroke-width="1.2"/>')

# 겹침 렌즈 — 두 원의 교차로 좌표를 계산한다
dist = AX - PX
a = (dist * dist + PR * PR - AR * AR) / (2 * dist)
xr = PX + a
hh = (PR * PR - a * a) ** 0.5
lens = (f"M {xr:.1f} {PY - hh:.1f} A {PR} {PR} 0 0 1 {xr:.1f} {PY + hh:.1f} "
        f"A {AR} {AR} 0 0 1 {xr:.1f} {PY - hh:.1f} Z")
d.o.append(f'<path d="{lens}" fill="{INK}0E" stroke="{SOFT}" stroke-width="0.8"/>')

d.t(216, 148, "프록시가 보는 것", 13, INK, KR, "middle", 600)
d.t(216, 168, "network observed", 9, MUTED, MONO, "middle")
d.t(784, 148, "애플리케이션이 아는 것", 13, INK, KR, "middle", 600)
d.t(784, 168, "self-reported", 9, MUTED, MONO, "middle")

d.t(284, 292, "요청 수 · 지연", 11, INK, KR, "middle")
d.t(284, 314, "실패 · 재시도", 11, INK, KR, "middle")
d.t(284, 336, "서킷 브레이킹 발생", 11, INK, KR, "middle")
d.t(284, 366, "코드 변경 없이 나온다", 11, SOFT, KR, "middle")

d.t(492, 292, "서비스 사이의", 11, MUTED, KR, "middle")
d.t(492, 312, "스팬과 전파", 11, MUTED, KR, "middle")

d.t(684, 286, "요청 하나가", 11, ACC, KR, "middle")
d.t(684, 308, "안에서 만든 인과", 11, ACC, KR, "middle", 600)
d.t(684, 336, "들어온 헤더를 나가는", 11, MUTED, KR, "middle")
d.t(684, 354, "요청에 넣는 일", 11, MUTED, KR, "middle")
d.o.append(f'<circle cx="{714}" cy="{258}" r="5" fill="{ACC}"/>')

d.t(28, 552, "계측을 아무리 해도 그것은 자기 보고다 — 둘이 어긋나면 프록시 쪽이 실제로 오간 요청이다", 11, SOFT, KR, "start")
d.t(28, 576, "Istio 는 서비스 안에서 무슨 일이 있었는지 알 수 없어 인과를 짝지을 수 없다", 11, MUTED, KR, "start")
d.legend(596, [("프록시가 대신할 수 없는 조각", ACC), ("두 관점이 겹치는 자리", SOFT)])
d.save("02-01.blackbox-boundary.svg")
