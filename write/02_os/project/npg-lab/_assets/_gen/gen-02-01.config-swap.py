# 02-01-config-swap — 새 설정 반영 국면과 검증 실패 시 옛 설정 유지 상태 전이도
# 본문 요구: 새 설정 하나가 지나는 국면: 본문 해석 → Provision(·Validate) → Start(포트 열기) → 교체. 각 국면의 실패 종료는 모두 500 과 옛 설정 유지 로(C1: 문법·모듈·포트 오류, E6: /admin 접두사를 Validate 가 거절). 옛 설정 유지 칸 옆에 E6 사실: 거절 중 손님 요청 60건 실패 0. 그리고 이 칸이 안전을 보장하지 않는다는 점(옛 설정이 새는 설정이면 계속 샘)을 라벨 한 줄로. 강조는 옛 설정 유지.
# 타입 스펙: type-state
# 사실 출처: 02-01.프록시 운영 — 무중단 설정 교체·인증서 사슬·모듈 등록부.md:66-74, ch10-c1-admin-api-control.md:29-33,99-104, ch10-e6-restrict-prefix-module.md:27-31,54-62
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "STATE MACHINE · ATOMIC CONFIG SWAP",
    "새 설정 반영 국면과 검증 실패 시 옛 설정 유지 전이",
    "새 설정의 본문 해석, Provision 및 Validate, Start 국면과 실패 시 500 반환 및 옛 설정 유지 상태 전이도",
    lead="원자 교체는 검증 실패 시 옛 설정을 보존하나, 옛 설정에 결함이 있으면 계속 누출되는 한계를 갖습니다.",
)

# 1. 상단 정상 전이 경로 (y = 124 ~ 192)
# 시작 상태점 (Start Dot)
d.o.append(f'<circle cx="32" cy="158" r="6" fill="{INK}"/>')
d.arrow([(38, 158), (56, 158)], c=MUTED, m="ar", sw=1.4)

# 국면 1: 본문 해석 (x: 56..220, 폭 164)
d.box(56, 124, 164, 68, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(138, 150, "1. 본문 해석", 13, INFO, KR, "middle", 600)
d.t(138, 172, "JSON 문법 검사", 13, INK, KR, "middle")

# 전이 1 -> 2
d.arrow([(220, 158), (284, 158)], c=INFO, m="info", sw=1.4)
d.t(252, 146, "문법 정상", 13, INFO, KR, "middle")

# 국면 2: Provision · Validate (x: 284..484, 폭 200)
d.box(284, 124, 200, 68, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(384, 150, "2. Provision·Validate", 13, INFO, KR, "middle", 600)
d.t(384, 172, "모듈 조립 및 검증", 13, INK, KR, "middle")

# 전이 2 -> 3
d.arrow([(484, 158), (548, 158)], c=INFO, m="info", sw=1.4)
d.t(516, 146, "검증 통과", 13, INFO, KR, "middle")

# 국면 3: Start (x: 548..708, 폭 160)
d.box(548, 124, 160, 68, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(628, 150, "3. Start (포트)", 13, INFO, KR, "middle", 600)
d.t(628, 172, "포트 :8000 바인드", 13, INK, KR, "middle")

# 전이 3 -> 4
d.arrow([(708, 158), (776, 158)], c=OK, m="ok", sw=1.4)
d.t(742, 146, "바인드 성공", 13, OK, KR, "middle")

# 국면 4: 원자 교체 완료 (x: 776..908, 폭 132)
d.tone(776, 124, 132, 68, OK, r=6, op="14", sw=1.4)
d.t(842, 150, "4. 원자 교체", 13, OK, KR, "middle", 600)
d.t(842, 172, "200 OK · 활성", 13, OK, MONO, "middle")

# 종료 상태점 (End Ring Dot)
d.arrow([(908, 158), (926, 158)], c=OK, m="ok", sw=1.4)
d.o.append(f'<circle cx="934" cy="158" r="8" fill="none" stroke="{OK}" stroke-width="1.8"/>')
d.o.append(f'<circle cx="934" cy="158" r="5" fill="{OK}"/>')

# 2. 실패 분기 (모두 HTTP 500 거절 및 옛 설정 유지로 수렴)
# 국면 1 하강 선 (문법 오류 C1)
d.line(138, 192, 138, 236, BAD, 1.2)
d.t(146, 218, "문법 오류 (C1)", 13, BAD, KR, "start")

# 국면 2 하강 선 (모듈 오류 C1 · Validate 거절 E6)
d.line(384, 192, 384, 236, BAD, 1.2)
d.t(392, 218, "모듈 오류 (C1) · 거절 (E6)", 13, BAD, KR, "start")

# 국면 3 하강 선 (포트 충돌 C1)
d.line(628, 192, 628, 236, BAD, 1.2)
d.t(636, 218, "포트 충돌 (C1)", 13, BAD, KR, "start")

# 공통 실패 수집 가로선 (y = 236)
d.line(138, 236, 628, 236, BAD, 1.2)

# 공통 실패선에서 '옛 설정 유지' 상자로 진입하는 화살표
d.arrow([(172, 236), (172, 276)], c=BAD, m="bad", sw=1.4)
d.t(212, 256, "500 거절", 13, BAD, KR, "middle")

# 3. 하단 카드 (y = 276 ~ 384)
# 카드 1: 옛 설정 유지 (x: 48..296, 폭 248) — FOCAL
d.tone(48, 276, 248, 108, ACC, r=6, op="14", sw=1.6)
d.t(172, 306, "옛 설정 유지", 14, ACC, KR, "middle", 600)
d.t(172, 332, "HTTP 500 · 새 설정 폐기", 13, INK, KR, "middle")
d.t(172, 356, "기존 설정 유지 서빙", 13, MUTED, KR, "middle")

# 카드 1 -> 카드 2 연결 화살표
d.arrow([(296, 330), (356, 330)], c=OK, m="ok", sw=1.4)
d.t(326, 314, "요청 지속", 13, OK, KR, "middle")

# 카드 2: E6 실측 가용성 (x: 356..604, 폭 248)
d.box(356, 276, 248, 108, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(480, 306, "E6 실측: 가용성 유지", 13, OK, KR, "middle", 600)
d.t(480, 332, "거절 중 손님 요청 60건", 13, INK, KR, "middle")
d.t(480, 356, "실패 0건 (200 처리)", 13, OK, KR, "middle")

# 카드 2 -> 카드 3 연결 화살표
d.arrow([(604, 330), (664, 330)], c=WARN, m="warn", sw=1.4)
d.t(634, 314, "보안 한계", 13, WARN, KR, "middle")

# 카드 3: 원자 교체의 한계 (x: 664..912, 폭 248)
d.box(664, 276, 248, 108, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(788, 306, "원자 교체의 한계", 13, WARN, KR, "middle", 600)
d.t(788, 332, "옛 설정 결함 시 계속 누출", 13, BAD, KR, "middle", 600)
d.t(788, 356, "배포 도구의 500 감지 필수", 13, MUTED, KR, "middle")

# 4. 범례 (y = 428)
d.legend(
    428,
    [
        ("유지 상태 (focal)", ACC),
        ("정상 교체", OK),
        ("검증 거절 (500)", BAD),
        ("보안 주의", WARN),
        ("정상 전이", INFO),
    ],
)

out_path = ASSETS_DIR / "02-01-config-swap.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
