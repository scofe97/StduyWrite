# 05-03 개요 — Protocol Buffers와 Avro의 이진 인코딩, 스키마 진화와 스키마 전달 방식 전체 지도.
# 사실 출처: 05-03 도입(L17~L21), §1(L30~L56), §2(L61~L75), §3(L84~L100), §4(L105~L116)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "05-03 · CHAPTER OVERVIEW", "Protocol Buffers와 Avro 전체 지도",
      "필드 태그와 스키마 해소라는 두 접근법, 스키마 진화 호환 규칙과 세 가지 전달 경로를 잇는다.",
      "필드 태그 압축 · 스키마 해소 번역 · 기본값 진화와 전달 · 스키마의 장점")

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "Protocol Buffers", "field tag 기반 압축",
     [("field tag 인코딩", "필드명 생략 · 33B 압축"),
      ("타입 주석·가변 정수", "1337=2B · repeated 반복"),
      ("태그 기반 진화", "미지 태그 건너뜀 · forward")],
     INFO),
    ("§2", "Apache Avro", "writer/reader 스키마",
     [("순수 값 바이트 열", "태그·타입 생략 · 32B 압축"),
      ("두 스키마 분리", "writer·reader 스키마"),
      ("필드명 매칭 번역", "순서 무관 · 기본값 대체")],
     ACC),
    ("§3", "진화와 전달", "호환 규칙과 세 가지 전달",
     [("기본값 필수 규칙", "기본값 있는 필드만 변경"),
      ("union null 명시", "첫 분기 null 이면 기본값"),
      ("맥락별 스키마 전달", "큰 파일 · DB 버전 · RPC")],
     WARN),
    ("§4", "스키마 장점", "이진 스키마의 가치",
     [("압축성과 최신 문서", "JSON 대비 절반 이하 크기"),
      ("배포 전 호환성 검사", "스키마 DB 로 미리 검사"),
      ("코드 생성", "정적 타입 언어의 타입 검사")],
     OK),
]

FOCAL = 1

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)
    
    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)
    
    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 11.5, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)
    
    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64
        
        if is_focal and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, ACC, KR, "middle")
        elif i == 0 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, INFO, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, INFO, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, WARN, KR, "middle")
        elif i == 3 and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, OK, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 11.5, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("핵심 인코딩 모델", ACC), ("필드 식별 방식", INFO), ("호환성 규칙·전달", WARN), ("스키마 이점·검증", OK)])
d.save("05-03.chapter-overview.svg")
