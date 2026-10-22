# 타입 스펙: type-flowchart — 열 가지 리스크를 "컨테이너 고유 수단이 있는가"로 가르면 셋은 막다른 길(코드 검토)이고 일곱은 앞 장의 수단이 붙는다. focal 은 알려진 취약점 컴포넌트의 이미지 스캐너.
# 사실 출처: 노트 L40~L124(막다른 길 셋·고유 수단 여섯), L126~L150(로깅·모니터링 → 13장), L154~L164(이미지 스캔 결론)
# Layout conventions: 오른쪽 일곱 행 stride 60(y=108+60i), 위험 상자 w=212·수단 상자 w=372·h=48, 왼쪽 열 중심 x=140. 마름모 예는 오른쪽·아니오는 아래. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 648
d = D(W, H, "CONTAINER SECURITY · 14-01 §1·§2·§3",
      "OWASP 열 가지 리스크 중 컨테이너 고유 수단이 붙는 것은 일곱",
      "인젝션 · XML 외부 엔티티 · XSS 는 막다른 길이고, 나머지는 앞 장의 수단이 붙는다. 가장 자주 나온 권고는 이미지 스캔이다.",
      "열 가지 리스크를 컨테이너 고유 수단이 있는가로 가르는 흐름도")

ROW0, STRIDE, BH = 108, 60, 48
CX = 140                      # 왼쪽 열 중심
RISK_X, RISK_W = 296, 212
MEAN_X, MEAN_W = 548, 372

# 시작: 열 가지 리스크
d.tone(40, 196, 200, 36, MUTED, 18, "12", 1.0)
d.t(CX, 219, "OWASP 리스크 열 가지", 13, INK, KR, "middle", 600)
d.arrow([(CX, 232), (CX, 264)], MUTED, "ar", 1.5)

# 판단: 마름모
DY = ROW0 + 3 * STRIDE + BH // 2   # 312
d.o.append(f'<polygon points="{CX},{DY-48} {CX+100},{DY} {CX},{DY+48} {CX-100},{DY}" fill="{INFO}18" stroke="{INFO}" stroke-width="1.2"/>')
d.t(CX, DY - 4, "컨테이너 고유", 13, INK, KR, "middle", 600)
d.t(CX, DY + 14, "수단이 있는가", 13, INK, KR, "middle", 600)

# 아니오: 막다른 길
d.arrow([(CX, DY + 48), (CX, 392)], BAD, "bad", 1.5)
d.t(CX + 12, DY + 76, "아니오", 13, BAD, KR, "start", 600)
d.tone(40, 392, 200, 96, BAD, 6, "14", 1.2)
for k, name in enumerate(["인젝션", "XML 외부 엔티티", "XSS"]):
    d.t(CX, 420 + k * 24, name, 13, INK, KR, "middle", 600)
d.arrow([(CX, 488), (CX, 520)], BAD, "bad", 1.5)
d.tone(40, 520, 200, 48, INFO, 6, "14", 1.0)
d.t(CX, 540, "자기 코드 검토", 13, INK, KR, "middle", 600)
d.t(CX, 558, "의존성은 이미지 스캐너", 13, MUTED, KR, "middle")

# 예: 버스 + 일곱 행
d.line(240, DY, 272, DY, OK, 1.5)
d.t(256, DY - 8, "예", 13, OK, KR, "middle", 600)
ROWS = [
    ("인증 취약",              "시크릿 전달 · 인증서",             "12장 · 11장 서비스 메시", False),
    ("민감정보 노출",          "접근 자격증명 제한 · 이미지 시크릿 스캔", "최소 권한 · 직무 분리", False),
    ("접근 통제 취약",         "비root · capability 제한 · rootless", "9장 · seccomp · AppArmor · SELinux", False),
    ("보안 설정 오류",         "CIS 벤치마크 · CSPM · 환경 변수 제한", "Docker · Kubernetes · 호스트 · 클라우드", False),
    ("안전하지 않은 역직렬화", "전용 컨테이너 · 네트워크 제한",       "8장 Firecracker · gVisor · 10장", False),
    ("알려진 취약점 컴포넌트", "이미지 스캐너 · 재빌드 · 교체",       "7장 · 투입 대비 효과 최대", True),
    ("로깅·모니터링 부족",     "이벤트 일곱 · SIEM · 차단",          "13장 런타임 프로파일", False),
]
yc0 = ROW0 + BH // 2
d.line(272, yc0, 272, yc0 + 6 * STRIDE, OK, 1.5)
for i, (risk, main, sub, focal) in enumerate(ROWS):
    y = ROW0 + i * STRIDE
    yc = y + BH // 2
    c = ACC if focal else OK
    d.arrow([(272, yc), (RISK_X, yc)], c, "acc" if focal else "ok", 1.5)
    d.box(RISK_X, y, RISK_W, BH, PAPER2, RULE, 0.9)
    d.t(RISK_X + 12, yc + 5, risk, 13, INK, KR, "start", 600)
    d.arrow([(RISK_X + RISK_W, yc), (MEAN_X, yc)], c, "acc" if focal else "ok", 1.5)
    d.tone(MEAN_X, y, MEAN_W, BH, c, 6, "1F" if focal else "12", 1.4 if focal else 1.0)
    d.t(MEAN_X + 12, y + 20, main, 13, INK, KR, "start", 600)
    d.t(MEAN_X + 12, y + 38, sub, 13, MUTED, KR, "start")

d.legend(H - 56, [("고유 수단 있음", OK), ("막다른 길", BAD), ("판단", INFO), ("가장 자주 나온 권고", ACC)])
d.save("14-01.owasp-container-map.svg")
