# 타입 스펙: type-layers — 캐시 다섯 층을 같은 폭 띠로 쌓고, 띠마다 안쪽 구분 칩과 키 → 값 예시 한 줄을 둔다. focal 은 ID 만 담는 뉴스 피드 층 하나.
# 사실 출처: 추출본 v2.txt 3113~3125행·PDF 175쪽 그림(News Feed: news feed / Content: hot cache · normal / Social Graph: follower · following / Action: liked · replied · others / Counters: like counter · reply counter · other counters). 키 → 값 예시는 설명용 값.
# Layout conventions: 띠 폭 832(x=64)·높이 64, y stride 76(y=100 부터), 이름 x+20, 칩 폭 88·높이 28·간격 100(x+176 부터), 예시 글자는 오른쪽 끝 x+812. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 960, 548
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 11-01 §6",
      "캐시 다섯 층은 담는 것의 모양이 서로 다르다",
      "뉴스 피드 층은 게시물 ID 목록만, 콘텐츠 층은 게시물 객체와 핫 캐시, 소셜 그래프 층은 팔로워와 팔로잉, 행동 층은 좋아요와 답글 여부, 카운터 층은 수를 담는다.",
      "층 이름 · 안쪽 구분 · 키에서 값으로")

X, LW, LH, LS, Y0 = 64, 832, 64, 76, 100
LAYERS = (
    ("뉴스 피드", ("피드",), "user 12 → 9003 · 9001", True),
    ("콘텐츠", ("핫 캐시", "일반"), "post 9001 → 게시물 객체", False),
    ("소셜 그래프", ("팔로워", "팔로잉"), "user 7 → 팔로워 · 팔로잉", False),
    ("행동", ("좋아요", "답글", "기타"), "(user 12, post 9001) → 좋아요", False),
    ("카운터", ("좋아요 수", "답글 수", "기타 수"), "post 9001 → 좋아요 수", False),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


for i, (name, chips, ex, focal) in enumerate(LAYERS):
    y = Y0 + LS * i
    if focal:
        d.o.append(f'<rect x="{X}" y="{y}" width="{LW}" height="{LH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        col = ACC
    else:
        d.box(X, y, LW, LH, PAPER2, RULE, 1.0, 6)
        col = INFO
    d.t(X + 20, y + 38, name, 15, INK, KR, "start", 600)
    for k, c in enumerate(chips):
        cx = X + 176 + 100 * k
        d.o.append(f'<rect x="{cx}" y="{y + 18}" width="88" height="28" rx="4" fill="{col}22" stroke="{col}" stroke-width="1.1"/>')
        d.t(cx + 44, y + 38, c, 13, col, KR, "middle")
    d.t(X + 812, y + 38, ex, 13, MUTED, fam(ex), "end")

d.legend(H - 56, [("캐시 층의 안쪽 구분", INFO), ("ID 만 담는 층", ACC)])
d.save("11-01.cache-layers.svg")
