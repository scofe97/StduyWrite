# 타입 스펙: type-sequence — 받는 쪽 · 레지스트리 · 이미지 관리자 세 레인의 시간순 pull. 오늘 :1.0 → 이미지 A, 관리자가 재태그, 내일 :1.0 → 이미지 B, 같은 시점의 @sha256 → 이미지 A. 위쪽 띠는 다이제스트가 나오는 길(층 blob → 매니페스트 → 해시). focal 은 다이제스트 노드.
# 사실 출처: 노트 L197~L199(blob · 매니페스트 · 다이제스트), L205~L214(참조 두 방식 · 태그는 옮겨 다님 · 해시 참조는 동일한 이미지), L216(관리자가 재태그하면 다음 pull 에 최신 패치).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, Seq, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 984, 788
NW, NH = 232, 56
SX = [48, 376, 704]                 # 위쪽 띠 노드 x
SY = 108                            # 위쪽 띠 y


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = Seq(W, H, "CONTAINER SECURITY · 06-01 §5",
        "태그는 오늘과 내일 다른 이미지를 주고, 다이제스트는 늘 같은 이미지를 줍니다",
        "위쪽 띠는 층 blob 에서 이미지 매니페스트를 거쳐 다이제스트가 나오는 길이다. 아래 시퀀스에서 받는 쪽이 pull :1.0 으로 이미지 A 를 받은 뒤 "
        "이미지 관리자가 :1.0 을 이미지 B 로 재태그하면, 내일의 pull :1.0 은 이미지 B 를 돌려주고 pull @sha256 다이제스트는 여전히 이미지 A 를 돌려준다.",
        lead="다이제스트는 이미지 매니페스트의 해시라서 이미지가 바뀌면 달라집니다.")


def strip_node(j, title, sub, c=None):
    x = SX[j]
    fit(title, 13, NW - 16)
    fit(sub, 12, NW - 16)
    if c:
        d.tone(x, SY, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, SY, NW, NH)
    d.t(x + NW / 2, SY + 24, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, SY + 44, sub, 12, MUTED, kr(sub), "middle")


def strip_arrow(j, label):
    y = SY + NH / 2
    x1, x2 = SX[j] + NW, SX[j + 1]
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 12, MUTED, KR, "middle", 600)


strip_node(0, "층 blob", "내용의 해시로 식별", None)
strip_node(1, "이미지 매니페스트", "층 blob 의 집합을 식별", None)
strip_node(2, "다이제스트", "sha256:<digest>", ACC)
strip_arrow(0, "집합")
strip_arrow(1, "해시")

LY0 = 212
d.lanes([("받는 쪽", "docker pull"), ("레지스트리", "registry"), ("이미지 관리자", "push · tag")], y0=LY0)
d.rails(708)
R, G, M = "받는 쪽", "레지스트리", "이미지 관리자"

# 오늘
d.chip(48, 296, "오늘", MUTED, 12, 7)
d.msg(R, G, "pull :1.0", 300, MUTED, sub="태그로 요청")
d.state(G, ":1.0 → A", 332, INFO)
d.msg(G, R, "sha256:<digest A>", 372, INFO, dash="5 4", sub="이미지 A")
d.msg(M, G, "tag :1.0 → B", 428, MUTED, sub="패치본으로 재태그")
d.state(G, ":1.0 → B", 456, WARN)

# 내일
d.line(24, 488, 936, 488, RULE, 1.0, "4 6")
d.chip(48, 488, "내일", MUTED, 12, 7)
d.msg(R, G, "pull :1.0", 528, MUTED, sub="같은 태그로 요청")
d.msg(G, R, "sha256:<digest B>", 584, WARN, dash="5 4", sub="이미지 B, 오늘과 다름")
d.msg(R, G, "pull @sha256:<digest A>", 640, OK, sub="다이제스트로 요청")
d.msg(G, R, "sha256:<digest A>", 696, INFO, dash="5 4", sub="이미지 A, 오늘과 같음")

d.legend(732, [("이미지 A", INFO), ("이미지 B", WARN), ("다이제스트로 요청", OK), ("다이제스트가 나오는 길", ACC)])
d.save(str(ASSETS / "06-01.tag-vs-digest.svg"))
print("ok 06-01 tag-vs-digest")
