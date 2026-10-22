# 타입 스펙: type-data-flow — uid 0 이 변환표를 지나 호스트의 uid 로 바뀌고 탈출 시 쥐는 권한이 갈린다. 매핑 없음 · 매핑 있음 두 줄 × 네 단계 (축약: 주체 lane 대신 경우 두 줄). focal 은 uid_map.
# 사실 출처: 노트 L87(탈출한 공격자는 평범한 사용자 권한), L89(한 번의 실수로 호스트를 통째로), L93~L101(uid_map 세 필드·vagrant 1000·0 1000 1), L216(기본적으로 전부 root).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 512
XS = [36, 252, 524, 740]
WS = [176, 232, 176, 208]
BH = 104
YA, YB = 176, 320


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "DATA-FLOW · 04-02 §2",
      "uid_map 이 있으면 컨테이너의 root 가 호스트에서는 비특권 uid 1000 입니다",
      "매핑이 없으면 컨테이너 안 uid 0 은 호스트에서도 root 이고, 탈출하면 호스트 root 권한을 쥔다. "
      "/proc/pid/uid_map 에 0 1000 1 을 쓰면 안쪽 시작 0, 호스트 시작 1000, 개수 1 로 컨테이너 root 가 호스트 uid 1000 에 대응하고, 탈출해도 평범한 사용자 권한만 쥔다.",
      lead="같은 uid 0 이 변환표를 지나며 호스트 쪽 번호가 바뀝니다.")

for x, w, h in zip(XS, WS, ("안에서 보이는 uid", "변환표", "호스트에서 보이는 uid", "탈출하면")):
    fit(h, 12, w)
    d.t(x + w / 2, 122, h, 12, MUTED, KR, "middle", 600)

# 화살표 먼저
for y in (YA, YB):
    for k in range(3):
        x1 = XS[k] + WS[k]
        d.arrow([(x1 + 2, y + BH // 2), (XS[k + 1] - 4, y + BH // 2)], SOFT, "soft", 1.3)

d.t(36, YA - 14, "매핑 없음", 13, BAD, KR, "start", 600)
d.t(36, YB - 14, "매핑 있음", 13, OK, KR, "start", 600)


def cell(k, y, title, sub, c=None, tf=MONO, dashed=False):
    x, w = XS[k], WS[k]
    fit(title, 14, w - 16)
    fit(sub, 12, w - 16)
    if c:
        d.tone(x, y, w, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, w, BH)
    d.t(x + w / 2, y + 46, title, 14, c or INK, tf, "middle", 600)
    d.t(x + w / 2, y + 70, sub, 12, MUTED, kr(sub), "middle")


# 매핑 없음
cell(0, YA, "uid 0", "컨테이너 안 root")
d.box(XS[1], YA, WS[1], BH, "#00000000", "rgba(191,192,192,0.22)", 0.9)
d.t(XS[1] + WS[1] / 2, YA + 46, "변환 없음", 14, MUTED, KR, "middle", 600)
d.t(XS[1] + WS[1] / 2, YA + 70, "uid 그대로", 12, MUTED, KR, "middle")
cell(2, YA, "uid 0", "호스트 root", BAD)
cell(3, YA, "호스트 root 권한", "실수 한 번에 호스트 장악", BAD, KR)

# 매핑 있음
cell(0, YB, "uid 0", "컨테이너 안 root")
x, w = XS[1], WS[1]
d.tone(x, YB, w, BH, ACC, 6, "14", 1.4)
d.t(x + w / 2, YB + 26, "/proc/<pid>/uid_map", 12, ACC, MONO, "middle", 600)
for fx, val, cap in ((x + 39, "0", "안쪽 시작"), (x + 116, "1000", "호스트 시작"), (x + 193, "1", "개수")):
    d.t(fx, YB + 62, val, 20, INK, MONO, "middle", 600)
    d.t(fx, YB + 88, cap, 12, MUTED, KR, "middle")
cell(2, YB, "uid 1000", "vagrant · 비특권", OK)
cell(3, YB, "평범한 사용자 권한", "탈출해도 여기까지", OK, KR)

d.legend(464, [("위험", BAD), ("안전", OK), ("매핑 파일", ACC)])
d.save(str(ASSETS / "04-02.user-namespace-mapping.svg"))
print("ok 04-02 user-namespace-mapping")
