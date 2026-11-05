# 06-01 §7 — Deployment 는 hostname 이 든 파드 템플릿을 복사하므로 파드 넷이 같은 이름을 받고, SRV 는 한 줄로 합쳐진다.
# 본문 근거: 이 노트 §7 「Deployment 에 붙인 hostname」 — 템플릿 YAML 과 dig 출력(SRV 1줄 · A 4줄).
# 값 근거: 같은 절 dig 출력의 IP 10.5.105.4~7 · 가중치 25 · 대상 이름 myhost.headless.default.svc (지어낸 값 없음).
# 사실 근거: Kubernetes Deployment 문서(".spec.template" 이 파드 템플릿, 복제본은 템플릿을 담는다) ·
#            DNS for Services and Pods 문서의 Pod's hostname and subdomain fields.
# 타입 스펙: type-data-flow — 템플릿(입력) → 파드 넷(변환) → DNS 응답(출력)으로 가로 흐르고, 넷이 한 줄로 모이는 자리가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 440
d = D(W, H, "LEARNING COREDNS · 06-01 §7",
      "템플릿이 이름을 복사한다",
      "파드 템플릿 한 장의 hostname 이 파드 넷에 복사되어 넷이 모두 myhost 라는 같은 이름을 받는다. "
      "그래서 SRV 는 대상 이름이 같은 넷이 한 줄로 합쳐지고, A 레코드는 같은 이름에 IP 만 다른 넷이 남는다.",
      "주황 칸이 같은 이름 넷이 한 줄로 합쳐지는 자리입니다")

# 열 머리
d.t(20, 108, "템플릿", 12, SOFT, KR, "start", 600)
d.t(300, 108, "파드 넷 · IP · 이름표", 12, SOFT, KR, "start", 600)
d.t(648, 108, "DNS 응답", 12, SOFT, KR, "start", 600)

# 템플릿 카드
d.box(20, 182, 200, 120, PAPER2, RULE, 1.0, 6)
d.t(36, 210, "파드 템플릿 한 장", 14, INK, KR, "start", 600)
d.t(36, 244, "hostname: myhost", 12, INK, MONO, "start")
d.t(36, 268, "subdomain: headless", 12, INK, MONO, "start")

# 복사: 템플릿 → 파드 넷 (버스를 거쳐 갈라진다)
PY = [120, 184, 248, 312]            # 파드 상단 y, 높이 52, 간격 12
PC = [y + 26 for y in PY]            # 파드 중심 y
BUS = 252
d.path(f"M 222 242 L {BUS} 242", MUTED, 1.4)
d.line(BUS, PC[0], BUS, PC[-1], MUTED, 1.4)
for c in PC:
    d.path(f"M {BUS} {c} L 298 {c}", MUTED, 1.4, m="ar")
d.t(BUS, 134 - 4, "복사", 12, MUTED, KR)

# 파드 넷
IPS = ["10.5.105.4", "10.5.105.5", "10.5.105.6", "10.5.105.7"]
for y, ip in zip(PY, IPS):
    d.box(300, y, 220, 52, PAPER2, RULE, 1.0, 6)
    d.t(316, y + 31, ip, 13, MUTED, MONO, "start")
    d.t(504, y + 31, "myhost", 13, INK, MONO, "end", 600)

# 파드 넷 → DNS 응답: 넷이 모였다가 둘로 갈린다
MX = 560
for c in PC:
    d.line(520, c, MX, c, MUTED, 1.4)
d.line(MX, PC[0], MX, PC[-1], MUTED, 1.4)
d.line(MX, 242, 600, 242, MUTED, 1.4)
d.path("M 600 242 L 600 178 L 646 178", ACC, 1.6, m="acc")
d.path("M 600 242 L 600 316 L 646 316", MUTED, 1.4, m="ar")

# SRV 한 줄 (focal)
d.tone(648, 130, 252, 96, ACC, 6, "12", 1.4)
d.t(664, 152, "ANSWER", 12, MUTED, MONO, "start")
d.t(664, 178, "SRV 한 줄 · 가중치 25", 14, ACC, KR, "start", 600)
d.t(664, 204, "myhost.headless.default.svc…", 12, MUTED, MONO, "start")

# A 레코드 넷
d.box(648, 258, 252, 116, PAPER2, RULE, 1.0, 6)
d.t(664, 280, "ADDITIONAL", 12, MUTED, MONO, "start")
d.t(664, 306, "A 레코드 넷 · 이름 하나", 14, INK, KR, "start", 600)
d.t(664, 332, "10.5.105.4 · .5 · .6 · .7", 12, MUTED, MONO, "start")
d.t(664, 356, "이름은 같고 IP 만 다름", 12, MUTED, KR, "start")

d.legend(398, [("같은 이름 넷이 한 줄로 합쳐지는 자리", ACC)])
d.save("06-01.template-same-name.svg")
