# 14-02 개요 — 행동 데이터 추적이 감시로 바뀌는 지점(§1), 감시 어휘 치환 사고실험(§2), 자유로운 동의의 한계(§3), 프라이버시 결정권의 본질(§4) 전체 지도.
# 사실 출처: 14-02 본문 서두(L16~L18), §1(L29~L35), §2(L45~L51), §3(L57~L71), §4(L77~L85), 원서 Ch.14 PDF p.6~7 Privacy and Tracking, p.7~8 Surveillance, p.8~10 Consent, p.10~12 Privacy and Use of Data
# 10-31 검증(cc-ddia-dverify14): 배너 INFO→중립(§1 범례 색과 겹침), 항목이 넷인데 '3대 한계' 라 한 제목, 본문에 없는 '센서' 를 고침
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 96
BANNER_H = 44
CARD_Y = 160
CARD_H = 248
LEG = 432
H = LEG + 56

d = D(W, H, "14-02 · CHAPTER OVERVIEW", "프라이버시와 감시·동의의 한계 전체 지도",
      "행동 데이터 수집이 감시로 바뀌는 경로, 동의의 한계, 프라이버시 결정권의 이전을 4개 절로 연결한 전체 지도.",
      "행동 데이터 추적 · 빅데이터 어휘 사고실험 · 동의의 구조적 비대칭 · 프라이버시 결정권의 이전")

# 상단 공통 전제 배너 (INFO 는 §1 범례 색이라 중립 박스로 둔다)
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 18, "행동 데이터 수집과 프라이버시: 서비스 제공에서 감시 인프라로의 전환", 13, INK, KR, "middle", 600)
d.t(W / 2, BANNER_Y + 34, "명시적 입력과 부수효과 추적의 갈림길 · 광고 비즈니스 모델 · 결정권 이전 메커니즘", 12, MUTED, KR, "middle")

# 4개 컬럼 기하 (CW=196, GAP=16, X0=24)
CW = 196
GAP = 16
X0 = 24
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]

# 루트 배너 → 4개 카드 배선 버스
BUS_Y = 150
d.line(W / 2, BANNER_Y + BANNER_H, W / 2, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[3], BUS_Y, RULE, 1.2)
for i in range(4):
    d.line(cx[i], BUS_Y, cx[i], CARD_Y, ACC if i == 2 else RULE, 1.2)

# 카드 간 수평 연결 화살표
for i in range(3):
    x_start = X0 + i * (CW + GAP) + CW
    x_end = X0 + (i + 1) * (CW + GAP)
    d.arrow([(x_start, CARD_Y + 124), (x_end, CARD_Y + 124)], MUTED, "ar", 1.2)

cards = [
    ("추적 → 감시", "§1", [
        "명시적 입력 데이터 처리",
        "부수효과 행동 추적 기록",
        "광고 기반 비즈니스 모델",
        "광고주 중심 이해 충돌"
    ], INFO, False),
    ("감시로 바꿔 읽기", "§2", [
        "데이터→감시 어휘 치환",
        "실시간 감시 스트림 저장",
        "인터넷 연결 마이크",
        "거대 대중 감시 인프라"
    ], WARN, False),
    ("동의의 한계", "§3", [
        "광고 프로필 필요성 불분명",
        "정책 불투명·이해 불가",
        "일방향 데이터 추출 관계",
        "필수 서비스로 거부 불가"
    ], ACC, True),
    ("프라이버시=결정권", "§4", [
        "비밀 유지 아닌 결정권",
        "공개 대상·목적 선택 자율",
        "개인에서 기업으로 이전",
        "기업의 이윤 극대화 행사"
    ], OK, False),
]

for i, (title, sec_chip, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, CARD_Y, CW, CARD_H, color, 6, "14", 1.4)
    else:
        d.box(x, CARD_Y, CW, CARD_H, PAPER2, RULE, 1.0)

    # 섹션 칩과 제목
    chip_x = x + 30
    d.chip(chip_x, CARD_Y + 22, sec_chip, color, 12, pad=5)
    d.t(x + CW / 2 + 16, CARD_Y + 26, title, 13, INK, KR, "middle", 600)
    d.line(x + 10, CARD_Y + 42, x + CW - 10, CARD_Y + 42, RULE, 0.8)

    # 4개 항목
    for j, it in enumerate(items):
        iy = CARD_Y + 62 + j * 44
        d.box(x + 8, iy - 13, CW - 16, 30, PAPER, RULE, 0.6, r=4)
        d.t(x + CW / 2, iy + 6, it, 12, INK if not is_focal else color, KR, "middle")

# 범례
d.legend(LEG, [
    ("추적과 감시", INFO),
    ("감시 어휘 치환", WARN),
    ("동의의 한계 (focal)", ACC),
    ("결정권의 본질", OK)
])

d.save("14-02.chapter-overview.svg")
