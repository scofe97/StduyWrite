# 타입 스펙: type-process — 절 아홉을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §5.
# 사실 출처: 추출본 v2.txt 4358~4401행(요구·추정)·4422~4457행(API)·4459~4503행(S3 이주)·4504~4520행(충돌)·4551~4577행(블록 서버)·4578~4604행(일관성·스키마)·4605~4651행(업로드·다운로드)·4652~4669행(롱 폴링)·4670~4717행(절약·장애),
#   계산: 20,000,000 ÷ 86,400 ≈ 231 → 240 · 10 GB ÷ 4 MB = 2,560 블록(10 GB = 10,240 MB).
# Layout conventions: 카드 폭 176·높이 124, x stride 192(24·216·408·600·792), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 1000, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 15-01",
      "Google Drive 를 아홉 절로 읽는다",
      "규모를 어림하고 단일 서버를 S3 로 옮긴 뒤, 충돌·블록·일관성을 거쳐 올리기와 내려받기 흐름, 알림, 절약과 장애로 이어 간다.",
      "추정 → API → 저장소 → 충돌 → 블록 → 일관성 → 흐름 → 알림 → 절약")

CW, CH = 176, 124
XS = (24, 216, 408, 600, 792)
YS = (104, 276)
CARDS = (
    ("§1", "요구와 추정", "10 TB · 480 QPS", INFO),
    ("§2", "API", "재개 가능 업로드", INFO),
    ("§3", "S3 로 이주", "샤딩 → 복제", INFO),
    ("§4", "동기화 충돌", "먼저 온 쪽이 승", INFO),
    ("§5", "블록 서버", "4 MB · 2·5 만", ACC),
    ("§6", "강한 일관성", "ACID · 여섯 표", INFO),
    ("§7", "올리기·내려받기", "pending → uploaded", INFO),
    ("§8", "롱 폴링", "30 s · changes", INFO),
    ("§9", "절약과 장애", "해시 · 콜드", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = (0, i) if i < 5 else (1, i - 5)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 13, c, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 13, MUTED, fam(val), "start")

for i in range(8):
    if i == 4:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[4][0] + CW // 2, YS[0] + CH + 4), (pos[4][0] + CW // 2, 252), (pos[5][0] + CW // 2, 252), (pos[5][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("15-01.chapter-overview.svg")
