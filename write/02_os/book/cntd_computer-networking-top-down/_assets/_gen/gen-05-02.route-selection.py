# 타입 스펙: type-flowchart — 규칙 넷을 순서대로 걸어 후보를 하나만 남긴다. 순서가 결과를 바꾼다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.4.3 Route-Selection Algorithm 규칙 1~4
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, KR, MONO

W, H = 1000, 700
d = D(W, H, "SECTION 5.4.3 · ROUTE SELECTION",
      "규칙의 순서가 답을 바꿉니다",
      "BGP 경로 선택 알고리즘의 네 규칙을 순서대로 적용하는 흐름. 뜨거운 감자가 세 번째에 놓인 덕분에 BGP 는 이기적인 알고리즘이 아니게 된다.",
      "같은 후보 둘도 규칙을 어느 순서로 거느냐에 따라 다른 답이 나옵니다")

BX, BW, BH = 60, 520, 66
STEPS = [
    ("1. 로컬 선호도", "관리자가 정책으로 정한 값. 가장 높은 것만 남깁니다", ACC),
    ("2. AS-PATH 길이", "남은 것 중 AS 홉이 가장 짧은 것만 남깁니다", INFO),
    ("3. 뜨거운 감자", "NEXT-HOP 라우터까지 AS 안 비용이 가장 싼 것", MUTED),
    ("4. BGP 식별자", "그래도 남으면 식별자로 자릅니다", SOFT),
]
y = 128
for i, (name, sub, c) in enumerate(STEPS):
    d.box(BX, y, BW, BH, PAPER2, c, 1.5 if i < 2 else 1.0, 8)
    d.t(BX + 20, y + 27, name, 12, c if i < 3 else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 11, MUTED, KR, "start")
    if i < len(STEPS) - 1:
        d.path(f"M {BX + BW / 2} {y + BH} L {BX + BW / 2} {y + BH + 26}", MUTED, 1.4, m="ar")
        d.t(BX + BW / 2 + 92, y + BH + 18, "아직 둘 이상 남으면", 11, SOFT, KR)
    y += BH + 26

# 규칙 4 에서 결론으로 내려가는 연결 — 루프가 마지막 화살표를 그리지 않는다
d.path(f"M {BX + BW / 2} {y - 26} L {BX + BW / 2} {y - 6}", ACC, 1.4, m="acc")
d.tone(BX, y, BW, 52, ACC, 8, "12", 1.5)
d.t(BX + BW / 2, y + 32, "남은 하나를 전달 표에 넣습니다", 12, ACC, KR, "middle", 600)

# 오른쪽 — Figure 5.10 의 1b 가 겪는 실제 판정
PX, PW = 620, 340
d.box(PX, 128, PW, 300, PAPER2, RULE, 1.0, 9)
d.t(PX + PW / 2, 156, "Figure 5.10 의 라우터 1b", 12, INK, KR, "middle", 600)
d.line(PX + 16, 170, PX + PW - 16, 170, RULE, 0.9)
rows = [("후보 A", "AS2 AS3", "NEXT-HOP 2a · 링크 2", MUTED),
        ("후보 B", "AS3", "NEXT-HOP 3d · 링크 3", ACC)]
ry = 196
for label, path, hop, c in rows:
    d.t(PX + 24, ry, label, 11, c, KR, "start", 600)
    d.t(PX + 96, ry, path, 12, c, MONO, "start")
    d.t(PX + 24, ry + 20, hop, 11, MUTED, MONO, "start")
    ry += 56
d.t(PX + 24, 314, "감자만 따지면 A 가 이깁니다 (2 < 3)", 11, MUTED, KR, "start")
d.t(PX + 24, 336, "그러나 규칙 2 가 먼저입니다", 11, INFO, KR, "start")
d.t(PX + 24, 358, "AS-PATH 가 1 칸인 B 가 남습니다", 11, ACC, KR, "start", 600)
d.t(PX + 24, 396, "AS2 를 건너뛰는 쪽이 선택됩니다", 11, ACC, KR, "start")

d.t(PX, 462, "규칙 2 가 유일한 규칙이라면 BGP 는", 11, MUTED, KR, "start")
d.t(PX, 482, "AS 홉을 거리로 쓰는 거리 벡터가 됩니다.", 11, MUTED, KR, "start")

d.t(30, 618, "규칙 1 이 맨 앞이라는 사실이 이 알고리즘의 성격을 정합니다. 정책이 최단 경로를 이깁니다.", 11, MUTED, KR, "start")

d.legend(640, [("정책이 정하는 값", ACC), ("AS 홉 수", INFO), ("AS 안의 비용", MUTED)])
d.t(960, 688, "KUROSE-ROSS 9E 5.4.3 · RFC 4271", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.route-selection.svg"
d.save(out)
print("→", out)
