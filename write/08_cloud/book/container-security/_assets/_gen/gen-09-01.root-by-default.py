# 타입 스펙: type-flowchart — 비root vagrant 가 친 docker run 이 사용자 ID 지정 여부와 user namespace 여부 두 판단을 지나 호스트 UID 로 끝나는 길. 기본 경로는 호스트 root 로 막다른 길이다. focal 은 호스트 root.
# 사실 출처: 노트 L40~L126 — L44~L58(whoami vagrant · docker run -it alpine sh · 안쪽 root · ps -fC sleep 의 root 30619 30557), L60(root 로 도는 Docker 데몬이 대신 생성), L79~L84(--user 5000), L126(rootless: 호스트 비root ID 가 컨테이너 안 root 로 매핑)
# Layout conventions: 1행 cy=176(시작 타원 · 마름모 둘 · 상자 · 종료 타원), 2행 y=292 h=80(Yes/No 아래 출구), 마름모 w136 h88, 가로 간격 40~52, 모든 좌표 4의 배수. 판단 출구 라벨은 모두 표기.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, PAPER2, KR, MONO

W, H = 984, 472


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "FLOWCHART · 09-01 §1",
      "비root 가 띄워도 user namespace 가 없으면 컨테이너의 root 는 호스트의 root 입니다",
      "docker run -it alpine sh 를 비root 사용자 vagrant 가 실행하면 root 로 도는 Docker 데몬이 컨테이너를 대신 만든다. "
      "사용자 ID 를 지정하면 호스트에서도 그 UID 로 보이고, user namespace 가 있으면 호스트 비root 로 매핑된다. "
      "둘 다 없으면 ps -fC sleep 에 root 가 찍힌다.",
      lead="사용자 ID 지정과 user namespace 두 판단을 모두 지나쳐야 호스트에서 root 로 끝납니다.")

CY, SH = 176, 88  # 1행 중심 y, 마름모 높이


def oval(x, w, y, h, title, sub, c=None, tmono=False, smono=False, focal=False, sub2=None):
    ts = 12 if tmono else 13
    fit(title, ts, w - 20)
    fit(sub, 12, w - 20)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
    elif c:
        d.tone(x, y, w, h, c, 20, "14", 1.1)
    else:
        d.box(x, y, w, h, PAPER2, MUTED, 1.2, 20)
    col = ACC if focal else (c or INK)
    n = 3 if sub2 else 2
    ty = y + h / 2 - (14 if sub2 else 4)
    d.t(x + w / 2, ty, title, ts, col, MONO if tmono else kr(title), "middle", 600)
    d.t(x + w / 2, ty + 20, sub, 12, MUTED, MONO if smono else kr(sub), "middle")
    if sub2:
        fit(sub2, 12, w - 20)
        d.t(x + w / 2, ty + 40, sub2, 12, MUTED, MONO, "middle")


def diamond(cx, cy, l1, l2, mono=False):
    pts = f"{cx} {cy - SH // 2} {cx + 68} {cy} {cx} {cy + SH // 2} {cx - 68} {cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
    f = MONO if mono else KR
    fit(l1, 13, 84)
    fit(l2, 13, 84)
    d.t(cx, cy - 4, l1, 13, INK, f, "middle", 600)
    d.t(cx, cy + 14, l2, 13, INK, f, "middle", 600)


def step(x, w, y, h, title, sub, tmono=False, smono=False):
    fit(title, 13, w - 16)
    fit(sub, 12, w - 16)
    d.box(x, y, w, h, PAPER2, MUTED, 1.0, 6)
    d.t(x + w / 2, y + h / 2 - 4, title, 13, INK, MONO if tmono else kr(title), "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, sub, 12, MUTED, MONO if smono else kr(sub), "middle")


# 1행 x: 시작 타원 36–240, D1 348, 상자 456–596, D2 704, 종료 타원 824–948
S_X, S_W = 36, 204
D1, B_X, B_W, D2 = 348, 456, 140, 704
OK2_X, OK2_W = 824, 124

# 1행 연결선 (판단 출구는 모두 라벨)
d.arrow([(S_X + S_W + 2, CY), (D1 - 68 - 3, CY)], MUTED, "ar", 1.4)
d.arrow([(D1 + 68 + 2, CY), (B_X - 3, CY)], MUTED, "ar", 1.4)
d.arrow([(B_X + B_W + 2, CY), (D2 - 68 - 3, CY)], MUTED, "ar", 1.4)
d.arrow([(D2 + 68 + 2, CY), (OK2_X - 3, CY)], OK, "ok", 1.4)
d.t((D1 + 68 + B_X) / 2, CY - 8, "없음", 12, MUTED, KR, "middle")
d.t((D2 + 68 + OK2_X) / 2, CY - 8, "있음", 12, MUTED, KR, "middle")

# 아래 출구 둘 + 시작 타원 아래 데몬 주석
R2_Y, R2_H = 292, 80
d.arrow([(D1, CY + SH // 2 + 2), (D1, R2_Y - 4)], OK, "ok", 1.4)
d.arrow([(D2, CY + SH // 2 + 2), (D2, R2_Y - 4)], ACC, "acc", 1.6)
d.t(D1 + 8, 262, "지정", 12, MUTED, KR, "start")
d.t(D2 + 8, 262, "없음", 12, MUTED, KR, "start")
d.line(S_X + S_W / 2, CY + 32, S_X + S_W / 2, R2_Y, SOFT, 1.2, "4 4")
d.chip(S_X + S_W / 2, 250, "요청", MUTED, 12)

# 도형
oval(S_X, S_W, CY - 32, 64, "docker run -it alpine sh", "whoami: vagrant", tmono=True, smono=True)
diamond(D1, CY, "사용자 ID", "지정?")
step(B_X, B_W, CY - 32, 64, "컨테이너 안 root", "whoami: root", smono=True)
diamond(D2, CY, "user", "namespace?", mono=True)
oval(OK2_X, OK2_W, CY - 32, 64, "호스트 비root", "rootless 매핑", OK)

step(S_X, S_W, R2_Y, R2_H, "Docker 데몬", "root 로 대신 생성")
oval(268, 160, R2_Y, R2_H, "호스트 UID 5000", "--user 5000", OK, smono=True)
oval(D2 - 112, 224, R2_Y, R2_H, "호스트 root", "ps -fC sleep", focal=True, smono=True, sub2="root 30619 30557")

d.legend(H - 56, [("호스트 root", ACC), ("호스트 비root", OK)])
d.save(str(ASSETS / "09-01.root-by-default.svg"))
print("ok 09-01 root-by-default")
