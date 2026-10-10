# 타입 스펙: type-data-flow — 클라이언트 요청 흐름이 Service Traffic Distribution 설정 전후로 존 A·B 백엔드에 분기되는 데이터 흐름. 포커스는 동일 존 집중 구간.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 188-201(curl·echo Pod 목록 및 IP), 줄 211-223(활성화 전: zone-a 43건 vs zone-b 46건 무작위 분산), 줄 234-245(활성화 후: zone-a 728건 집중 vs zone-b 0건 증가), 줄 254-264(zone-b curl-hgg5v: zone-b 962건 집중)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 440
d = D(W, H, "CILIUM UP AND RUNNING · 08-01 §2", "Service Traffic Distribution 활성화 전후 트래픽 흐름",
      "trafficDistribution 설정에 따른 존 A·B 백엔드 선택 분포 실측 비교",
      "설정 전 무작위 분산과 설정 후 로컬 존 백엔드 우선 전달의 실측 요청 분포")

# 상단: 활성화 전 (기본 무작위 분산)
Y1 = 120
d.box(16, Y1 - 24, W - 32, 144, PAPER2, RULE, 0.7, r=6)
d.t(36, Y1 - 6, "활성화 전: 기본 무작위 분산 (교차 존 트래픽 52%)", 12, WARN, KR, "start", 600)
d.t(W - 36, Y1 - 6, "교차 존 네트워크 지연 · 과금 발생", 11, MUTED, KR, "end")

# 클라이언트
d.box(36, Y1 + 14, 190, 68, PAPER, RULE, 0.9)
d.t(131, Y1 + 36, "curl-zr6kt", 12, INK, MONO, "middle", 600)
d.t(131, Y1 + 54, "kind-worker2 · zone-a", 11, MUTED, KR)
d.t(131, Y1 + 70, "10.244.1.132", 11, MUTED, MONO)

# 서비스 VIP
d.box(266, Y1 + 22, 150, 52, PAPER, SOFT, 1.0)
d.t(341, Y1 + 43, "std-service", 12, INK, MONO, "middle", 600)
d.t(341, Y1 + 61, "기본 ClusterIP", 11, MUTED, KR)

d.arrow([(226, Y1 + 48), (266, Y1 + 48)], MUTED, "ar", 1.4)

# 백엔드 분기 전 (직교 라우팅)
d.box(476, Y1 + 4, 190, 42, PAPER, OK, 0.9)
d.t(571, Y1 + 24, "zone-a echo 4대", 12, OK, KR, "middle", 600)
d.t(571, Y1 + 39, "각 7~16회 수신", 11, MUTED, KR)

d.box(476, Y1 + 52, 190, 42, PAPER, WARN, 0.9)
d.t(571, Y1 + 72, "zone-b echo 4대", 12, WARN, KR, "middle", 600)
d.t(571, Y1 + 87, "각 10~13회 수신", 11, MUTED, KR)

# 직교 라우팅: 서비스 -> zone-a 및 zone-b
d.arrow([(416, Y1 + 38), (446, Y1 + 38), (446, Y1 + 25), (476, Y1 + 25)], OK, "ok", 1.4)
d.arrow([(416, Y1 + 58), (446, Y1 + 58), (446, Y1 + 73), (476, Y1 + 73)], WARN, "warn", 1.4)

# 결과 요약
d.box(706, Y1 + 18, 180, 60, PAPER, RULE, 0.7)
d.t(796, Y1 + 42, "8개 Pod 무작위 분산", 12, INK, KR, "middle", 600)
d.t(796, Y1 + 60, "존 경계 넘나듦", 11, WARN, KR)


# 하단: 활성화 후 (PreferSameZone)
Y2 = 276
d.box(16, Y2 - 24, W - 32, 168, PAPER2, RULE, 0.7, r=6)
d.t(36, Y2 - 6, "활성화 후: PreferClose (PreferSameZone 의 옛 별칭)", 12, OK, KR, "start", 600)
d.t(W - 36, Y2 - 6, "동일 존 우선 · 교차 존 감소", 11, OK, KR, "end")

# 클라이언트 2개
d.box(36, Y2 + 10, 190, 50, PAPER, RULE, 0.9)
d.t(131, Y2 + 30, "curl-zr6kt (zone-a)", 12, INK, MONO, "middle", 600)
d.t(131, Y2 + 48, "10.244.1.132", 11, MUTED, MONO)

d.box(36, Y2 + 74, 190, 50, PAPER, RULE, 0.9)
d.t(131, Y2 + 94, "curl-hgg5v (zone-b)", 12, INK, MONO, "middle", 600)
d.t(131, Y2 + 112, "10.244.2.76", 11, MUTED, MONO)

# 서비스 VIP
d.tone(266, Y2 + 38, 150, 56, ACC, r=4, op="14", sw=1.4)
d.t(341, Y2 + 60, "trafficDistribution", 12, ACC, MONO, "middle", 600)
d.t(341, Y2 + 78, "PreferClose (옛 별칭)", 11, INK, MONO)

# 클라이언트 -> 서비스 (직교 라우팅)
d.arrow([(226, Y2 + 35), (246, Y2 + 35), (246, Y2 + 54), (266, Y2 + 54)], MUTED, "ar", 1.4)
d.arrow([(226, Y2 + 99), (246, Y2 + 99), (246, Y2 + 78), (266, Y2 + 78)], MUTED, "ar", 1.4)

# 백엔드 분기 후
d.tone(476, Y2 + 10, 190, 50, OK, r=4, op="12", sw=1.2)
d.t(571, Y2 + 30, "zone-a echo 4대 집중", 12, OK, KR, "middle", 600)
d.t(571, Y2 + 48, "각 179~187회", 11, INK, KR)

d.tone(476, Y2 + 74, 190, 50, OK, r=4, op="12", sw=1.2)
d.t(571, Y2 + 94, "zone-b echo 4대 집중", 12, OK, KR, "middle", 600)
d.t(571, Y2 + 112, "각 223~259회", 11, INK, KR)

# 서비스 -> 백엔드 (직교 라우팅)
d.arrow([(416, Y2 + 54), (446, Y2 + 54), (446, Y2 + 35), (476, Y2 + 35)], OK, "ok", 1.5)
d.arrow([(416, Y2 + 78), (446, Y2 + 78), (446, Y2 + 99), (476, Y2 + 99)], OK, "ok", 1.5)

# 결과 요약
d.box(706, Y2 + 38, 180, 56, PAPER, OK, 0.9)
d.t(796, Y2 + 60, "로컬 존 백엔드가 대부분 수신", 12, OK, KR, "middle", 600)
d.t(796, Y2 + 78, "원격 존은 34~52회·46~49회", 11, MUTED, KR)

d.save("08-01.service-traffic-distribution.svg")
