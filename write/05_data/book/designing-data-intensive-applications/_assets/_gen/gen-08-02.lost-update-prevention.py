# 08-02 §4 — 두 트랜잭션이 읽기-수정-쓰기를 동시 수행할 때 발생하는 갱신 손실을 막는 4대 기법(원자적 쓰기, 명시적 잠금, 자동 감지, 조건부 쓰기 CAS) 비교.
# 사실 출처: 08-02 본문 §4(L74~L92), 원서 Ch.8 "Preventing Lost Updates"(PDF p.24~28: 위키 임의 텍스트 p.25, FOR UPDATE·잠금 누락·데드락 p.26, 자동 감지·재시도·CAS p.27, optimistic locking·다중 리더 p.28)
# 타입 스펙: type-dp-security-matrix
# 검증(10-31 cc-ddia-dverify08): 본문·원서에 없는 라벨(비관적 락, RMW, 처리량 감소, 스냅샷 격리 자동화, 단일 객체 저장소, 비동기 복제, old_val)을 원서 대목으로 바꾸고, 데드락 칸에 붙은 잠금 누락 설명을 나눔
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 300
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "08-02 · §4 LOST UPDATE PREVENTION", "갱신 손실(Lost Update) 방지 4대 기법 비교",
      "동시 읽기-수정-쓰기 충돌을 막는 4가지 기법의 동작 원리와 한계를 비교한다.",
      "원자적 쓰기 연산 · 명시적 잠금 · 자동 갱신 손실 감지 · 조건부 쓰기 CAS")

# 상단 공통 문제 배경 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, WARN, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "갱신 손실: 두 클라이언트가 카운터 42를 동시 수정하여 44가 아닌 43이 되는 현상", 12, INK, KR, "middle", 600)

CW = 196
GAP = 12
X0 = 32

cols = [
    ("원자적 쓰기 연산", "내장 연산",
     [("UPDATE counters", "DB 내장 원자 연산"),
      ("사이클 불필요", "읽기-수정-쓰기 없음"),
      ("가장 단순", "가능하면 이 방법"),
      ("표현 한계", "위키 임의 텍스트 편집")],
     OK),
    ("명시적 잠금", "앱이 직접 잠금",
     [("SELECT FOR UPDATE", "읽은 행 잠근 뒤 수정"),
      ("쿼리로 표현 못 할 검증", "체스 말 이동"),
      ("잠금 누락 위험", "잠금 하나 누락 · 버그"),
      ("데드락 위험", "여러 객체 잠금 시")],
     WARN),
    ("자동 갱신 감지", "엔진 내장",
     [("갱신 손실 자동 감지", "트랜잭션 중단"),
      ("특별한 앱 코드 불필요", "DB가 감지·중단"),
      ("엔진별 지원 편차", "PG·오라클 지원 · MySQL 미지원"),
      ("앱 재시도 필수", "중단 트랜잭션 재실행")],
     INFO),
    ("조건부 쓰기 (CAS)", "낙관적 락",
     [("content = '옛 내용'", "읽은 값일 때만 쓰기"),
      ("트랜잭션 없는 DB", "조건부 쓰기 연산 제공"),
      ("MVCC 예외 주의", "WHERE 절 미커밋 쓰기 노출"),
      ("다중 리더 한계", "단일 최신 복사본 가정")],
     BAD),
]

FOCAL = 0

for i, (title, chip_txt, items, c_accent) in enumerate(cols):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 열 외곽 상자
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, OK, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 열 헤더: 제목 + 태그
    d.t(x + CW / 2, PY + 24, title, 13, INK, KR, "middle", 600)
    d.chip(x + CW / 2, PY + 46, chip_txt, c_accent, 11)
    d.line(x + 12, PY + 60, x + CW - 12, PY + 60, RULE, 0.8)

    # 4개 행 항목
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 70 + j * 54

        if is_focal and j == 2:
            d.tone(x + 8, iy, CW - 16, 46, OK, 4, "20", 1.2)
            d.t(x + CW / 2, iy + 18, top_txt, 11, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 11, OK, KR, "middle")
        elif i == 1 and j == 2:
            d.tone(x + 8, iy, CW - 16, 46, WARN, 4, "1C", 1.2)
            d.t(x + CW / 2, iy + 18, top_txt, 11, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 11, WARN, KR, "middle")
        elif i == 2 and j == 2:
            d.tone(x + 8, iy, CW - 16, 46, INFO, 4, "1C", 1.2)
            d.t(x + CW / 2, iy + 18, top_txt, 11, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 11, INFO, KR, "middle")
        elif i == 3 and j == 2:
            d.tone(x + 8, iy, CW - 16, 46, BAD, 4, "1C", 1.2)
            d.t(x + CW / 2, iy + 18, top_txt, 11, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 11, BAD, KR, "middle")
        else:
            d.box(x + 8, iy, CW - 16, 46, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 18, top_txt, 11, INK, MONO if not any("가" <= ch <= "힣" for ch in top_txt) else KR, "middle", 600)
            d.t(x + CW / 2, iy + 34, bot_txt, 11, MUTED, KR, "middle")

d.legend(LEG, [("원자 연산 가장 단순 (focal)", OK), ("엔진 감지 지원", INFO), ("잠금 누락·데드락 주의", WARN), ("MVCC 예외 주의", BAD)])
d.save("08-02.lost-update-prevention.svg")
