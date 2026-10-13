# 타입 스펙: type-process — 코드를 읽는 모델을 만들고 문제마다 풀이를 대량으로 뽑은 뒤 걸러 내 열 개 이하만 제출하는 다섯 단계. 칸마다 단계·값·결과가 같은 자리에 반복되고 화살표가 순서를 나른다.
# 사실 출처: DeepMind 글 "Competitive programming with AlphaCode"(pre-train on GitHub code, fine-tune on competitive programming dataset, massive C++·Python samples, filter·cluster·rerank to 10 candidates, 10 recent Codeforces contests) https://deepmind.google/discover/blog/competitive-programming-with-alphacode/ 와 arXiv 2203.07814 초록(평균 순위 상위 54.3%, 참가자 5,000 명 넘는 대회). 추출본 v1.txt 2510~2525행, PDF 쪽 102 그림.
# Layout conventions: 카드 폭 168·높이 212, 가로 stride 184(x=20+184k), 카드 y=112, 화살표는 카드 중앙 y=218. 5 카드. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 08-01 §5",
      "AlphaCode 는 대량으로 만든 뒤 열 개만 낸다",
      "문제 하나에 표본을 쏟아붓고 필터·군집·재순위로 줄여 후보 열 개 이하를 제출합니다",
      "Codeforces 10 개 대회에서 평균 상위 54.3%")

CW, CH, STRIDE, X0, Y0 = 168, 212, 184, 20, 112
cards = [
    ("1", "사전 학습", "GitHub 코드", "트랜스포머 모델", "코드를 읽는 모델", INFO),
    ("2", "미세 조정", "CodeContests", "문제와 풀이", "대회용 데이터", INFO),
    ("3", "표본 생성", "C++ · Python", "문제 하나에 대량", "풀이 후보의 바다", INFO),
    ("4", "거르기", "필터 → 군집 → 재순위", "후보 10 개 이하", "행동으로 줄임", ACC),
    ("5", "제출과 판정", "Codeforces 10 개 대회", "상위 54.3%", "중간 순위", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, KR, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, KR if any("가" <= ch <= "힣" for ch in v1) else MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("거르는 단계", ACC), ("학습·생성·평가", INFO)])
d.save("08-01.alphacode-process.svg")
