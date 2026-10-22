# 타입 스펙: type-timeline — 같은 질문 앞에서 원문 시점(2020)의 답과 지금(2026)의 답을 나란히 놓고 여섯 해 사이 답이 바뀐 다섯 항목과 그대로인 다섯 항목을 가른다. 시간축은 눈금 둘(원문·지금)만 쓴 축약이고 행마다 바뀐 곳(쿠버네티스·커널)을 꼬리표로 단다. focal 은 가장 크게 움직인 어드미션 컨트롤.
# 사실 출처: 노트 L84~L100(PodSecurityPolicy v1.21 폐기 예고→v1.25 제거·PSA 세 등급·Gatekeeper/Kyverno·애노테이션→securityContext·readOnlyRootFilesystem·BPF LSM 5.7 -EPERM·Secrets Store CSI Driver·답 그대로 다섯), 원문 연도 2020은 노트 L6 source
# Layout conventions: 질문 열 x=24(w168) · 원문 상자 x=208(w240) · 화살표 · 지금 상자 x=496(w280) · 꼬리표 x=792(w132). 행 h=72·stride 84(y=148+84i), 그대로인 행은 구분선 아래 h=88. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, PAPER, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def tw(t, size):
    return sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)


def fit(t, size, limit):
    assert tw(t, size) <= limit, (t, tw(t, size), limit)


W, H = 960, 744
QX, QW = 24, 168
TX, TW = 208, 240
NX, NW = 496, 280
GX, GW = 792, 132
Y0, RH, STRIDE = 148, 72, 84

d = D(W, H, "CONTAINER SECURITY · 15-01 §3",
      "질문은 그대로이고 답은 다섯 항목에서 바뀌었다",
      "어드미션 컨트롤은 PodSecurityPolicy 에서 Pod Security Admission 으로, seccomp·AppArmor 는 애노테이션에서 securityContext 필드로, "
      "읽기 전용은 readOnlyRootFilesystem 으로, 런타임 보호는 관찰만 하던 eBPF 에서 BPF LSM 으로, 시크릿 전달은 Secrets Store CSI Driver 가 더해졌다. "
      "비root·--privileged·capability·CIS 벤치마크·컨테이너 전용 호스트는 답이 같다.",
      "체크리스트 질문별로 원문 시점의 답과 지금의 답을 잇고 바뀐 곳을 꼬리표로 단 도식")

# 시간축: 눈금 둘
AXY = 124
TC, NC = TX + TW // 2, NX + NW // 2
d.t(QX, 112, "질문", 12, MUTED, KR, "start", 600)
d.t(TC, 112, "원문 시점 · 2020", 13, INK, KR, "middle", 600)
d.t(NC, 112, "지금 · 2026", 13, INK, KR, "middle", 600)
d.t(GX, 112, "바뀐 곳", 12, MUTED, KR, "start", 600)
d.arrow([(TC + 8, AXY), (NC - 12, AXY)], SOFT, "soft", 1.2)
d.o.append(f'<circle cx="{TC}" cy="{AXY}" r="4" fill="{SOFT}"/><circle cx="{NC}" cy="{AXY}" r="4" fill="{SOFT}"/>')
d.t((TC + NC) // 2, AXY - 8, "여섯 해", 12, MUTED, KR, "middle")

ROWS = [
    # (질문, 부제, 원문 제목, 원문 부제, 지금 제목, [지금 부제…], 꼬리표, focal)
    ("어드미션 컨트롤", "", "PodSecurityPolicy", "v1.21 폐기 예고 → v1.25 제거",
     "Pod Security Admission", ["privileged · baseline · restricted", "조건부 정책은 Gatekeeper · Kyverno"], "쿠버네티스", True),
    ("seccomp · AppArmor", "프로파일 붙이는 법", "애노테이션", "",
     "securityContext 필드", ["정식 필드"], "쿠버네티스", False),
    ("읽기 전용", "루트 파일시스템", "PodSecurityPolicy 의 필드", "",
     "securityContext", ["readOnlyRootFilesystem"], "쿠버네티스", False),
    ("런타임 보호", "시스템 콜", "eBPF", "관찰만 하고 바꾸지는 못함",
     "BPF LSM", ["커널 5.7 · -EPERM 으로 거부"], "커널 5.7", False),
    ("시크릿 전달", "", "임시 파일시스템", "저자의 선호",
     "+ Secrets Store CSI Driver", ["볼륨으로 직접 마운트 · etcd 우회"], "쿠버네티스", False),
]


def lines(x, y, items, c_first=INK):
    n = len(items)
    y0 = y + RH / 2 - (n - 1) * 9 + 4
    for k, (t, size, col, wt) in enumerate(items):
        d.t(x, y0 + k * 18, t, size, col, kr(t), "middle", wt)


for i, (q, qs, t1, t2, n1, n2, tag, focal) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    fit(q, 13, QW)
    d.t(QX, y + (30 if qs else 40), q, 13, INK, kr(q), "start", 600)
    if qs:
        fit(qs, 12, QW)
        d.t(QX, y + 50, qs, 12, MUTED, kr(qs), "start")
    d.box(TX, y, TW, RH)
    t_items = [(t1, 13, INK, 600)] + ([(t2, 12, MUTED, 400)] if t2 else [])
    for t, size, _, _ in t_items:
        fit(t, size, TW - 16)
    lines(TC, y, t_items)
    ac = ACC if focal else SOFT
    d.arrow([(TX + TW + 2, y + RH // 2), (NX - 4, y + RH // 2)], ac, "acc" if focal else "soft", 1.5 if focal else 1.3)
    if focal:
        d.tone(NX, y, NW, RH, ACC, 6, "1F", 1.4)
    else:
        d.tone(NX, y, NW, RH, INFO, 6, "14", 1.1)
    n_items = [(n1, 13, INK, 600)] + [(s, 12, MUTED, 400) for s in n2]
    for t, size, _, _ in n_items:
        fit(t, size, NW - 16)
    lines(NC, y, n_items)
    tc = WARN if tag.startswith("커널") else MUTED
    w = tw(tag, 12) + 16
    d.o.append(f'<rect x="{GX}" y="{y + RH // 2 - 12}" width="{w:.1f}" height="24" rx="4" fill="{PAPER}" stroke="{tc}" stroke-width="0.9"/>')
    d.t(GX + w / 2, y + RH // 2 + 4, tag, 12, tc if tc == WARN else INK, KR)

# 그대로인 행
SEP = Y0 + len(ROWS) * STRIDE - 4          # 564
d.line(24, SEP, 924, SEP, "rgba(191,192,192,0.22)", 1.0, "4 6")
GY, GH = SEP + 20, 88
d.t(QX, GY + 36, "답까지 그대로", 13, INK, KR, "start", 600)
d.t(QX, GY + 56, "다섯 항목", 12, MUTED, KR, "start")
d.tone(TX, GY, NX + NW - TX, GH, OK, 6, "12", 1.1)
for r, chips in enumerate((["비root", "--privileged", "capability"], ["CIS 벤치마크", "컨테이너 전용 호스트"])):
    ws = [tw(c, 12) + 16 for c in chips]
    total = sum(ws) + 8 * (len(chips) - 1)
    x = TX + (NX + NW - TX - total) / 2
    for c, w in zip(chips, ws):
        yy = GY + 14 + r * 36
        d.o.append(f'<rect x="{x:.1f}" y="{yy}" width="{w:.1f}" height="24" rx="4" fill="{PAPER}" stroke="{OK}" stroke-width="0.9"/>')
        d.t(x + w / 2, yy + 16, c, 12, INK, kr(c))
        x += w + 8
d.o.append(f'<rect x="{GX}" y="{GY + GH // 2 - 12}" width="{tw("변화 없음", 12) + 16:.1f}" height="24" rx="4" fill="{PAPER}" stroke="{OK}" stroke-width="0.9"/>')
d.t(GX + (tw("변화 없음", 12) + 16) / 2, GY + GH // 2 + 4, "변화 없음", 12, INK, KR)

d.legend(GY + GH + 28, [("원문 시점의 답", SOFT), ("지금의 답", INFO), ("가장 크게 움직인 것", ACC), ("답 그대로", OK), ("커널이 바꾼 것", WARN)])
d.save(str(ASSETS / "15-01.checklist-then-now.svg"))
print("ok 15-01 checklist-then-now")
