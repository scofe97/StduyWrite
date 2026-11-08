# 04-03.dns-search-path — 같은 규칙인데 클러스터 밖 이름은 시도가 네 번이다
# 본문 요구: 「검색 경로와 이름 하나의 질의」 — 후보를 앞에서부터 시도하고 답이 오면 멈춘다. web 은 첫 후보에서 적중(시도 1번),
#           example.com 은 클러스터 접미사 셋이 NXDOMAIN 이고 이름 그대로 적중(시도 4번). 시도마다 A 와 AAAA 두 질의가 나간다.
#           ndots 의 5 는 질의 횟수가 아니라 "점이 5개 미만이면 검색 경로를 먼저 돈다"는 임계값이다.
# 타입 스펙: type-process.md — 같은 절차를 두 입력으로 돌려 시도 횟수가 갈리는 것을 보인다. 위 띠가 안 이름, 아래 띠가 밖 이름.
# 이력: 2026-11-08 kind(kubeadm, 노드 v1.37.0, CoreDNS v1.14.6)에서 잰 이름과 네임스페이스(default)로 다시 그렸다.
#       측정 노드에는 호스트 검색 도메인이 없어 네 번째 후보가 이름 그대로다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, PAPER, PAPER2, KR, MONO

W, H = 1000, 596
d = D(W, H, "CLUSTER DNS · THE SEARCH PATH IS TRIED IN ORDER",
      "같은 규칙인데 클러스터 밖 이름은 시도가 네 번이다",
      "default 네임스페이스의 Pod 에서 web 은 web.default.svc.cluster.local 이 첫 후보라 시도 1번에 끝나 질의가 2번이다. "
      "example.com 은 접미사 세 개가 NXDOMAIN 이고 이름 그대로 네 번째에 적중해 시도 4번, 질의 8번이다.",
      lead="안 이름은 첫 후보에서 맞고 밖 이름은 접미사 셋을 소진한 뒤 맞는다")


def band(x, y, w, h, c):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.4"/>')


def step(x, y, w, h, c, sw, no, name, name_c=INK, name_mono=True):
    d.tone(x, y, w, h, c, 6, "12", sw)
    cx = x + w // 2
    d.t(cx, y + 22, no, 11, MUTED, KR)
    d.t(cx, y + 42, ddx.fit(name, 12, w - 16, name), 12, name_c, MONO if name_mono else KR)


# ── 위 띠: 클러스터 안 이름 — 첫 후보에서 끝난다
band(32, 112, 936, 180, OK)
d.t(52, 138, "클러스터 안 이름 · web", 12, OK, KR, "start", 600)
step(52, 152, 300, 56, OK, 1.2, "1번째 후보", "web.default.svc.cluster.local")
d.t(202, 228, "적중 · 여기서 끝", 12, OK, KR)
d.line(356, 180, 392, 180, SOFT, 1.0, "3 3")
d.box(396, 152, 540, 56, PAPER, "rgba(191,192,192,0.14)", 0.9, 6)
d.t(666, 185, "이후 후보는 시도하지 않음", 12, SOFT, KR)
d.t(52, 264, "시도 1번 × (A + AAAA) = 질의 2번", 12, MUTED, KR, "start")

# ── 아래 띠: 클러스터 밖 이름 — 접미사 셋이 NXDOMAIN, 이름 그대로 적중
band(32, 310, 936, 212, BAD)
d.t(52, 336, "클러스터 밖 이름 · example.com", 12, BAD, KR, "start", 600)
SW, STR = 214, 224
TRIES = [("1번째 후보", "+default.svc.cluster.local"), ("2번째 후보", "+svc.cluster.local"),
         ("3번째 후보", "+cluster.local")]
for i, (no, name) in enumerate(TRIES):
    x = 52 + i * STR
    step(x, 350, SW, 56, BAD, 1.1, no, name)
    d.t(x + SW // 2, 426, "NXDOMAIN", 12, BAD, MONO)
    d.path(f"M {x + SW + 4} 378 L {x + STR - 2} 378", BAD, 1.4, m="bad")
x4 = 52 + 3 * STR
step(x4, 350, SW, 56, OK, 1.4, "4번째 후보", "example.com (그대로)", OK)
d.t(x4 + SW // 2, 426, "적중", 12, OK, KR)

d.box(52, 444, 884, 58, PAPER, RULE, 0.9, 6)
d.t(72, 478, "시도 4번 × (A + AAAA) = 질의 8번 · 점이 하나라 ndots:5 에 걸려 검색 경로를 먼저 돈다", 12, MUTED, KR, "start")

d.legend(548, [("NXDOMAIN 으로 끝난 후보", BAD), ("적중한 후보", OK)])
d.save("04-03.dns-search-path.svg")
print("ok dns-search-path")
