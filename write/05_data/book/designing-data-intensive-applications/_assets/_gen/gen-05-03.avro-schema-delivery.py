# 05-03 §3 — 맥락에 따른 Avro writer 스키마의 세 가지 전달 방식과 호환성 진화 규칙.
# 사실 출처: 05-03 본문 §3(L86~L100), 원서 Ch.5 But what is the writer's schema?(PDF p.15~16). 원서는 버전 번호의 바이트 수를 말하지 않는다(정수 또는 해시).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
H = 516
LEG = 460

d = D(W, H, "05-03 · AVRO SCHEMA DELIVERY", "Avro 맥락별 writer 스키마 전달 방식",
      "대용량 파일·DB 레지스트리·RPC 연결 협상이라는 세 맥락으로 스키마를 전달하고, 기본값 규칙으로 호환성을 유지한다.",
      "큰 파일 헤더 전달 · DB 버전 번호와 레지스트리 · RPC 연결 협상 · 스키마 진화 규칙")

X0 = 24
CW = 268
GAP = 14

cards = [
    ("대용량 컨테이너 파일", "object container file", ACC, [
        ("파일 헤더", "writer 스키마 1회 포함", ACC),
        ("데이터 블록", "수백만 레코드 연속 기록", INFO),
        ("특징 요약", "레코드별 스키마 오버헤드 0", MUTED)
    ], [
        "파일 시작 시점에 스키마 1회 기록",
        "수백만 레코드 데이터 공간 절감",
        "같은 스키마로 쓴 레코드 묶음"
    ]),
    ("개별 레코드 DB·스트림", "Confluent 레지스트리 · Espresso", OK, [
        ("레코드 선두", "스키마 버전 번호", OK),
        ("중앙 DB", "Schema Registry 스키마 조회", INFO),
        ("특징 요약", "버전 관리 및 호환성 중앙 검증", MUTED)
    ], [
        "레코드 앞에 버전 번호 포함",
        "중앙 레지스트리에서 스키마 조회",
        "다른 시점 작성 레코드 공존 지원"
    ]),
    ("네트워크 RPC 연결", "Avro RPC", INFO, [
        ("연결 수립", "스키마 버전 협상", INFO),
        ("세션 수명", "동일 협상 스키마 재사용", ACC),
        ("특징 요약", "호출별 스키마 교환 비용 제거", MUTED)
    ], [
        "연결 설정 시 스키마 버전 협상",
        "연결 지속 동안 스키마 재전송 없음",
        "양방향 네트워크 연결에서 사용"
    ])
]

# 상단: 3개 맥락 카드
for i, (title, sub, col, blocks, items) in enumerate(cards):
    cx = X0 + i * (CW + GAP)
    d.box(cx, PY, CW, 206, PAPER2, col, 1.2 if col == ACC else 0.9)
    d.chip(cx + 34, PY + 20, f"맥락 {i+1}", col, 11)
    d.t(cx + 72, PY + 24, title, 12.5, INK, KR, "start", 600)
    d.line(cx + 8, PY + 34, cx + CW - 8, PY + 34, RULE, 0.8)
    
    # 내부 구조 블록 2개
    for j, (b_top, b_bot, b_col) in enumerate(blocks[:2]):
        by = PY + 42 + j * 38
        d.box(cx + 8, by, CW - 16, 32, PAPER, RULE, 0.8)
        d.t(cx + 14, by + 15, b_top, 11.5, b_col, KR, "start", 600)
        d.t(cx + CW - 14, by + 15, b_bot, 11.5, SOFT, KR, "end")
    
    d.line(cx + 8, PY + 122, cx + CW - 8, PY + 122, RULE, 0.8)
    
    # 텍스트 요약 3줄
    for j, item in enumerate(items):
        iy = PY + 130 + j * 22
        d.t(cx + 14, iy + 11, f"· {item}", 11.5, MUTED, KR, "start")

# 하단: Avro 스키마 진화 핵심 제약과 장점
S2_Y = PY + 222
d.box(X0, S2_Y, 832, 86, PAPER2, RULE, 0.9)
d.chip(X0 + 44, S2_Y + 18, "진화 규칙", WARN, 11.5)
d.t(X0 + 84, S2_Y + 22, "Avro 스키마 진화 제약과 동적 생성 친화성", 12.5, INK, KR, "start", 600)
d.line(X0 + 8, S2_Y + 32, X0 + 824, S2_Y + 32, RULE, 0.8)

sub_cols = [
    ("기본값 필수 원칙", "기본값 정의 필드만 추가·삭제 허용", WARN),
    ("union null 명시", "null 기본값은 union 첫 분기일 때", INFO),
    ("동적 스키마 친화", "DB 스키마 덤프 시 자동 Avro 스키마 생성", OK)
]
SC_W = 264
SGAP = 12
for i, (sc_title, sc_desc, sc_col) in enumerate(sub_cols):
    scx = X0 + 8 + i * (SC_W + SGAP)
    scy = S2_Y + 40
    d.box(scx, scy, SC_W, 36, PAPER, RULE, 0.8)
    d.t(scx + SC_W / 2, scy + 16, sc_title, 11.5, sc_col, KR, "middle", 600)
    d.t(scx + SC_W / 2, scy + 29, sc_desc, 11.5, MUTED, KR, "middle")

d.legend(LEG, [("스키마 전달 위치", ACC), ("레코드 바이너리 데이터", INFO), ("스키마 레지스트리 관리", OK), ("스키마 기본값 제약", WARN)])
d.save("05-03.avro-schema-delivery.svg")
