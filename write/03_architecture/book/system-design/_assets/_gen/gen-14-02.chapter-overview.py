# 타입 스펙: type-process — 절 아홉을 카드 슬롯(절 번호·이름·핵심 값)으로 세 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §3(자원 관리자).
# 사실 출처: 구조는 추출본 v2.txt 4094~4178행(전처리기·DAG 스케줄러·자원 관리자·작업 서버·임시 저장소·인코딩된 영상)·4179~4275행(속도·보안·비용)·4276~4304행(오류 처리)·4305~4324행(마무리),
#   PDF 231~240쪽 그림. 카드 값은 본문 §1~§9 의 값이다.
# Layout conventions: 카드 폭 288·높이 124, x stride 312(24·336·648), 줄 stride 172(y=104·276·448). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, KR, MONO

W, H = 960, 656
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-02",
      "트랜스코딩을 아홉 절로 읽는다",
      "전처리기·DAG 스케줄러·자원 관리자·작업 서버가 변환을 나누고, 속도·보안·비용·오류가 그 위에서 다듬어지며, 시간이 남으면 확장·라이브·삭제로 넓힌다.",
      "구조 넷 → 다듬기 넷 → 넓히기")

CW, CH = 288, 124
XS = (24, 336, 648)
YS = (104, 276, 448)
CARDS = (
    ("§1", "전처리기", "GOP 조각 · DAG", INFO),
    ("§2", "DAG 스케줄러", "단계 1 → 단계 2", INFO),
    ("§3", "자원 관리자", "큐 셋 · 스케줄러", ACC),
    ("§4", "작업 서버", "종류별 서버 풀", INFO),
    ("§5", "속도", "조각 · 지점 · 큐", OK),
    ("§6", "보안", "사전 서명 URL", OK),
    ("§7", "비용", "인기 영상만 CDN", OK),
    ("§8", "오류", "재시도 · 대체", WARN),
    ("§9", "넓히기", "라이브 · 삭제", MUTED),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = divmod(i, 3)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c if c != MUTED else SOFT, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 13 if fam(val) == KR else 12, MUTED, fam(val), "start")

for i in range(8):
    x, y = pos[i]
    if i % 3 != 2:
        d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
    else:
        # 줄 끝에서 다음 줄 처음으로 읽는 순서를 잇는다.
        yb = y + CH + 24
        d.arrow([(x + CW // 2, y + CH + 4), (x + CW // 2, yb), (pos[i + 1][0] + CW // 2, yb), (pos[i + 1][0] + CW // 2, pos[i + 1][1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("구조", INFO), ("가장 중심인 절", ACC), ("다듬기", OK), ("오류", WARN), ("넓히기", MUTED)])
d.save("14-02.chapter-overview.svg")
