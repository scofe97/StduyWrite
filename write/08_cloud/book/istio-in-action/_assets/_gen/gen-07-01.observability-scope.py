# 07-01 §1 관측 가능성·모니터링·Istio 계측의 포함과 겹침.
# 본문: 저자의 "Monitoring is a subset of observability" 와 "Istio helps with one part of observability:
#       application-level network instrumentation", 그리고 관측 가능성이 요구하는 재료 넷.
# 타입 스펙: type-venn — 집합의 포함·교집합이 논점이다. 원 셋(2~3 권장), 라벨은 원 밖, 교집합 라벨은 겹침 안,
#           focal 은 교집합 한 곳, 중심·반지름은 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 576
d = D(W, H, "ISTIO IN ACTION · 07-01 §1",
      "관측 가능성 안에서 Istio 가 맡는 자리",
      "저자는 모니터링을 관측 가능성의 부분집합으로 두고, Istio 는 관측 가능성의 한 부분인 "
      "애플리케이션 수준 네트워크 계측을 돕는다고 적는다. 색이 붙은 겹침이 저자가 요약에서 짚은 자리다.",
      "모니터링은 아는 나쁜 상태를 봅니다. 관측 가능성은 모르는 실패를 전제합니다")

# 원 — 중심·반지름 모두 4의 배수
BX, BY, BR = 420, 316, 184          # 관측 가능성
MX, MY, MR = 356, 316, 104          # 모니터링 (관측 가능성에 완전히 포함)
IX, IY, IR = 476, 316, 100          # Istio 데이터 플레인 계측

for cx, cy, r, col in ((BX, BY, BR, MUTED), (MX, MY, MR, SOFT), (IX, IY, IR, INK)):
    d.o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}0A" stroke="{col}" stroke-width="1"/>')

# 겹침(focal) — 두 원의 교차 렌즈. 교점은 두 원 방정식으로 산출한다.
dist = IX - MX                                   # 120
a = (dist * dist + MR * MR - IR * IR) / (2 * dist)
xr = MX + a                                      # 419.4
hh = (MR * MR - a * a) ** 0.5                    # 82.4
lens = (f"M {xr:.1f} {MY - hh:.1f} A {MR} {MR} 0 0 1 {xr:.1f} {MY + hh:.1f} "
        f"A {IR} {IR} 0 0 1 {xr:.1f} {MY - hh:.1f} Z")
d.o.append(f'<path d="{lens}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')

# 집합 라벨 — 원 밖, 테두리를 넘지 않는 자리
d.t(BX, 104, "OBSERVABILITY", 8, SOFT, MONO, "middle")
d.t(BX, 122, "관측 가능성", 14, MUTED, KR, "middle", 600)
d.t(264, 168, "모니터링", 13, SOFT, KR, "middle", 600)
d.path("M 292 172 L 292 240 L 326 240", SOFT, 0.8, m="soft")
d.t(700, 162, "Istio 데이터 플레인 계측", 13, INK, KR, "start", 600)
d.t(700, 180, "envoy sidecar", 9, SOFT, MONO, "start")
d.path("M 694 172 L 694 272 L 560 272", INK, 0.8, m="ar")

# 관측 가능성만의 영역 — 저자가 센 나머지 재료
d.t(BX, 172, "앱 자체 계측", 11, MUTED, KR, "middle")
d.t(BX, 192, "신호 수집 인프라와 저장소", 11, MUTED, KR, "middle")
d.t(BX, 212, "데이터를 헤집어 보는 도구", 11, MUTED, KR, "middle")

# 모니터링만의 영역
d.t(312, 300, "아는 나쁜 상태", 12, SOFT, KR, "middle")
d.t(312, 322, "임계를 정해 감시", 12, SOFT, KR, "middle")

# 겹침 라벨
d.t(419, 310, "임계 감시", 12, ACC, KR, "middle", 600)
d.t(419, 330, "메트릭", 12, ACC, KR, "middle", 600)

# Istio 만의 영역
d.t(517, 300, "나중에 더한 축", 12, INK, KR, "middle")
d.t(517, 322, "미리 몰랐던 것", 12, INK, KR, "middle")

d.legend(524, [("저자가 요약에서 짚은 겹침", ACC), ("Istio 가 채우는 부분", INK)])
d.save("07-01.observability-scope.svg")
