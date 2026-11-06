# 02-01-module-registry — Caddy 모듈 등록부(정적 init 등록)와 실행 시점 핸들러 조립 파이프라인
# 본문 요구: 가로로 두 구간. 빌드 때: xcaddy 가 빈 import(_) → 패키지 init() → caddy.RegisterModule → 전역 표(ID http.handlers.restrict_prefix → New). 실행 때: JSON "handler": "restrict_prefix" → 표에서 ID 로 찾기 → New() → Provision → Validate. 표 위에 caddy list-modules 가 이 표를 읽는다는 화살표. 바이너리 +160 B 는 작은 값 칸 하나. focal 은 전역 표.
# 타입 스펙: type-process
# 사실 출처: 02-01.프록시 운영 — 무중단 설정 교체·인증서 사슬·모듈 등록부.md:98-124, ch10-e6-restrict-prefix-module.md:23-27,60,77-81, restrictprefix.go:21-41, ADR 0019:20-35
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, RULE, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "PROCESS · CADDY MODULE REGISTRY",
    "Caddy 모듈 등록부와 조립 파이프라인",
    "정적 컴파일 시점의 전역 표 등록과 실행 시점의 JSON 핸들러 인스턴스 조립 흐름",
    lead="바이너리 빌드 때 전역 표에 모듈을 등록하고, 실행 때 JSON 설정으로 인스턴스를 조립합니다.",
)

# 상단 구분선 (4의 배수)
d.line(24, 92, 936, 92, RULE, 0.8)

# 1. 구간 1: 빌드 때 (정적 링크 등록) — x=24..456
d.box(24, 108, 432, 324, fill="rgba(245,245,243,0.02)", stroke=RULE, sw=0.8, r=8)
d.t(40, 130, "빌드 때", 14, INK, KR, "start", 600)
d.line(40, 142, 444, 142, RULE, 0.8)

# 1-1. xcaddy 빌드 도구
d.box(40, 154, 180, 52, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(130, 176, "xcaddy", 14, INFO, MONO, "middle", 600)
d.t(130, 194, "빈 import (_) 주입", 13, MUTED, KR, "middle")

# xcaddy -> init 화살표
d.arrow([(130, 206), (130, 226)], c=MUTED, m="ar", sw=1.4)

# 1-2. 패키지 init()
d.box(40, 226, 180, 52, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(130, 248, "init()", 14, INFO, MONO, "middle", 600)
d.t(130, 266, "패키지 자동 실행", 13, MUTED, KR, "middle")

# init -> RegisterModule 화살표
d.arrow([(130, 278), (130, 298)], c=MUTED, m="ar", sw=1.4)

# 1-3. caddy.RegisterModule
d.box(40, 298, 180, 52, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(130, 320, "RegisterModule", 13, INFO, MONO, "middle", 600)
d.t(130, 338, "모듈 등록 호출", 13, INK, KR, "middle")

# 1-4. 바이너리 +160 B 작은 값 칸
d.box(40, 368, 180, 48, fill=PAPER2, stroke=OK, sw=1.0, r=6)
d.t(130, 388, "바이너리 +160 B", 13, OK, KR, "middle", 600)
d.t(130, 404, "페이지 여백 흡수", 12, MUTED, KR, "middle")

# 1-5. caddy list-modules (전역 표 위)
d.box(256, 154, 192, 52, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(352, 176, "list-modules", 13, INFO, MONO, "middle", 600)
d.t(352, 194, "등록 모듈 조회", 13, MUTED, KR, "middle")

# list-modules -> 전역 표 읽기 화살표 (20px)
d.arrow([(352, 206), (352, 226)], c=INFO, m="info", sw=1.4)
d.t(360, 218, "표 읽기", 12, INFO, KR, "start")

# 1-6. 전역 표 (focal)
d.tone(256, 226, 192, 124, ACC, r=6, op="14", sw=1.6)
d.t(352, 248, "전역 표", 14, ACC, KR, "middle", 600)
d.line(268, 258, 436, 258, RULE, 0.8)
d.t(352, 276, "http.handlers.", 12, MUTED, MONO, "middle")
d.t(352, 294, "restrict_prefix", 13, ACC, MONO, "middle", 600)
d.line(268, 306, 436, 306, RULE, 0.8)
d.t(352, 328, "New: func() Module", 12, OK, MONO, "middle")

# RegisterModule -> 전역 표 등록 화살표 (36px)
d.arrow([(220, 324), (256, 324)], c=ACC, m="acc", sw=1.4)
d.t(238, 314, "등록", 12, ACC, KR, "middle")

# 2. 구간 2: 실행 때 (핸들러 인스턴스 조립) — x=504..936
d.box(504, 108, 432, 324, fill="rgba(245,245,243,0.02)", stroke=RULE, sw=0.8, r=8)
d.t(520, 130, "실행 때", 14, INK, KR, "start", 600)
d.line(520, 142, 924, 142, RULE, 0.8)

# 2-1. JSON 설정 주입
d.box(520, 154, 400, 52, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(720, 176, "JSON 설정 주입", 14, INFO, KR, "middle", 600)
d.t(720, 194, '"handler": "restrict_prefix"', 13, INK, MONO, "middle")

# JSON -> 표에서 ID 로 찾기 화살표 (20px)
d.arrow([(720, 206), (720, 226)], c=MUTED, m="ar", sw=1.4)

# 2-2. 표에서 ID 로 찾기 (h=50, 226..276)
d.box(520, 226, 400, 50, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(720, 248, "ID 로 모듈 찾기", 14, INFO, KR, "middle", 600)
d.t(720, 266, "http.handlers 매핑", 13, MUTED, KR, "middle")

# 전역 표 -> 표에서 ID 로 찾기 연결 화살표 (두 구간 사이 448..520, 길이 72px)
d.arrow([(448, 252), (520, 252)], c=ACC, m="acc", sw=1.4)
d.t(482, 242, "ID 매핑", 12, ACC, KR, "middle")

# ID 로 찾기 -> New() 화살표 (20px)
d.arrow([(720, 276), (720, 296)], c=MUTED, m="ar", sw=1.4)

# 2-3. New() 인스턴스 생성 (h=50, 296..346)
d.box(520, 296, 400, 50, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(720, 318, "New()", 14, OK, MONO, "middle", 600)
d.t(720, 334, "인스턴스 할당", 13, INK, KR, "middle")

# New() -> Provision 화살표 (수직 24px)
d.arrow([(612, 346), (612, 370)], c=MUTED, m="ar", sw=1.4)

# 2-4. Provision (h=46, 370..416)
d.box(520, 370, 184, 46, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(612, 388, "Provision", 13, INFO, MONO, "middle", 600)
d.t(612, 404, '로거 · 기본값 "."', 12, MUTED, KR, "middle")

# Provision -> Validate 화살표 (길이 32px)
d.arrow([(704, 393), (736, 393)], c=MUTED, m="ar", sw=1.4)

# 2-5. Validate (h=46, 370..416)
d.box(736, 370, 184, 46, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(828, 388, "Validate", 13, WARN, MONO, "middle", 600)
d.t(828, 404, "슬래시 검증 · 500 거절", 12, WARN, KR, "middle")

# 3. 범례 (y=448, 높이 492 안에서 448+22=470, 여유 22px >= 16px)
d.legend(
    448,
    [
        ("전역 표 (focal)", ACC),
        ("빌드 도구 · 설정 입력", INFO),
        ("정상 생성 · 바이너리", OK),
        ("유효성 검증", WARN),
    ],
)

d.save("02-01-module-registry.svg")
