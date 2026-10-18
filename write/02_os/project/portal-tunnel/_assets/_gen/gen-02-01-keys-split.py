# 타입 스펙: type-architecture
# 사실 출처: RFC 8446 §2 (Protocol Overview), §4.4.3 (Certificate Verify),
#   §7.1 (Key Schedule), RFC 7748 (Curve25519).
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 520
d = D(W, H, "TLS 1.3 · CRYPTOGRAPHIC KEY SPLIT",
      "인증서 서명 키와 ECDHE 임시 세션 키의 분리",
      "인증서 개인키는 신원 증명 서명에만 사용되며 세션 트래픽 복호화 권한이 없고, ECDHE 임시 개인키는 세션 데이터 암호화를 전담하지만 독자적 신원 증명 권한이 없습니다.",
      lead="서명 권한과 복호화 권한의 수학적 분리가 전방 비밀성과 키리스 TLS 의 토대가 됩니다")

# 1. 좌측 영역: 인증서 개인키 (신원 증명)
lx, ly, lw, lh = 24, 104, 444, 276
d.box(lx, ly, lw, lh, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(lx + 16, ly + 24, "IDENTITY KEY", 9, WARN, MONO, "start", 600)
d.t(lx + 106, ly + 24, "인증서 개인키 (장기 신원 서명)", 12, INK, KR, "start", 600)
d.t(lx + 16, ly + 42, "CA 서명 X.509 인증서 대응 · 유효기간 90일~200일(2026 기준, 점차 축소)", 10, MUTED, KR, "start")

left_items = [
    ("트랜스크립트 서명", "CertificateVerify 전자 서명 생성", WARN),
    ("도메인 소유 증명", "공인 도메인의 정당한 소유자 입증", INFO),
    ("수동 복호화 불가", "임시 비밀 미보유로 열람 불가(임의 서명 시 능동 공격 주의)", BAD),
    ("과거 복호화 불가", "키 유출 시에도 과거 트래픽 복호화 불가 (PFS)", BAD),
]

for i, (title, desc_txt, col) in enumerate(left_items):
    iy = ly + 58 + i * 52
    d.box(lx + 12, iy, lw - 24, 42, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.chip(lx + 76, iy + 21, title, col, size=10)
    d.t(lx + 152, iy + 25, desc_txt, 11, MUTED, KR, "start")

# 2. 우측 영역: ECDHE 임시 개인키 (세션 기밀성)
rx, ry, rw, rh = 492, 104, 444, 276
d.box(rx, ry, rw, rh, fill=PAPER2, stroke=OK, sw=1.2, r=8)
d.t(rx + 16, ry + 24, "SESSION KEY", 9, OK, MONO, "start", 600)
d.t(rx + 102, ry + 24, "ECDHE 임시 개인키 (세션 기밀성)", 12, INK, KR, "start", 600)
d.t(rx + 16, ry + 42, "연결마다 새로 생성하는 32바이트 X25519 키 쌍", 10, MUTED, KR, "start")

right_items = [
    ("X25519 키 교환", "공개키 교환으로 (EC)DHE 공유 비밀 도출", OK),
    ("트래픽 암호화", "핸드셰이크 및 애플리케이션 대칭키 도출", OK),
    ("신원 증명 불가", "인증서 서명 없이는 독자 신뢰 획득 불가", BAD),
    ("일회성 메모리 상주", "핸드셰이크 종료 즉시 파기되어 영구 누출 차단", OK),
]

for i, (title, desc_txt, col) in enumerate(right_items):
    iy = ry + 58 + i * 52
    d.box(rx + 12, iy, rw - 24, 42, fill=PAPER, stroke=RULE, sw=0.8, r=4)
    d.chip(rx + 78, iy + 21, title, col, size=10)
    d.t(rx + 154, iy + 25, desc_txt, 11, MUTED, KR, "start")

# 3. 하단 영역: 권한 분리의 아키텍처적 결과 (좌우 2개 박스로 대칭 분할)
by, bh = 394, 54

# 좌하단: 전방 비밀성
d.box(lx, by, lw, bh, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.chip(lx + 90, by + 27, "전방 비밀성 (PFS)", OK, size=10)
d.t(lx + 172, by + 31, "장기 키 누출 시에도 과거 도청 암호문 보호", 11, MUTED, KR, "start")

# 우하단: 키리스 TLS
d.box(rx, by, rw, bh, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.chip(rx + 96, by + 27, "키리스 TLS (Keyless)", ACC, size=10)
d.t(rx + 190, by + 31, "서명 연산만 위임하고 세션 키는 로컬 격리", 11, MUTED, KR, "start")

# 범례
d.legend(468, [
    ("세션 암호화 및 복호화", OK),
    ("신원 증명 및 서명", WARN),
    ("권한 없음 및 차단", BAD),
    ("원격 서명 위임 구조", ACC),
    ("표준 명세 및 인프라", INFO),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01-keys-split.svg"))
d.save(out)
print(f"saved: {out}")
