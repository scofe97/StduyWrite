# 01-03 개요 — 소프트웨어 제작과 운영의 아웃소싱 스펙트럼부터 클라우드 서비스 장단점, cloud native 레이어링, 저장·연산 분리, 멀티테넌시, DevOps 운영 전환까지 여섯 절의 전체 지도.
# 사실 출처: 01-03 본문 서두(L25~L29), §1(L36~L46), §2(L57~L70), §3(L79~L94), §4(L103~L109), §5(L116~L118), §6(L127~L150)
# 타입 스펙: type-architecture
import pathlib
import sys

_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_DIR))
sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
CW = 264
GAP = 20
X0 = 24

Y_B1 = 96
H_B1 = 28
Y1 = 132
PH = 216

Y_B2 = 360
H_B2 = 28
Y2 = 396

LEG = 636
H = LEG + 56

d = D(W, H, "01-03 · CHAPTER OVERVIEW", "클라우드 대 셀프 호스팅 전체 지도",
      "소프트웨어 제작·운영 주체 선택에서 cloud native 계층화·저장연산 분리·DevOps 운영까지 여섯 절을 조망한다.",
      "소프트웨어 제공 모델의 갈림과 cloud native 핵심 설계 축")

# 1행 상단 배너: 인프라 위치와 소프트웨어 모델 (§1 ~ §3)
d.box(X0, Y_B1, W - X0 * 2, H_B1, PAPER2, RULE, 0.9)
d.t(X0 + 16, Y_B1 + 18, "클라우드 선택과 cloud native 계층 · §1 ~ §3", 12, MUTED, KR, "start", 600)

# 2행 상단 배너: cloud native 아키텍처와 운영 (§4 ~ §6)
d.box(X0, Y_B2, W - X0 * 2, H_B2, PAPER2, RULE, 0.9)
d.t(X0 + 16, Y_B2 + 18, "저장·연산 분리·멀티테넌시·운영 · §4 ~ §6", 12, MUTED, KR, "start", 600)

cards = [
    # 1행 카드 (§1, §2, §3)
    (0, Y1, "§1", "아웃소싱 스펙트럼", "제작·운영 주체",
     [("맞춤 제작(bespoke)", "직접 작성 · 사내 운영"),
      ("기성품 셀프 호스팅", "on-prem · IaaS VM"),
      ("클라우드 SaaS", "외부 벤더 · API 접근")],
     INFO),
    (1, Y1, "§2", "서비스 장단점", "비용·통제 맞바꿈",
     [("빠른 시작과 전문성", "미숙한 시스템 학습 절감"),
      ("탄력적 확장", "피크 부하 유휴 방지"),
      ("통제 상실과 lock-in", "대안 이전 비용 위험")],
     WARN),
    (2, Y1, "§3", "서비스 레이어링", "하위 서비스 위 적층",
     [("cloud native 설계", "클라우드 활용 전제"),
      ("오브젝트 스토리지", "물리 머신 은닉 분산"),
      ("상위 서비스 적층", "S3 위 Snowflake 구축")],
     INFO),
    # 2행 카드 (§4, §5, §6)
    (0, Y2, "§4", "저장과 연산 분리", "독립 확장과 분리",
     [("로컬 디스크 한계", "인스턴스 교체 시 휘발"),
      ("가상 디스크 오버헤드", "I/O마다 네트워크 호출"),
      ("저장·연산 분리", "오브젝트 스토어와 분리")],
     ACC),
    (1, Y2, "§5", "멀티테넌시", "공유 하드웨어 격리",
     [("공유 하드웨어 처리", "여러 고객 데이터 수용"),
      ("더 나은 하드웨어 활용", "쉬운 확장 · 쉬운 관리"),
      ("자원 격리와 접근 제어", "독점 방지 · 테넌트 보호")],
     WARN),
    (2, Y2, "§6", "DevOps와 SRE", "서비스 통합과 비용",
     [("머신 관리 탈피", "OS 패치에서 서비스로"),
      ("재무·비용 최적화", "용량 계획 재무화"),
      ("위탁 불가 핵심 운영", "보안 유지 · 서비스 통합")],
     OK),
]

FOCAL = 3

for idx, (col, y, sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + col * (CW + GAP)
    is_focal = (idx == FOCAL)

    # 외곽 상자
    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목 + 역할
    d.chip(x + 28, y + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 12, y + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, y + 46, role, 12, SOFT, KR, "middle")
    d.line(x + 12, y + 56, x + CW - 12, y + 56, RULE, 0.8)

    # 내부 3개 항목
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = y + 66 + j * 48
        if is_focal and j == 2:
            d.tone(x + 10, iy, CW - 20, 42, ACC, 4, "18", 1.2)
            d.t(x + CW / 2, iy + 17, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 33, bot_txt, 12, ACC, KR, "middle")
        elif is_focal:
            d.tone(x + 10, iy, CW - 20, 42, ACC, 4, "0E", 0.9)
            d.t(x + CW / 2, iy + 17, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 33, bot_txt, 12, MUTED, KR, "middle")
        else:
            d.box(x + 10, iy, CW - 20, 42, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 17, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 33, bot_txt, 12, MUTED, KR, "middle")

# 1행 수평 연결 화살표 (§1 → §2 → §3)
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = Y1 + 22
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.2)

# 2행 수평 연결 화살표 (§4 → §5 → §6)
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = Y2 + 22
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.2)

d.legend(LEG, [
    ("저장·연산 분리 (focal)", ACC),
    ("위치와 적층", INFO),
    ("맞바꿈과 격리", WARN),
    ("운영 전환", OK),
])

d.save("01-03.chapter-overview.svg")
