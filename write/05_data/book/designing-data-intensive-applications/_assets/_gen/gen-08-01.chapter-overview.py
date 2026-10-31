# 08-01 개요 — 트랜잭션 필요성(§1), ACID 네 속성(§2~§4), 단일·다중 객체 연산(§5), abort 재시도 함정(§6)의 전체 체계 지도.
# 사실 출처: 08-01 본문 서두(L13~L19), §1(L23~L29), §2(L31~L37), §3(L39~L45), §4(L47~L53), §5(L55~L68), §6(L70~L79)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY1 = 104
CH = 212
PY2 = 340
LEG = 576
H = LEG + 56

d = D(W, H, "08-01 · CHAPTER OVERVIEW", "ACID와 트랜잭션 개요 전체 지도",
      "트랜잭션이 막는 문제(§1)와 ACID 네 보장(§2~§4), 단일·다중 객체 범위(§5), abort 재시도 함정(§6)의 체계.",
      "트랜잭션 추상화 · 원자성과 일관성 · 격리성과 지속성 · 단일 vs 다중 객체 · 재시도 부작용")

CW = 264
GAP = 20
X0 = 24

cards = [
    # Row 1
    (0, 0, "§1", "트랜잭션 필요성", "오류 처리 추상화",
     [("다중 쓰기 부분 실패", "크래시 시 부분 갱신 방지"),
      ("단일 논리 단위", "전부 성공 또는 전부 취소"),
      ("단순 모델 제공", "애플리케이션 오류 처리 집약")],
     INFO, False),
    (1, 0, "§2", "원자성 (Atomicity)", "abort 가능성",
     [("중단 가능성 보장", "오류 시 선행 쓰기 전면 폐기"),
      ("동시성과 무관", "스레드 원자 연산과 다른 개념"),
      ("안전한 재시도", "초기 상태 보존으로 오염 방지")],
     OK, False),
    (2, 0, "§3", "일관성 (Consistency)", "불변 조건 유지",
     [("애플리케이션 책임", "데이터베이스 단독 보장 불가"),
      ("비즈니스 불변식", "복식 장부 차변·대변 균형"),
      ("스키마 제약 활용", "외래 키·유니크·체크 제약")],
     WARN, False),
    # Row 2
    (0, 1, "§4", "격리성 · 지속성", "간섭 차단과 영구 저장",
     [("격리성 (Isolation)", "동시 실행 트랜잭션 간섭 방지"),
      ("직렬화 가능성", "현실은 약한 격리 수준 다수"),
      ("지속성 (Durability)", "fsync · WAL · 다중 노드 복제")],
     ACC, True),
    (1, 1, "§5", "단일 vs 다중 객체", "다중 객체 동시 조율",
     [("단일 객체 보장", "저장 엔진 기본 원자성·격리성"),
      ("다중 객체 불일치", "메일 카운터·본문 동시 갱신"),
      ("조율 필수 영역", "외래 키 · 비정규화 · 보조 인덱스")],
     INFO, False),
    (2, 1, "§6", "abort 재시도 함정", "무조건적 재시도 위험",
     [("네트워크 타임아웃", "커밋 성공 후 응답 유실 중복 쓰기"),
      ("과부하 악순환", "부하 증가 시 지수 백오프 필요"),
      ("외부 부작용", "이메일 발송 등 DB 외부 취소 불가")],
     BAD, False),
]

for col, row, sec, title, role, items, card_c, is_focal in cards:
    x = X0 + col * (CW + GAP)
    y = PY1 if row == 0 else PY2
    
    if is_focal:
        d.box(x, y, CW, CH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 0.9)
    
    # 카드 상단 헤더: 절 칩 + 제목 + 부제목 2줄 분리
    d.chip(x + 28, y + 20, sec, card_c, 11)
    d.t(x + 50, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 50, y + 42, role, 11, SOFT, KR, "start")
    
    d.line(x + 12, y + 54, x + CW - 12, y + 54, RULE, 0.8)
    
    # 3개 항목
    iy0 = y + 78
    for idx, (head, sub) in enumerate(items):
        iy = iy0 + idx * 46
        d.box(x + 12, iy - 14, CW - 24, 38, PAPER, RULE, 0.6)
        d.t(x + 20, iy, head, 12, INK, KR, "start", 600)
        d.t(x + 20, iy + 16, sub, 11, MUTED, KR, "start")

d.legend(LEG, [
    ("핵심 (focal)", ACC),
    ("안전 보장", OK),
    ("구조·추상", INFO),
    ("주의·제약", WARN),
    ("위험·오염", BAD),
])

d.save("08-01.chapter-overview.svg")
