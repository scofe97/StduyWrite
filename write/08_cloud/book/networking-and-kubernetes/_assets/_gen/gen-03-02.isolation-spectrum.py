# 03-02.isolation-spectrum — 일곱 모드를 격리 눈금 위에 줄 세운다
# 본문 요구: "한쪽 끝이 아무것도 연결하지 않는 None, 반대쪽 끝이 격리를 통째로 내주는 Host"
#           — 두 극단만 본문이 못박았으므로 그 둘만 축의 끝에 두고, 나머지 다섯은 순서를
#           지어내지 않고 가운데 구간에 표의 거래 문구 그대로 나열한다.
# 타입 스펙: type-dp-security-matrix.md — 한 행 세 구간(None · 사이 다섯 · Host) 대조 + 위에 격리 눈금 축.
#           카탈로그에 1차원 스펙트럼 타입이 없어 행 대조로 축약했다
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 552
d = D(W, H, "DOCKER NETWORK MODES · ISOLATION SCALE",
      "일곱 모드는 격리를 얼마나 포기하는가의 눈금 위에 있다",
      "None 이 아무것도 연결하지 않는 끝이고 Host 가 격리를 통째로 내주는 끝이다. 사이의 다섯은 연결 방식이 갈린다.",
      lead="양 끝만 격리의 정도가 다르고, 사이의 다섯은 어떻게 연결하느냐가 다르다")

BY, BH = 176, 232
d.line(32, 152, 968, 152, RULE, 1.0)
d.t(32, 140, "완전 격리", 12, MUTED, KR, "start")
d.t(968, 140, "격리 포기", 12, ACC, KR, "end")

# 왼쪽 끝
d.box(32, BY, 176, BH, PAPER2, INFO, 1.1, 6)
d.t(120, BY + 44, "None", 14, INFO, MONO, "middle", 600)
for i, ln in enumerate(["네트워킹 비활성화", "네트워크가 필요 없는", "컨테이너용"]):
    d.t(120, BY + 80 + i * 26, ddx.fit(ln, 12, 144, ln), 12, MUTED, KR)

# 가운데 — 순서를 주장하지 않는 구간
ddx.band(d, BY, BY + BH, "그 사이 — 연결 방식이 갈린다", x=232, w=536)
MID = [("Bridge", "기본값 — 사설망에서 돌고 밖으로는 NAT"),
       ("Custom", "용도별 브리지 — 예를 들면 DB 전용"),
       ("Macvlan", "물리망에 직접 매핑 — 대부분의 클라우드가 차단"),
       ("IPvlan", "MAC 은 부모 것을 공유하고 IP 만 분리"),
       ("Overlay", "여러 호스트에 같은 네트워크를 확장")]
for i, (nm, desc) in enumerate(MID):
    y = BY + 52 + i * 36
    d.t(248, y, nm, 12, INFO, MONO, "start", 600)
    d.t(372, y, ddx.fit(desc, 12, 380, desc), 12, MUTED, KR, "start")

# 오른쪽 끝 — 본문이 짚는 극단
d.tone(792, BY, 176, BH, ACC, 6, "12", 1.4)
d.t(880, BY + 44, "Host", 14, ACC, MONO, "middle", 600)
for i, ln in enumerate(["호스트와 IP 를", "네임스페이스째 공유", "포트 관리는", "배포자 몫"]):
    d.t(880, BY + 80 + i * 26, ddx.fit(ln, 12, 144, ln), 12, ACC if i < 2 else MUTED, KR)

d.t(36, 448, "Host 만 격리를 내주는 대신 호스트 네트워크 자원에 직접 닿는다 — 나머지 여섯은 격리를 유지한 채 연결 방식만 고른다",
    12, MUTED, KR, "start")
d.t(36, 474, "Host 모드는 Linux 호스트에서만 동작한다 (책 시점 기준)", 12, WARN, KR, "start")
d.legend(488, [("격리를 유지하는 모드", INFO), ("환경 제약", WARN), ("격리를 내주는 끝", ACC)])
d.save("03-02.isolation-spectrum.svg")
print("ok isolation-spectrum")
