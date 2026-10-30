# 05-01 개요 — 롤링 업그레이드로 인한 공존 환경 위에서 인코딩·호환성·언어 특정 형식의 세 절을 잇는 전체 지도.
# 사실 출처: 05-01 서두(L21~L23), §1(L33~L45), §2(L52~L61), §3(L71~L78)
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

d = D(W, H, "05-01 · CHAPTER OVERVIEW", "인코딩과 호환성 기초 전체 지도",
      "롤링 업그레이드로 인한 공존 환경에서 두 데이터 표현의 번역, 양방향 호환성, 언어 내장 직렬화의 한계를 잇는다.",
      "인메모리·바이트 번역 · 롤링 업그레이드 공존 · 양방향 호환성 · 언어 내장 직렬화 회피")

# 상단 배포 현실 배너 (공통 전제 축)
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 23, "배포 현실: 롤링 업그레이드와 점진 배포로 옛·새 코드와 데이터 공존", 12, INK, KR, "middle", 600)

CW = 252
GAP = 26
X0 = 36

cards = [
    ("§1", "인코딩과 디코딩", "두 데이터 표현의 번역",
     [("인메모리 객체", "CPU 효율 접근 · 포인터"),
      ("바이트 시퀀스", "파일·네트워크용 자족적 직렬화"),
      ("zero-copy 대안", "명시적 변환 단계 없음")],
     INFO),
    ("§2", "호환성 두 방향", "점진 배포 공존 요구",
     [("양방향 호환성", "롤링 업그레이드 핵심 요건"),
      ("backward 호환", "새 코드가 옛 데이터 읽기"),
      ("forward 호환", "옛 코드가 새 필드 보존 필요")],
     ACC),
    ("§3", "언어 특정 형식", "회피 대상과 보안 취약점",
     [("내장 직렬화 API", "pickle · Serializable 편의성"),
      ("보안 원격 코드 실행", "임의 클래스 인스턴스화 위험"),
      ("일시적 용도 외 회피", "언어 종속 · 버전·효율 뒷전")],
     WARN),
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
    d.t(x + CW / 2 + 14, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64

        if is_focal and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 0 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        elif i == 2 and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(2):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("핵심 호환성 (focal)", ACC), ("데이터 표현과 번역", INFO), ("변환 생략 대안", OK), ("보안 취약점·주의", WARN)])
d.save("05-01.chapter-overview.svg")
