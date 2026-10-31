# 09-03 개요 — 진실·거짓·시스템 모델 전체 지도
# 사실 출처: 09-03 서두(L13~L19), §1(L23~L33), §2(L35~L43), §3(L45~L57), §4(L59~L69), §5(L71~L96)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 246
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "09-03 · CHAPTER OVERVIEW", "진실·거짓·시스템 모델 전체 지도",
      "비신뢰 네트워크와 불완전한 시계 환경에서 분산 시스템이 진실을 규정하고 올바름을 보장하는 체계",
      "단일 노드 불신 · 만료 미인지 좀비 · 단조 펜싱 토큰 · 비잔틴 장애 경계 · 시스템 모델")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "핵심 과제: 단일 노드의 자체 판단을 불신하고, 과반수 투표와 펜싱 토큰으로 진실을 강제함", 12, INK, KR, "middle", 600)

CW = 158
GAP = 12
X0 = 24

cards = [
    ("§1", "다수결 원칙", "단일 노드 불신",
     [("비대칭 장애", "송신 두절 노드 고립"),
      ("판단 배제", "자체 생존 주장 불신"),
      ("진실 결정", "과반수 쿼럼 투표")],
     WARN),
    ("§2", "분산 락의 함정", "좀비 쓰기 위험",
     [("리스 만료", "GC 포즈 중 권한 상실"),
      ("오판 재개", "유효 착각 후 쓰기 시도"),
      ("이상 현상", "스플릿 브레인 오염")],
     BAD),
    ("§3", "펜싱 토큰", "단조 토큰 방어",
     [("발급 규칙", "락 서비스 번호 증가"),
      ("저장소 검증", "최신 미만 요청 거부"),
      ("방어 범위", "좀비 및 지연 차단")],
     ACC),
    ("§4", "비잔틴 장애", "기만 노드 경계",
     [("가정 붕괴", "모순된 거짓 투표 전송"),
      ("비용 한계", "2/3 초과 정상 노드"),
      ("실용 방어", "체크섬 · 입력 검증")],
     INFO),
    ("§5", "시스템 모델", "모델 가정·보장",
     [("현실 모델", "부분 동기 + 크래시-복구"),
      ("안전성", "나쁜 일 미발생 (항상)"),
      ("활동성", "좋은 일 발생 (조건부)")],
     MUTED),
]

FOCAL = 2

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 카드 헤더
    d.box(x, PY, CW, 32, PAPER, RULE, 0.7)
    d.t(x + 10, PY + 21, sec, 11, ACC if is_focal else SOFT, MONO, "start", 700)
    d.t(x + CW - 10, PY + 21, role, 11, card_c, KR, "end", 600)

    # 섹션 타이틀
    d.t(x + CW / 2, PY + 56, title, 13, INK, KR, "middle", 700)
    d.line(x + 14, PY + 68, x + CW - 14, PY + 68, RULE, 0.6)

    # 내부 아이템
    iy = PY + 92
    for label, desc in items:
        d.tone(x + 8, iy - 14, CW - 16, 44, card_c if is_focal else RULE, 4, "10" if is_focal else "08", 0.8)
        d.t(x + 14, iy + 2, label, 11, card_c if is_focal else INK, KR, "start", 600)
        d.t(x + 14, iy + 20, desc, 11, MUTED, KR, "start")
        iy += 52

d.legend(LEG, [
    ("노드 불신", WARN),
    ("좀비 위험", BAD),
    ("펜싱 방어 (focal)", ACC),
    ("기만 경계", INFO),
    ("가정·보장", MUTED),
])

d.save("09-03.chapter-overview.svg")
