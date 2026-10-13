# 타입 스펙: type-process — URL 하나(/wiki/Kay_Hagan)가 프론티어에서 나가 다운로드되고, 그 페이지에서 나온 새 링크(/wiki/John_Conyers)가 다시 프론티어로 돌아오는 한 바퀴. 카드마다 그 단계의 실제 값을 싣는다.
# 사실 출처: 추출본 v2.txt 2450~2466행(11 단계 흐름), PDF 138쪽 링크 추출 그림의 href 값(/wiki/Cong_Weixi·/wiki/Kay_Hagan·/wiki/Vladimir_Bukovsky·/wiki/John_Conyers)과 접두 https://en.wikipedia.org,
#   표 매핑 en.wikipedia.org → b1(PDF 142쪽 표, 호스트 이름은 en.wikipedia.org 로 통일), 203.0.113.7 은 RFC 5737 문서용 주소(예시),
#   SHA-256 48d2b36e… 는 본문 예시 HTML `<html><body><h1>Kay Hagan</h1></body></html>` 을 python hashlib 로 계산한 값, 200·text/html 은 HTTP 응답 예시.
# Layout conventions: 카드 폭 204·높이 124, x stride 228(48·276·504·732), 줄 stride 172(y=104·276), 되돌림 통로 x=24·y=428. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 540
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 09-01 §2",
      "URL 하나가 프론티어를 나가 새 URL 을 낳고 돌아온다",
      "프론티어가 URL 을 내보내 DNS 와 다운로더를 거치고, 내려받은 페이지의 링크가 필터와 중복 검사를 지나 다시 프론티어로 들어간다.",
      "Kay_Hagan 을 내려받아 John_Conyers 를 얻는 한 바퀴")

CW, CH = 204, 124
XS = (48, 276, 504, 732)
YS = (104, 276)
CARDS = (
    ("1", "프론티어", "b1 · en.wikipedia.org", "/wiki/Kay_Hagan", INFO),
    ("2", "DNS 해석", "en.wikipedia.org", "→ 203.0.113.7", INFO),
    ("3", "다운로드", "GET /wiki/Kay_Hagan", "200 · text/html", INFO),
    ("4", "파서 · 내용 검사", "SHA-256 48d2b36e…", "처음 본 내용 → 저장", INFO),
    ("5", "링크 추출", "href 4 개 중 하나", "/wiki/John_Conyers", INFO),
    ("6", "절대 경로로", "https://en.wikipedia.org", "/wiki/John_Conyers", INFO),
    ("7", "필터 · 본 적 있나", "필터 통과", "URL Seen? 없음", INFO),
    ("8", "프론티어", "b1 · en.wikipedia.org", "/wiki/John_Conyers", ACC),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, v1, v2, c) in enumerate(CARDS):
    row, col = (0, i) if i < 4 else (1, i - 4)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 14, y + 56, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 88, v1, 13 if fam(v1) == KR else 12, MUTED, fam(v1), "start")
    d.t(x + 14, y + 108, v2, 13 if fam(v2) == KR else 12, MUTED, fam(v2), "start")

for i in range(7):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
# 4 → 5: 줄 바꿈은 카드 사이 빈 줄 y=252 를 지난다.
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)
# 8 → 1: 왼쪽 여백 통로로 되돌아간다.
d.arrow([(pos[7][0] + CW // 2, YS[1] + CH + 4), (pos[7][0] + CW // 2, 428), (24, 428), (24, YS[0] + 62), (XS[0] - 6, YS[0] + 62)], ACC, "acc", 1.5, "5 4")
d.chip(480, 428, "새 URL 이 1 로 돌아감", ACC, 13)

d.legend(H - 56, [("처리 단계", INFO), ("한 바퀴를 닫는 자리", ACC)])
d.save("09-01.url-journey.svg")
