# 04-01 §1 진입점 앞의 두 장치 — 가상 IP 와 가상 호스팅.
# 본문 요구: 단일 인스턴스 IP 에 DNS 를 직접 매핑하면 인스턴스 장애 때 오류가 이어진다.
#           가상 IP 를 리버스 프록시에 묶고, 호스트 여럿을 프로토콜별 단서(Host · :authority · SNI)로 가른다.
# 값 근거: 04-01 §1 및 ch04.txt 4.1.1~4.1.2 (api.istioinaction.io, prod.istioinaction.io, Host, :authority, SNI).
# 타입 스펙: type-architecture — 문제(직접 매핑)와 해결(가상 IP + 가상 호스팅) 경계를 나누고 직교 화살표로 연결.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, BAD, KR, MONO

W, H = 920, 520

d = D(W, H, "ARCHITECTURE · 04-01 §1",
      "가상 IP로 장애를 가리고 가상 호스팅으로 서비스를 나눈다",
      "직접 인스턴스 IP 매핑은 인스턴스가 죽으면 DNS 갱신 전까지 오류가 이어진다. "
      "도메인 여럿을 하나의 가상 IP와 리버스 프록시로 받고, 프로토콜별 호스트 단서로 각 서비스 풀에 분산한다.",
      lead="위쪽은 직접 IP 매핑이 깨지는 장면(빨강), 아래쪽은 가상 IP(코랄)와 가상 호스팅(초록) 대응입니다.")

# 상단 존: 안티패턴 — 단일 인스턴스 IP 직접 매핑
d.o.append(f'<rect x="24" y="96" width="848" height="116" rx="8" fill="rgba(240,97,109,0.04)" stroke="{BAD}" stroke-width="0.9" stroke-dasharray="4 3"/>')
d.t(38, 114, "AVOID · DIRECT INSTANCE IP", 8, BAD, MONO, "start")

d.tone(44, 130, 200, 66, INFO, 6, "14", 1.1)
d.t(144, 156, "api.istioinaction.io", 13, INK, MONO, "middle", 600)
d.t(144, 178, "DNS가 인스턴스 IP 응답", 13, MUTED, KR, "middle")

d.tone(332, 130, 212, 66, BAD, 6, "14", 1.1)
d.t(438, 156, "단일 서비스 인스턴스", 14, BAD, KR, "middle", 600)
d.t(438, 178, "인스턴스 장애 → 즉시 오류", 13, MUTED, KR, "middle")

d.tone(632, 130, 220, 66, BAD, 6, "14", 1.1)
d.t(742, 156, "운영자 수동 DNS 변경", 14, BAD, KR, "middle", 600)
d.t(742, 178, "전파 지연 · 가용성 저하", 13, MUTED, KR, "middle")

d.arrow([(244, 163), (330, 163)], BAD, "bad", 1.4)
d.t(287, 153, "직접 묶음", 13, BAD, KR, "middle")
d.arrow([(544, 163), (630, 163)], BAD, "bad", 1.4)
d.t(587, 153, "복구 대기", 13, BAD, KR, "middle")

# 하단 존: 해결 — 가상 IP + 리버스 프록시 + 가상 호스팅
d.o.append(f'<rect x="24" y="232" width="848" height="224" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9"/>')
d.t(38, 250, "SOLUTION · VIP + VIRTUAL HOSTING", 8, OK, MONO, "start")

# 도메인 둘
d.tone(44, 272, 200, 68, INFO, 6, "14", 1.1)
d.t(144, 298, "api.istioinaction.io", 13, INK, MONO, "middle", 600)
d.t(144, 320, "같은 가상 IP로 풀이", 13, MUTED, KR, "middle")

d.tone(44, 370, 200, 68, INFO, 6, "14", 1.1)
d.t(144, 396, "prod.istioinaction.io", 13, INK, MONO, "middle", 600)
d.t(144, 418, "같은 가상 IP로 풀이", 13, MUTED, KR, "middle")

# 가운데: 가상 IP + 리버스 프록시 (코랄 focal)
d.tone(332, 286, 220, 136, ACC, 6, "1e", 1.4)
d.t(442, 316, "가상 IP · 리버스 프록시", 15, ACC, KR, "middle", 700)
d.t(442, 340, "부하 분산 · 교체 은닉", 13, INK, KR, "middle")
d.t(442, 366, "HTTP/1.1 → Host 헤더", 13, MUTED, KR, "middle")
d.t(442, 386, "HTTP/2 → :authority", 13, MUTED, KR, "middle")
d.t(442, 406, "TCP+TLS → SNI", 13, MUTED, KR, "middle")

# 오른쪽: 서비스 인스턴스 풀 둘
d.tone(640, 272, 212, 68, OK, 6, "14", 1.1)
d.t(746, 298, "api 인스턴스 풀", 14, OK, KR, "middle", 600)
d.t(746, 320, "다중 인스턴스 · 무중단", 13, MUTED, KR, "middle")

d.tone(640, 370, 212, 68, OK, 6, "14", 1.1)
d.t(746, 396, "prod 인스턴스 풀", 14, OK, KR, "middle", 600)
d.t(746, 418, "다중 인스턴스 · 무중단", 13, MUTED, KR, "middle")

# 화살표 (직교)
d.arrow([(244, 306), (288, 306), (288, 332), (330, 332)], INFO, "info", 1.3)
d.arrow([(244, 404), (288, 404), (288, 376), (330, 376)], INFO, "info", 1.3)
d.t(288, 358, "가상 IP", 13, MUTED, KR, "middle")

d.arrow([(552, 332), (596, 332), (596, 306), (638, 306)], OK, "ok", 1.4)
d.arrow([(552, 376), (596, 376), (596, 404), (638, 404)], OK, "ok", 1.4)
d.t(596, 358, "호스트 분기", 13, OK, KR, "middle", 600)

d.legend(H - 42, [
    ("직접 IP 장애", BAD),
    ("외부 도메인 요청", INFO),
    ("가상 IP · 프록시(핵심)", ACC),
    ("인스턴스 풀 분산", OK),
])
d.save("04-01.vip-virtual-hosting.svg")
print("ok 04-01 vip-virtual-hosting")
