# 타입 스펙: type-flowchart — 격리 경계를 맡은 쪽이 서로 볼 통로를 열어 두는가에서 갈라진다. 열어 두는 커널은 통로 셋 → 2천만 줄 이상 → 약한 격리의 막다른 길, 열어 두지 않는 하이퍼바이저는 통로 없음 → 약 5만 줄 → 강한 격리의 막다른 길이다. focal 은 갈림 마름모.
# 사실 출처: 노트 L159~L167(ps · /proc · IPC · 공유 메모리 통로, VM 사이에는 대응물 없음), L165(예상 밖 접근 결함), L169(Linux 2천만 줄 이상 · Xen 약 5만 줄), L171(공격 표면 · 결함 가능성), L204(4천만 줄 · 6.14-rc1)
# Layout conventions: 시작 타원 y=96 h=36, 마름모 y=164 h=96 폭 200, 가지 열 중심 x=246·738 폭 360, 상자 h=72 · stride 104(y=300·404·508). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, KR, MONO

W, H = 984, 656
CXS = [246, 738]
BW, BH = 360, 72
BY = [300, 404, 508]
MID = 492


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "FLOWCHART · 05-01 §5",
      "통로를 열어 둔 커널은 코드가 크고, 통로가 없는 하이퍼바이저는 코드가 작습니다",
      "격리 경계를 맡은 쪽이 서로 볼 통로를 열어 두는지에서 갈라지는 흐름. "
      "커널은 ps, /proc, IPC 와 공유 메모리 통로를 열어 두므로 메모리 관리 코드가 Linux 커널 2천만 줄 이상으로 크고, 예상 밖 접근을 허용하는 결함 가능성이 있어 격리가 약하다. "
      "하이퍼바이저는 VM 사이에 통로가 없어 메모리 공유를 다루지 않으므로 Xen 약 5만 줄로 작고, 공격 표면이 작아 격리가 강하다.",
      lead="격리 강도를 가르는 것은 하이퍼바이저의 실력이 아니라, 서로 볼 통로를 열어 두느냐에서 생기는 코드 규모입니다.")

# 시작 타원
d.o.append(f'<rect x="{MID - 110}" y="96" width="220" height="36" rx="18" fill="#161B22" stroke="#BFC0C038" stroke-width="0.9"/>')
d.t(MID, 119, "격리 경계를 맡은 쪽", 13, INK, KR, "middle", 600)

# 갈림 마름모
cy = 212
d.arrow([(MID, 134), (MID, 160)], SOFT, "soft", 1.3)
d.o.append(f'<polygon points="{MID},164 {MID + 100},{cy} {MID},260 {MID - 100},{cy}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
d.t(MID, cy - 2, "서로 볼 통로를", 12, INK, KR, "middle", 600)
d.t(MID, cy + 16, "열어 두는가", 12, INK, KR, "middle", 600)

# 갈래 화살표
for k, (label, cx) in enumerate((("있음", CXS[0]), ("없음", CXS[1]))):
    xs = MID - 102 if k == 0 else MID + 102
    d.arrow([(xs, cy), (cx, cy), (cx, BY[0] - 4)], SOFT, "soft", 1.3)
    d.t((xs + cx) / 2, cy - 10, label, 12, MUTED, KR, "middle", 600)

# 가지별 사슬
BRANCH_TITLE = ["커널 — 프로세스 사이", "하이퍼바이저 — VM 사이"]
BOXES = [
    [  # 커널
        (None, "합법적인 통로 셋", ["ps · /proc · IPC · 공유 메모리", "의도적인 프로세스 간 메모리 공유"]),
        (None, "커널의 메모리 관리 코드", ["Linux 커널 2천만 줄 이상", "현재는 4천만 줄 (6.14-rc1)"]),
        (BAD, "격리 약함", ["예상 밖 접근을 허용하는 결함 가능성"]),
    ],
    [  # 하이퍼바이저
        (None, "통로 없음", ["다른 VM 의 프로세스를 볼 수 없음", "VM 끼리 메모리 공유 없음"]),
        (None, "하이퍼바이저의 메모리 관리 코드", ["Xen 약 5만 줄"]),
        (OK, "격리 강함", ["공격 표면 작음 · 결함 가능성 낮음"]),
    ],
]
for k in range(2):
    cx = CXS[k]
    x = cx - BW // 2
    d.t(cx + 12, 262, BRANCH_TITLE[k], 12, INK, KR, "start", 600)
    for n in range(2):
        d.arrow([(cx, BY[n] + BH + 2), (cx, BY[n + 1] - 4)], SOFT, "soft", 1.3)
        d.t(cx + 12, BY[n] + BH + 21, ("코드 규모", "공격 표면")[n], 12, MUTED, KR, "start", 600)
    for n, (col, title, subs) in enumerate(BOXES[k]):
        y = BY[n]
        fit(title, 13, BW - 16)
        if col:
            d.tone(x, y, BW, BH, col, 6, "14", 1.2)
        else:
            d.box(x, y, BW, BH)
        d.t(x + 16, y + 20, str(n + 1), 11, SOFT, MONO, "start")
        ty = y + (28 if len(subs) == 2 else 30)
        d.t(cx, ty, title, 13, col or INK, kr(title), "middle", 600)
        for m, s in enumerate(subs):
            fit(s, 12, BW - 16)
            d.t(cx, ty + 20 + m * 18, s, 12, MUTED, kr(s), "middle")

d.legend(612, [("갈림", ACC), ("약한 격리", BAD), ("강한 격리", OK)])
d.save(str(ASSETS / "05-01.isolation-strength.svg"))
print("ok 05-01 isolation-strength")
