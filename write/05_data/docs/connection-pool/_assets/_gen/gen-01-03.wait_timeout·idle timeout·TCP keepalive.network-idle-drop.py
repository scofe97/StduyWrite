# -*- coding: utf-8 -*-
# 타입 스펙: type-sequence
"""중간 네트워크 장비의 유휴 연결 추적과 무통보 드롭(Silent Drop) 시퀀스 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
좌표와 간격은 모두 4의 배수로 산출한다.
다크 스킨 토큰과 1곳의 focal 포인트를 적용한다.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 520

d = Seq(
    W,
    H,
    "CONNECTION POOL · NETWORK TIMEOUT SEQUENCE",
    "중간 네트워크 장비의 유휴 연결 추적과 무통보 드롭",
    "상태 저장형 장비의 유휴 만료에 따른 세션 엔트리 침묵 삭제와 고스트 커넥션 발생 흐름",
    lead="양 끝 통보 없는 추적 항목 삭제로 생기는 고스트 커넥션과 쿼리 전송 시점의 단절"
)

# 세 개 참여자 레인
d.lanes([
    ("애플리케이션 (풀)", "HikariCP Pool"),
    ("중간 네트워크 장비", "NLB · NAT · 방화벽 conntrack"),
    ("데이터베이스 서버", "MySQL · MariaDB · PostgreSQL")
], y0=96, lane_w=224)

# 가이드 레일 (수직 점선)
d.rails(464)

# 1. 초기 연결 수립
y = 160
d.msg("애플리케이션 (풀)", "데이터베이스 서버", "TCP 3-Way Handshake / JDBC Connect", y, OK, mk="ok")
d.state("중간 네트워크 장비", "ESTABLISHED (타이머 350s)", y + 24, OK)

# 2. 유휴 시간 경과 (트래픽 부재)
y = 224
d.selfmsg("애플리케이션 (풀)", "유휴 대기 (풀 보관)", y, INFO, "풀 내 유휴 상태 유지")
d.selfmsg("중간 네트워크 장비", "타이머 카운트다운 경과", y + 40, WARN, "양방향 패킷 부재 · 350초 만료")

# 3. 무통보 침묵 삭제 (FOCAL POINT)
y = 308
# 중간 장비 엔트리 제거 상태 칩
d.state("중간 네트워크 장비", "세션 삭제 (Silent Drop)", y, ACC)
d.t(W // 2, y + 24, "삭제 시점에 양 끝으로 알림 없음", 12, ACC, KR, "middle", 600)

# 양 끝단의 고스트 상태
d.state("애플리케이션 (풀)", "정상 연결 간주 (고스트)", y + 48, WARN)
d.state("데이터베이스 서버", "정상 소켓 유지", y + 48, WARN)

# 4. 풀에서 커넥션 대여 후 쿼리 전송 시도
y = 396
d.msg("애플리케이션 (풀)", "중간 네트워크 장비", "SQL Query 전송 (DATA 패킷)", y, BAD, mk="bad")
d.t(d.LX["중간 네트워크 장비"], y + 20, "추적 없는 연결 → RST (NLB) 또는 드롭", 12, BAD, KR, "middle", 600)

# 5. 애플리케이션 장애 수신
y = 440
d.msg("중간 네트워크 장비", "애플리케이션 (풀)", "TCP RST 또는 무응답 타임아웃", y, BAD, mk="bad", dash="4 4")
d.selfmsg("애플리케이션 (풀)", "소켓 오류 (리셋 · 읽기 타임아웃)", y + 24, BAD, "드라이버 예외로 전달")

# 범례
d.legend(480, [
    ("정상 수립 · 대여", OK),
    ("대기 · 주의 상태", WARN),
    ("세션 침묵 삭제 (Focal)", ACC),
    ("패킷 차단 · 연결 오류", BAD),
])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-03.wait_timeout·idle timeout·TCP keepalive.network-idle-drop.svg"
d.save(str(out_svg))
print(f"Generated: {out_svg}")
