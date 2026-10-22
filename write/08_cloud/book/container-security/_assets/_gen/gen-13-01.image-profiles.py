# 타입 스펙: type-architecture — 이미지 → 이미지 프로파일 → 컨테이너로 이어지는 한 줄 위에서 프로파일이 다섯 축으로 갈라지고, 축마다 정상 값과 벗어났을 때의 이상 신호가 붙는다. focal 은 이미지 프로파일.
# 사실 출처: 노트 L40~L96(이미지 단위 프로파일, 상품 검색 서비스의 다섯 축), 축 둘 L60~L64(productsearch · bash/sh/zsh), 축 셋 L70(openat 20개+), 축 넷 L78(신원 하나 · 예상 밖 root), 축 다섯 L82~L94(seccomp · AppArmor · capability 7개).
#   축 셋·축 다섯의 이상 신호(집합 밖)는 노트가 명시하지 않고 프로파일 정의("필요한 집합")에서 도출했다.
# Layout conventions: 좌측 세로 사슬(x=28, w=152), 오른쪽 다섯 행 stride 76 · 높이 64(y=128부터), 열 x=244 · 496 · 776. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 960, 576


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 13-01 §1",
      "이미지 프로파일 하나가 다섯 축으로 모든 컨테이너를 단속합니다",
      "같은 이미지에서 뜬 컨테이너는 같게 동작한다. 그래서 이미지에 프로파일을 붙이고, 축마다 정상 값을 정해 벗어나면 이상 신호로 본다. "
      "축은 네트워크 트래픽, 실행 파일, 파일 접근, 사용자 ID, 시스템 콜과 capability다.",
      "정상 값은 상품 검색 서비스를 예로 들었습니다.")

AX, AW = 244, 212
NX, NW = 496, 240
EX, EW = 776, 156
RY0, RS, RH = 128, 76, 64

# 열 머리
d.t(AX, 112, "프로파일 축", 12, MUTED, KR, "start")
d.t(NX, 112, "정상 값", 12, OK, KR, "start", 600)
d.t(EX, 112, "벗어나면", 12, BAD, KR, "start", 600)

ROWS = [
    ("네트워크 트래픽", ("인그레스 · 로드 밸런서 웹 요청", "상품 DB로 연결 시작"), ("그 밖의 트래픽", None)),
    ("실행 파일", ("productsearch", "Go 실행 파일 하나"), ("bash · sh · zsh", "셸 실행 → 경보")),
    ("파일 접근", ("제한된 파일 위치 집합", "nginx 예 openat 20개+"), ("집합 밖 파일 접근", None)),
    ("사용자 ID", ("신원 하나", "컨테이너 하나, 일 하나"), ("다른 신원", "예상 밖 root")),
    ("시스템 콜 · capability", ("필요한 집합 (nginx 예 7개)", "→ seccomp · AppArmor"), ("집합 밖 호출", None)),
]
CY = [RY0 + RS * i + RH // 2 for i in range(5)]  # 행 중심

# 화살표를 먼저 — 프로파일 → 버스 → 축, 축 → 정상 → 이상
BUS = 216
d.line(180, CY[2], BUS, CY[2], SOFT, 1.3)
d.line(BUS, CY[0], BUS, CY[4], SOFT, 1.3)
for i, cy in enumerate(CY):
    d.arrow([(BUS, cy), (AX - 4, cy)], SOFT, "soft", 1.3)
    d.arrow([(AX + AW + 2, cy), (NX - 4, cy)], MUTED, "ar", 1.3)
    d.arrow([(NX + NW + 2, cy), (EX - 4, cy)], BAD, "bad", 1.3)

for i, (axis, normal, anomaly) in enumerate(ROWS):
    y = RY0 + RS * i
    cy = CY[i]
    # 축
    fit(axis, 14, AW - 24)
    d.box(AX, y, AW, RH, "#161B22", RULE, 1.0)
    d.t(AX + 16, cy + 5, axis, 14, INK, kr(axis), "start", 600)
    # 정상
    d.tone(NX, y, NW, RH, OK, 6, "12", 1.1)
    l1, l2 = normal
    fit(l1, 13, NW - 24)
    fit(l2, 12, NW - 24)
    d.t(NX + 16, y + 28, l1, 13, INK, kr(l1), "start", 600)
    d.t(NX + 16, y + 48, l2, 12, MUTED, kr(l2), "start")
    # 이상
    d.tone(EX, y, EW, RH, BAD, 6, "12", 1.1)
    a1, a2 = anomaly
    fit(a1, 13, EW - 24)
    if a2:
        fit(a2, 12, EW - 24)
        d.t(EX + 16, y + 28, a1, 13, INK, kr(a1), "start", 600)
        d.t(EX + 16, y + 48, a2, 12, BAD, kr(a2), "start")
    else:
        d.t(EX + 16, y + 38, a1, 13, INK, kr(a1), "start", 600)

# 좌측 사슬 — 이미지 → 프로파일 → 컨테이너
LX, LW = 28, 152
d.tone(LX, 148, LW, 72, INFO, 6, "14", 1.2)
d.t(LX + 16, 176, "이미지", 14, INK, KR, "start", 600)
d.t(LX + 16, 198, "productsearch", 12, MUTED, MONO, "start")
d.tone(LX, 280, LW, 64, ACC, 6, "1F", 1.4)
d.t(LX + 16, 308, "이미지 프로파일", 14, ACC, KR, "start", 600)
d.t(LX + 16, 328, "기대 동작 정의", 12, MUTED, KR, "start")
d.tone(LX, 392, LW, 72, INFO, 6, "14", 1.2)
d.t(LX + 16, 420, "컨테이너 × N", 14, INK, KR, "start", 600)
d.t(LX + 16, 442, "전부 같은 동작", 12, MUTED, KR, "start")
d.arrow([(LX + LW // 2, 222), (LX + LW // 2, 276)], INFO, "info", 1.4)
d.t(LX + LW // 2 + 12, 254, "정의", 12, MUTED, KR, "start")
d.arrow([(LX + LW // 2, 346), (LX + LW // 2, 388)], ACC, "acc", 1.4)
d.t(LX + LW // 2 + 12, 372, "단속", 12, MUTED, KR, "start")

d.legend(516, [("이미지 · 컨테이너", INFO), ("이미지 프로파일", ACC), ("정상 값", OK), ("이상 신호", BAD)])
d.save(str(ASSETS / "13-01.image-profiles.svg"))
print("ok 13-01 image-profiles")
