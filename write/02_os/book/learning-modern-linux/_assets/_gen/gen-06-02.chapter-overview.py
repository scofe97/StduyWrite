# 06-02 학습 목표 뒤 전체 지도 — 6장 뒤 절반의 절 일곱을 읽는 순서로 잇는다.
# 원문 6장 서두: "In the next part of the chapter, we focus on containers: what they are and how they
#       work. We'll review the building blocks of containers, what tooling you have available, and good
#       practices around using containers. To round off this chapter, we look at modern ways to manage
#       Linux apps, especially in desktop environments."
# 판단: 이 도식은 장 전체의 읽는 순서 지도라 한 대상의 "실제 구조" 를 그릴 자리가 아니다(본문도 "읽는 순서로
#       이은 지도" 라 소개한다). 그래서 흐름은 그대로 두고, 칸마다 그 절이 다루는 실제 대상(명령·경로)을 칩으로
#       달고, 나머지 다섯 장과 같은 말로 묶음(재료 셋 · 재료를 감싼 것 · 같은 재료의 다른 쓰임)을 보였다.
# 칩 값: 모두 본문 그 절에 나오는 것 — §1 연도 2001~2014, §2 clone(CLONE_NEW*)·sudo lsns, §3 systemd-cgtop,
#       §4 CoW·바인드 마운트, §5 docker run, §6 greeter:1, §7 Snap·Flatpak.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음 · 다루는 대상)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 516
d = D(W, H, "LEARNING MODERN LINUX · 06-02",
      "컨테이너의 새로움은 재료가 아니라 조합에 있다",
      "6장 뒤 절반의 절 일곱을 읽는 순서로 이은 지도. 칸마다 절 번호와 그 절이 답하는 물음, 그 절이 "
      "다루는 실제 명령·경로를 적었다. 2~4절이 재료 셋(네임스페이스·cgroups·CoW)이고 5~6절이 그 재료를 "
      "감싼 Docker 와 Dockerfile, 7절이 같은 재료를 쓰는 데스크톱 쪽 관리자다.",
      "5절이 이 노트의 제목이 가리키는 자리입니다")

CW, CH, GAP, X0, PAD = 188, 108, 28, 22, 6
R1, R2 = 140, 316
cards = [
    ("§1", "오래됐고 새롭다", "Docker 가 얹은 두 가지", "2001 → 2014"),
    ("§2", "네임스페이스", "무엇이 보이는가", "clone(CLONE_NEW*)"),
    ("§3", "cgroups", "얼마나 쓰는가", "systemd-cgtop"),
    ("§4", "세 번째 재료", "CoW 는 5장에서 이미", "CoW · 바인드 마운트"),
    ("§5", "Docker", "재료를 감싸 준 것", "docker run"),
    ("§6", "Dockerfile", "지시어가 층이 된다", "greeter:1"),
    ("§7", "데스크톱 쪽 관리자", "같은 재료, 다른 목표", "Snap · Flatpak"),
]


def pos(i):
    return (X0 + (i % 4) * (CW + GAP), R1) if i < 4 else (X0 + (i - 4) * (CW + GAP), R2)


# 묶음 띠 (글자·카드보다 먼저)
groups = [("재료 셋", 1, 3, INFO), ("재료를 감싼 것", 4, 5, ACC), ("같은 재료, 다른 쓰임", 6, 6, OK)]
for name, a, b, c in groups:
    (xa, ya), (xb, _) = pos(a), pos(b)
    d.o.append(f'<rect x="{xa - PAD}" y="{ya - PAD}" width="{xb + CW - xa + 2 * PAD}" height="{CH + 2 * PAD}" rx="10" '
               f'fill="{c}0A" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    d.t(xa - PAD, ya - 16, name, 12, c, KR, "start", 600)

# 읽는 순서 화살표
for i in range(len(cards) - 1):
    (x1, y1), (x2, y2) = pos(i), pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 26
        d.path(f"M {x1 + CW / 2} {y1 + CH + 8} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 10}", MUTED, 1.3, m="ar")

for i, (n, title, q, obj) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 4)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 14, y + 24, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 14, y + 48, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 14, y + 68, q, 12, MUTED, KR, "start")
    kr = any('가' <= ch <= '힣' for ch in obj)
    cw = len(obj) * (11 * 1.0 if kr else 11 * 0.62) + 14
    d.chip(x + 14 + cw / 2, y + 88, obj, ACC if focal else MUTED, 11)

d.legend(R2 + CH + 32, [("재료 셋", INFO), ("재료를 감싼 자리", ACC), ("같은 재료의 다른 쓰임", OK)])
d.save("06-02.chapter-overview.svg")
print("ok 06-02.chapter-overview", R2 + CH + 32)
