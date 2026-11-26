# 사실 출처: Tomcat 11 RemoteIpValve.invoke() (오른쪽부터, internal 건너뜀, 첫 비신뢰 IP), Spring Boot 4.1.1 internal-proxies 기본값(사설 대역 전체), 예시 IP
# 타입 스펙: type-flowchart
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 670
d = D(
    W, H,
    "FLOWCHART · REMOTE IP VALVE EVALUATION",
    "같은 헤더를 기본값과 좁힌 값으로 읽은 결과",
    "RemoteIpValve가 X-Forwarded-For를 오른쪽부터 검증할 때 프록시 신뢰 대역 설정에 따른 클라이언트 IP 판정 비교",
    "Tomcat 11 RemoteIpValve.invoke() 역순 순회 로직 기준"
)

# ── 공통 입력 (상단 영역) ──
d.box(40, 104, 880, 104, PAPER2, RULE, 1.0)
d.t(480, 124, "공통 입력: 위조 요청과 Nginx 프록시 전달 헤더", 12, INK, KR, "middle", 600)

# 헤더 토막 시각화
d.t(210, 150, "사용자 위조 헤더", 11, MUTED, KR, "middle")
d.chip(210, 172, "1.2.3.4", BAD, 11)

d.arrow([(270, 172), (340, 172)], INFO, "info", 1.4)
d.t(305, 164, "Nginx 덧붙임", 11, INFO, KR, "middle")

d.t(560, 150, "Spring 수신 헤더 토막 (연결 상대: 172.18.0.2)", 11, MUTED, KR, "middle")
d.chip(490, 172, "1.2.3.4", BAD, 11)
d.t(536, 176, ",", 13, MUTED, MONO)
d.chip(584, 172, "10.8.0.7", INFO, 11)

# 순회 방향 안내 (오른쪽부터)
d.arrow([(580, 196), (500, 196)], WARN, "warn", 1.3)
d.t(670, 196, "← 오른쪽부터 역순 검증", 11, WARN, KR, "middle")

# ── 하단 2분기 (비교 트레이스) ──
LX, RX = 250, 710
BW, BH = 340, 42

# 중앙 구분선
d.line(480, 226, 480, 598, RULE, 0.8, dash="4 4")

# 열 헤더
d.box(LX - BW / 2, 228, BW, 34, PAPER2, RULE, 1.0)
d.t(LX, 250, "internal-proxies 기본값 (사설 대역 전체)", 13, INK, KR, "middle", 600)

d.box(RX - BW / 2, 228, BW, 34, PAPER2, ACC, 1.2)
d.t(RX, 250, "internal-proxies = 172.18.0.2 만", 13, ACC, MONO, "middle", 600)

# ── 왼쪽 열: 기본값 순회 ──
# 1단계: 172.18.0.2
d.box(LX - BW / 2, 280, BW, BH, PAPER2, RULE, 1.0)
d.t(LX, 298, "1. 172.18.0.2 신뢰 확인", 12, INK, MONO, "middle", 600)
d.t(LX, 312, "사설 대역 기본 포함 → 통과", 11, MUTED, KR, "middle")
d.arrow([(LX, 322), (LX, 350)], MUTED, "ar", 1.3)

# 2단계: 10.8.0.7
d.box(LX - BW / 2, 352, BW, BH, PAPER2, RULE, 1.0)
d.t(LX, 370, "2. 10.8.0.7 신뢰 확인", 12, INK, MONO, "middle", 600)
d.t(LX, 384, "사설 대역(10/8) 포함 → 건너뜀", 11, WARN, KR, "middle")
d.arrow([(LX, 394), (LX, 422)], MUTED, "ar", 1.3)

# 3단계: 1.2.3.4
d.box(LX - BW / 2, 424, BW, BH, PAPER2, RULE, 1.0)
d.t(LX, 442, "3. 1.2.3.4 비신뢰 발견", 12, INK, MONO, "middle", 600)
d.t(LX, 456, "공인 IP → 첫 비신뢰 IP 확정", 11, BAD, KR, "middle")
d.arrow([(LX, 466), (LX, 498)], BAD, "bad", 1.3)

# 결과 상자 (위조 성공)
d.tone(LX - BW / 2, 500, BW, 52, BAD, r=6)
d.t(LX, 522, "클라이언트 IP = 1.2.3.4", 13, BAD, MONO, "middle", 600)
d.t(LX, 540, "위조 성공 (공격자 IP로 오인)", 11, BAD, KR, "middle")

# ── 오른쪽 열: 좁힌 값 순회 ──
# 1단계: 172.18.0.2
d.box(RX - BW / 2, 280, BW, BH, PAPER2, RULE, 1.0)
d.t(RX, 298, "1. 172.18.0.2 신뢰 확인", 12, INK, MONO, "middle", 600)
d.t(RX, 312, "172.18.0.2 일치 → 통과", 11, MUTED, KR, "middle")
d.arrow([(RX, 322), (RX, 350)], MUTED, "ar", 1.3)

# 2단계: 10.8.0.7
d.box(RX - BW / 2, 352, BW, BH, PAPER2, OK, 1.1)
d.t(RX, 370, "2. 10.8.0.7 신뢰 확인", 12, INK, MONO, "middle", 600)
d.t(RX, 384, "믿는 대상 아님 → 즉시 멈춤", 11, OK, KR, "middle")
d.arrow([(RX, 394), (RX, 422)], OK, "ok", 1.3)

# 3단계: 순회 멈춤
d.box(RX - BW / 2, 424, BW, BH, PAPER2, OK, 1.0)
d.t(RX, 442, "3. 1.2.3.4 도달 전 종료", 12, INK, KR, "middle", 600)
d.t(RX, 456, "첫 비신뢰 IP(10.8.0.7) 확정", 11, MUTED, KR, "middle")
d.arrow([(RX, 466), (RX, 498)], OK, "ok", 1.3)

# 결과 상자 (정상 인식)
d.tone(RX - BW / 2, 500, BW, 52, OK, r=6)
d.t(RX, 522, "클라이언트 IP = 10.8.0.7", 13, OK, MONO, "middle", 600)
d.t(RX, 540, "정상 인식 (실제 VPN 주소)", 11, OK, KR, "middle")

# 범례
d.legend(H - 44, [
    ("바꾼 설정", ACC),
    ("정상 인식", OK),
    ("위조 성공", BAD),
    ("건너뜀·검증", WARN),
    ("헤더 토막", INFO),
])

out_path = Path(__file__).parent.parent / "03-01.xff-trust.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
