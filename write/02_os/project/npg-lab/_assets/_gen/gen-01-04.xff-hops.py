# 01-04-xff-hops — 전달 헤더 신뢰 경계와 위치 기반 신뢰 우회
# 본문 요구: 생명선 넷(손님 · Caddy · npgproxy · fakeinv). 홉마다 두 값을 나란히: 사실 remote_addr(바로 앞 홉), 주장 X-Forwarded-For. E3 기본 판: 손님이 203.0.113.195 를 실어도 맨 뒤에는 ["127.0.0.1"] 만 남음(앞 홉을 안 믿어 버림). 아래쪽에 E3 6단계: 127.0.0.1/32 를 믿게 하자 curl 직접 6.6.6.6 이 6.6.6.6, 127.0.0.1 로 통과 — 한 기계라 손님도 127.0.0.1. focal 은 6단계 통과 자리.
# 타입 스펙: type-sequence
# 사실 출처: 01-04.리버스 프록시 앞단 층 — 규칙 고르기·전달 헤더 신뢰·건강 검사.md:90-128, ADR 0017:9,16-44,51-56, ch10-e3-forwarded-for-trust.md:24,28,73-91
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 700

d = D(
    W,
    H,
    "SEQUENCE · FORWARDED-FOR TRUST BOUNDARY",
    "전달 헤더 신뢰 경계와 위치 기반 신뢰 우회",
    "앞단 Caddy 와 npgproxy 가 앞 홉을 믿지 않아 가짜 헤더를 지우는 기본 판과, 단일 머신에서 IP 신뢰 부여 시 가짜 주소가 맨 뒤 fakeinv 까지 통과하는 우회",
    lead="앞 홉을 불신하면 가짜 주소가 지워지지만, IP 로 믿으면 같은 기계의 손님 위조가 통과합니다.",
)

# 1. 생명선 넷 (손님, Caddy, npgproxy, fakeinv)
X_CLIENT = 120
X_CADDY = 360
X_PROXY = 600
X_BACKEND = 840

# 상단 참여자 상자 (w=150, h=44)
for x, name, sub in [
    (X_CLIENT, "손님", "curl"),
    (X_CADDY, "Caddy", ":8000"),
    (X_PROXY, "npgproxy", ":28080"),
    (X_BACKEND, "fakeinv", ":29090"),
]:
    d.box(x - 75, 104, 150, 44, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
    d.t(x, 124, name, 13, INK, KR, "middle", 600)
    d.t(x, 140, sub, 12, MUTED, MONO)

# 수직 레일
for x in (X_CLIENT, X_CADDY, X_PROXY, X_BACKEND):
    d.line(x, 156, x, 636, RULE, 1.0, "3 6")

# 2. 판 a 기본: 앞 홉 불신 (y = 168 ~ 420)
d.box(24, 168, 120, 26, fill=PAPER2, stroke=INFO, sw=1.0, r=4)
d.t(84, 186, "판 a 기본", 13, INFO, KR, "middle", 600)

# 메시지 1: 손님 -> Caddy (y=216)
d.arrow([(X_CLIENT, 216), (X_CADDY, 216)], c=MUTED, m="ar", sw=1.4)
d.t((X_CLIENT + X_CADDY) / 2, 200, "GET /_whoami", 13, INK, MONO, "middle")
d.t((X_CLIENT + X_CADDY) / 2, 236, "XFF: 203.0.113.195", 13, WARN, MONO, "middle")

# Caddy 검증: remote_addr 확인 및 불신 (y=252..282)
d.box(X_CADDY - 75, 252, 150, 30, fill=PAPER, stroke="none", sw=0, r=4)
d.tone(X_CADDY - 75, 252, 150, 30, INFO, r=4, op="14", sw=1.0)
d.t(X_CADDY, 272, "remote: 127.0.0.1", 13, INFO, MONO, "middle")

# 메시지 2: Caddy -> npgproxy (y=316)
d.arrow([(X_CADDY, 316), (X_PROXY, 316)], c=MUTED, m="ar", sw=1.4)
d.t((X_CADDY + X_PROXY) / 2, 300, "앞 홉 불신 · 삭제", 13, MUTED, KR, "middle")
d.t((X_CADDY + X_PROXY) / 2, 336, "XFF: 127.0.0.1", 13, INK, MONO, "middle")

# npgproxy 검증: remote_addr 확인 및 불신 (y=352..382)
d.box(X_PROXY - 75, 352, 150, 30, fill=PAPER, stroke="none", sw=0, r=4)
d.tone(X_PROXY - 75, 352, 150, 30, INFO, r=4, op="14", sw=1.0)
d.t(X_PROXY, 372, "remote: 127.0.0.1", 13, INFO, MONO, "middle")

# 메시지 3: npgproxy -> fakeinv (y=406)
d.arrow([(X_PROXY, 406), (X_BACKEND - 80, 406)], c=OK, m="ok", sw=1.4)
d.t((X_PROXY + X_BACKEND - 80) / 2, 424, "SetXForwarded", 13, MUTED, MONO, "middle")

# fakeinv 결과 (판 a, y=384..436)
d.box(X_BACKEND - 75, 384, 150, 52, fill=PAPER, stroke="none", sw=0, r=6)
d.tone(X_BACKEND - 75, 384, 150, 52, OK, r=6, op="18", sw=1.2)
d.t(X_BACKEND, 404, "[\"127.0.0.1\"]", 13, OK, MONO, "middle", 600)
d.t(X_BACKEND, 424, "가짜 주소 소멸", 13, MUTED, KR, "middle")

# 구분선
d.line(24, 448, 936, 448, RULE, 0.8, dash="4 4")

# 3. 6단계: 위치 기반 신뢰 우회 (y = 460 ~ 630)
d.box(24, 460, 140, 26, fill=PAPER2, stroke=WARN, sw=1.0, r=4)
d.t(94, 478, "6단계 위치 신뢰", 13, WARN, KR, "middle", 600)

# 메시지 4: 손님 curl -> npgproxy 직접 전송 (y=502)
d.arrow([(X_CLIENT, 502), (X_PROXY, 502)], c=WARN, m="warn", sw=1.4)
d.t((X_CLIENT + X_PROXY) / 2, 486, "curl 직접 호출", 13, INK, KR, "middle")
d.t((X_CLIENT + X_PROXY) / 2, 522, "XFF: 6.6.6.6 (위조)", 13, WARN, KR, "middle")

# npgproxy 검증: 127.0.0.1/32 신뢰 일치 (y=534..564)
d.box(X_PROXY - 90, 534, 180, 30, fill=PAPER, stroke="none", sw=0, r=4)
d.tone(X_PROXY - 90, 534, 180, 30, WARN, r=4, op="18", sw=1.0)
d.t(X_PROXY, 554, "127.0.0.1/32 신뢰 일치", 13, WARN, KR, "middle")

# 메시지 5: npgproxy -> fakeinv (y=594)
d.arrow([(X_PROXY, 594), (X_BACKEND - 95, 594)], c=ACC, m="acc", sw=1.4)
d.t((X_PROXY + X_BACKEND - 95) / 2, 614, "헤더 복원", 13, ACC, KR, "middle")

# fakeinv 결과 (focal: 6단계 우회 통과, y=570..626)
d.box(X_BACKEND - 95, 570, 190, 56, fill=PAPER, stroke="none", sw=0, r=6)
d.tone(X_BACKEND - 95, 570, 190, 56, ACC, r=6, op="20", sw=1.4)
d.t(X_BACKEND, 592, "[\"6.6.6.6, 127.0.0.1\"]", 12, ACC, MONO, "middle", 600)
d.t(X_BACKEND, 612, "6.6.6.6 통과 (우회)", 13, ACC, KR, "middle", 600)

# 범례
d.legend(
    654,
    [
        ("사실 검증", INFO),
        ("정상 방어", OK),
        ("위조 주장", WARN),
        ("신뢰 우회 (focal)", ACC),
    ],
)

out = ASSETS_DIR / "01-04-xff-hops.svg"
d.save(out)
print(f"saved: {out}")
