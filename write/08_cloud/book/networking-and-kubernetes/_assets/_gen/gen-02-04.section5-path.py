# 02-04.section5-path — 패킷 하나가 §5 의 부품들을 지나는 전체 경로
# 본문 요구: §5 는 추적 켜기·엔트리 모양·NAT 변형·첫 패킷 발화를 소절로 나눠 다루는데,
#           그 넷이 한 패킷의 여정에서 어디에 놓이는지는 절 어디에도 없다. 절의 리드로 그것을 편다.
# 타입 스펙: type-flowchart.md — 두 판단이 갈래를 만든다(추적이 켜졌나 · 아는 연결인가).
#           모양이 종류를 나른다(타원=시작·끝, 마름모=판단, 사각=단계).
#           focal 은 논점 하나 — 아는 연결이면 규칙을 아예 안 거친다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 720
d = D(W, H, "SECTION 5 · ONE PACKET'S PATH",
      "패킷 하나가 지나는 자리에 이 절의 네 주제가 놓인다",
      "추적이 켜져 있어야 기록이 남고, 아는 연결이면 규칙을 거치지 않습니다. "
      "그래서 nat 규칙은 연결의 첫 패킷에서만 발화합니다.",
      lead="추적이 켜졌나, 아는 연결인가 — 두 판단이 경로를 가른다")

DW, DH, BW, BH = 340, 92, 224, 76
L, R = 316, 748

def oval(cx, cy, txt, c=MUTED, w=224, focal=False):
    if focal:
        d.o.append(f'<rect x="{cx-w//2}" y="{cy-22}" width="{w}" height="44" rx="20" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
    else:
        d.box(cx - w // 2, cy - 22, w, 44, PAPER2, c, 1.1, 20)
    d.t(cx, cy + 5, ddx.fit(txt, 12, w - 24, txt), 12, c, KR, "middle", 600)

def diamond(cx, cy, txt, sub):
    hw, hh = DW // 2, DH // 2
    d.path(f"M {cx} {cy-hh} L {cx+hw} {cy} L {cx} {cy+hh} L {cx-hw} {cy} Z", RULE, 1.2)
    d.t(cx, cy - 10, ddx.fit(txt, 12, DW - 48, txt), 12, INK, KR, "middle", 600)
    avail = int(2 * hw * (1 - 16 / hh)) - 24
    d.t(cx, cy + 16, ddx.fit(sub, 11, avail, f"sub@{cy}"), 11, SOFT, MONO)

def step(cx, cy, t, s, c=None):
    d.box(cx - BW // 2, cy - BH // 2, BW, BH, PAPER, c or RULE, 1.1, 6)
    d.t(cx, cy - 8, ddx.fit(t, 12, BW - 16, t), 12, c or INK, KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 11, BW - 14, s), 11, MUTED, KR)

oval(L, 172, "패킷이 FORWARD 를 지난다")
d.path(f"M {L} 194 L {L} {268-DH//2-8}", MUTED, 1.5, m="ar")
diamond(L, 268, "추적 훅이 등록돼 있나?", "-m conntrack 또는 nat 규칙")
d.path(f"M {L+DW//2} 268 L {R-112-8} 268", MUTED, 1.5, m="ar")
d.t((L + DW // 2 + R - 112) // 2, 256, "아니오", 11, SOFT, KR)
oval(R, 268, "아무 기록도 안 남는다")
d.t(R, 312, "conntrack -L → 0건", 11, SOFT, MONO)

d.path(f"M {L} {268+DH//2} L {L} {404-DH//2-8}", MUTED, 1.5, m="ar")
d.t(L + 14, 352, "예", 11, SOFT, KR, "start")
diamond(L, 404, "conntrack 이 아는 연결인가?", "응답 방향 튜플로 조회")

d.path(f"M {L+DW//2} 404 L {R-112-8} 404", ACC, 1.6, m="acc")
d.t((L + DW // 2 + R - 112) // 2, 392, "예", 11, ACC, KR)
step(R, 404, "저장된 튜플로 변환", "규칙을 아예 안 거친다", ACC)

d.path(f"M {L} {404+DH//2} L {L} {528-BH//2-8}", MUTED, 1.5, m="ar")
d.t(L + 14, 484, "아니오 — 첫 패킷", 11, SOFT, KR, "start")
step(L, 528, "nat 규칙을 훑는다", "카운터가 여기서 오른다", INFO)
d.path(f"M {L} {528+BH//2} L {L} {632-BH//2-8}", MUTED, 1.5, m="ar")
step(L, 632, "엔트리 생성", "튜플 두 줄이 정해진다", INFO)
d.path(f"M {L+BW//2} 632 L {R-BW//2-8} 632", MUTED, 1.5, m="ar")
step(R, 632, "변환 후 전달", "이후 패킷은 위 갈래로", None)

d.legend(680, [("첫 패킷만 지나는 길", INFO), ("이후 패킷 — 규칙을 건너뛴다", ACC)])
d.save("02-04.section5-path.svg")
print("ok section5-path")
