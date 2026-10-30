# 06-01 개요 — 단일 리더 복제 구조에서 출발해 동기화 트레이드오프, 백업과의 목적 분리, 다운타임 없는 신규 팔로워 셋업으로 이어지는 전체 지도.
# 사실 출처: 06-01 서두(L21~L23), §1(L27~L39), §2(L44~L54), §3(L56~L63), §4(L65~L76)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "06-01 · CHAPTER OVERVIEW", "단일 리더 복제와 동기화·백업·신규 팔로워 전체 지도",
      "단일 리더 복제 구조(§1), 동기·비동기 트레이드오프(§2), 백업과 복제의 차이(§3), 신규 팔로워 셋업(§4)을 조망한다.",
      "단일 리더 쓰기 전담 · 동기·비동기 트레이드오프 · 실수 삭제와 백업 보완 · 무중단 신규 팔로워 셋업")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "복제하는 이유: 지연 감소 · 가용성·내구성 · 읽기 처리량", 12, INK, KR, "middle", 600)

CW = 196
GAP = 12
X0 = 32

cards = [
    ("§1", "단일 리더 구조", "쓰기 전담과 복제 로그 전파",
     [("리더 로컬 쓰기", "새 데이터 로컬 저장소 기록"),
      ("복제 로그 스트림", "모든 팔로워 순차 전파"),
      ("읽기 질의 분산", "모든 레플리카 읽기 분담")],
     INFO),
    ("§2", "동기화 트레이드오프", "최신성 vs 견고성 절충",
     [("동기 복제 보장", "팔로워 최신성 · 장애 시 대기"),
      ("비동기 복제 처리", "리더 진행 유지 · 내구성 약화"),
      ("반동기 절충 구성", "동기 하나 · 나머지 비동기")],
     ACC),
    ("§3", "백업과 복제", "목적 분리와 상호 보완",
     [("실시간 복제 전파", "실수 삭제도 모든 사본 확산"),
      ("불변 스냅샷 보존", "과거 시점 복원 목적 백업"),
      ("오브젝트 스토어", "로그 아카이브와 백업 연계")],
     WARN),
    ("§4", "신규 팔로워 셋업", "다운타임 없는 노드 추가",
     [("일관 스냅샷", "전체 잠금 없는 시점 캡처"),
      ("로그 위치 연계", "LSN · binlog · GTID"),
      ("변경분 따라잡음", "스냅샷 이후 밀린 변경 처리")],
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
    d.chip(x + 28, PY + 24, sec, card_c, 11)
    d.t(x + CW / 2 + 12, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64

        if is_focal and j == 2:
            d.tone(x + 8, iy, CW - 16, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 1:
            d.tone(x + 8, iy, CW - 16, 52, INFO, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, INFO, KR, "middle")
        elif i == 2 and j == 0:
            d.tone(x + 8, iy, CW - 16, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif i == 3 and j == 2:
            d.tone(x + 8, iy, CW - 16, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 8, iy, CW - 16, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 1, y), (x2 - 3, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("동기화 절충 (focal)", ACC), ("단일 리더 쓰기·읽기", INFO), ("실수 삭제 전파 주의", WARN), ("따라잡음", OK)])
d.save("06-01.chapter-overview.svg")
