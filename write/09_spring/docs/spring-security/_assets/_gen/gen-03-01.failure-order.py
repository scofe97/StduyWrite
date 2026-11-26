# 사실 출처: 로그인 실패 응답 보안 순서 비교(예제 앱 기준)
# 타입 스펙: type-flowchart
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 680
d = D(
    W, H,
    "FLOWCHART · POLICY EVALUATION ORDER",
    "실패 응답이 계정 존재를 드러내는 순서와 숨기는 순서",
    "계정 상태를 먼저 확인해 계정 존재가 노출되는 순서와 해시를 먼저 비교해 숨기는 순서의 비교",
    "예제 앱 기준"
)

LX = 240
RX = 720
DW, DH = 62, 26

def diamond(cx, cy, label, c=WARN, lab_c=INK):
    pts = f"{cx},{cy-DH} {cx+DW},{cy} {cx},{cy+DH} {cx-DW},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.3"/>')
    d.t(cx, cy + 4, label, 12, lab_c, KR, "middle", 600)

# 중앙 구분선
d.line(480, 104, 480, 580, RULE, 0.8, dash="4 4")

# 열 헤더
d.box(LX - 150, 104, 300, 34, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(LX, 126, "상태를 먼저 보는 순서", 13, INK, KR, "middle", 600)

d.box(RX - 150, 104, 300, 34, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(RX, 126, "비밀번호를 먼저 보는 순서", 13, INK, KR, "middle", 600)

# ── 왼쪽 열: 상태 우선 (계정 노출) ──
# 1. 이메일 조회
d.box(LX - 90, 154, 180, 38, fill=PAPER2, stroke=INFO, sw=1.1)
d.t(LX, 178, "이메일 조회", 13, INK, KR, "middle", 600)
d.arrow([(LX, 192), (LX, 226)], MUTED, "ar", 1.3)

# 2. 계정 존재 판정
diamond(LX, 252, "계정 존재?", WARN)
# 없음 -> 401
d.arrow([(LX - DW, 252), (102, 252)], BAD, "bad", 1.3)
d.t((LX - DW + 102) / 2, 244, "없음", 11, BAD, KR)
d.box(16, 232, 84, 40, fill=PAPER2, stroke=BAD, sw=1.1)
d.t(58, 249, "401", 13, BAD, MONO, "middle", 600)
d.t(58, 263, "계정 없음", 11, MUTED, KR, "middle")

# 있음 -> 상태 확인
d.arrow([(LX, 252 + DH), (LX, 314)], MUTED, "ar", 1.3)
d.t(LX + 18, 290, "있음", 11, MUTED, KR, "start")

# 3. 상태 확인 (ACC 갈리는 지점)
diamond(LX, 340, "상태 확인", ACC, ACC)
# LOCKED -> 423 (BAD: 틀린 비밀번호여도 도달)
d.arrow([(LX - DW, 340), (122, 340)], BAD, "bad", 1.3)
d.t((LX - DW + 122) / 2, 332, "LOCKED", 11, BAD, MONO)
d.tone(16, 320, 104, 40, BAD, r=6)
d.t(68, 337, "423 Locked", 12, BAD, MONO, "middle", 600)
d.t(68, 351, "있는 계정만 423", 11, BAD, KR, "middle")

# ACTIVE -> 비밀번호 비교
d.arrow([(LX, 340 + DH), (LX, 406)], MUTED, "ar", 1.3)
d.t(LX + 18, 386, "ACTIVE", 11, MUTED, MONO, "start")

# 4. 비밀번호 비교
diamond(LX, 432, "비밀번호 비교", WARN)
# 불일치 -> 401
d.arrow([(LX - DW, 432), (102, 432)], BAD, "bad", 1.3)
d.t((LX - DW + 102) / 2, 424, "틀림", 11, BAD, KR)
d.box(16, 412, 84, 40, fill=PAPER2, stroke=BAD, sw=1.1)
d.t(58, 429, "401", 13, BAD, MONO, "middle", 600)
d.t(58, 443, "비밀번호 오류", 11, MUTED, KR, "middle")

# 일치 -> 200
d.arrow([(LX, 432 + DH), (LX, 498)], OK, "ok", 1.3)
d.t(LX + 18, 478, "맞음", 11, OK, KR, "start")
d.tone(LX - 60, 500, 120, 40, OK, r=6)
d.t(LX, 517, "200 OK", 13, OK, MONO, "middle", 600)
d.t(LX, 532, "로그인 성공", 11, OK, KR, "middle")

# ── 오른쪽 열: 비밀번호 우선 (계정 보호) ──
# 1. 이메일 조회
d.box(RX - 100, 152, 200, 42, fill=PAPER2, stroke=INFO, sw=1.1)
d.t(RX, 169, "이메일 조회", 13, INK, KR, "middle", 600)
d.t(RX, 185, "없으면 가짜 해시로 비교", 11, INFO, KR, "middle")
d.arrow([(RX, 194), (RX, 226)], MUTED, "ar", 1.3)

# 2. 비밀번호 비교
diamond(RX, 252, "비밀번호 비교", WARN)
# 틀림 -> 401 (OK: 계정 유무 동일 응답)
d.arrow([(RX + DW, 252), (848, 252)], OK, "ok", 1.3)
d.t((RX + DW + 848) / 2, 244, "틀림", 11, OK, KR)
d.box(850, 232, 94, 40, fill=PAPER2, stroke=OK, sw=1.1)
d.t(897, 249, "401", 13, OK, MONO, "middle", 600)
d.t(897, 263, "계정 유무 동일", 11, OK, KR, "middle")

# 맞음 -> 상태 확인
d.arrow([(RX, 252 + DH), (RX, 314)], MUTED, "ar", 1.3)
d.t(RX + 18, 290, "맞음", 11, MUTED, KR, "start")

# 3. 상태 확인 (ACC 갈리는 지점)
diamond(RX, 340, "상태 확인", ACC, ACC)
# LOCKED -> 423
d.arrow([(RX + DW, 340), (848, 340)], BAD, "bad", 1.3)
d.t((RX + DW + 848) / 2, 332, "LOCKED", 11, BAD, MONO)
d.box(850, 320, 94, 40, fill=PAPER2, stroke=BAD, sw=1.1)
d.t(897, 337, "423", 13, BAD, MONO, "middle", 600)
d.t(897, 351, "계정 잠김", 11, MUTED, KR, "middle")

# PENDING·DISABLED -> 403
d.arrow([(RX - DW, 340), (598, 340)], WARN, "warn", 1.3)
d.t((RX - DW + 598) / 2, 332, "미승인", 11, WARN, KR)
d.box(502, 320, 94, 40, fill=PAPER2, stroke=WARN, sw=1.1)
d.t(549, 337, "403", 13, WARN, MONO, "middle", 600)
d.t(549, 351, "대기·비활성", 11, MUTED, KR, "middle")

# ACTIVE -> 200
d.arrow([(RX, 340 + DH), (RX, 498)], OK, "ok", 1.3)
d.t(RX + 18, 419, "ACTIVE", 11, OK, MONO, "start")
d.tone(RX - 60, 500, 120, 40, OK, r=6)
d.t(RX, 517, "200 OK", 13, OK, MONO, "middle", 600)
d.t(RX, 532, "로그인 성공", 11, OK, KR, "middle")

# 범례
d.legend(H - 44, [
    ("순서 갈림", ACC),
    ("정상·동일", OK),
    ("계정 노출·거부", BAD),
    ("판단·비교", WARN),
    ("입력·가짜 해시", INFO),
])

out_path = Path(__file__).parent.parent / "03-01.failure-order.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
