# 04-03.dns-search-path — 같은 규칙인데 클러스터 밖 이름이 훨씬 비싸다
# 본문 요구: 검색 도메인을 앞에서부터 붙여 시도한다는 것, 안 이름은 첫 판에 맞고 밖 이름은
#           실패를 다 소진한 뒤에야 맞는다는 것, 그리고 시도마다 A·AAAA 두 질의가 나간다는 것.
#           ndots 의 5 는 질의 횟수가 아니라 "점이 5개 미만이면 검색 경로를 먼저 돈다"는 임계값이다.
# 타입 스펙: type-process.md — 같은 절차를 두 입력으로 돌려 시도 횟수가 갈리는 것을 보인다.
#           위 띠가 안 이름(1판에서 끝), 아래 띠가 밖 이름(다섯 판)이고 대비가 곧 논지다.
# 이력: 2026-09-05 생성기 재작성. SVG 는 2026-09-02 회차에 전면 재작성됐는데 생성기는 옛 판
#       (SEARCH PATH COST · 시도 4개 + 처방 2개)을 그대로 만들고 있었다. 재생성하면 지금 그림이
#       옛 그림으로 되돌아가는 상태였다. 현재 SVG 를 정본으로 삼아 값·좌표·색을 그대로 옮기고,
#       손으로 그려져 있던 탓에 남아 있던 한글 9~10px 라벨만 하한 11px 로 올렸다.
# 좌표: 띠 두 개(y=112 h=180 · y=310 h=212). 아래 띠의 단계는 x stride 180, 폭 168(마지막 164).
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, PAPER, PAPER2, KR, MONO

W, H = 1000, 624   # 범례 아래 여유 확보 (정본 SVG 는 0px 라 dd-lint margin error)
d = D(W, H, "CLUSTER DNS · THE SEARCH PATH IS TRIED IN ORDER",
      "같은 규칙인데 클러스터 밖 이름이 훨씬 비싸다",
      "검색 도메인을 앞에서부터 붙여 시도한다. 클러스터 안 이름은 첫 판에 맞고, 밖 이름은 "
      "검색 경로의 실패를 다 소진한 뒤에야 맞는다. 시도마다 A 와 AAAA 두 질의가 나가므로 패킷은 그 두 배다.",
      lead="검색 도메인을 앞에서부터 붙여 시도한다. 안 이름은 첫 판에 맞고 밖 이름은 실패를 다 소진한 뒤 맞는다")

def band(x, y, w, h, c):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.4"/>')

def step(x, y, w, h, c, sw, no, name, name_c=INK, name_mono=True):
    d.tone(x, y, w, h, c, 6, "12", sw)
    cx = x + w // 2
    d.t(cx, y + 22, no, 11, MUTED, MONO)
    d.t(cx, y + 42, ddx.fit(name, 11, w - 16, name), 11, name_c, MONO if name_mono else KR)

# ── 위 띠: 클러스터 안 이름 — 첫 판에서 끝난다
band(32, 112, 936, 180, OK)
d.t(52, 138, "클러스터 안 이름 · web", 12, OK, KR, "start", 600)
step(52, 152, 200, 56, OK, 1.2, "1차", "web.default.svc…")
d.t(152, 228, "있다 · 여기서 끝", 11, OK, KR)
d.line(256, 180, 292, 180, SOFT, 1.0, "3 3")
d.box(296, 152, 640, 56, PAPER, "rgba(191,192,192,0.14)", 0.9, 6)
d.t(616, 185, "2차부터는 아예 시도하지 않는다", 11, SOFT, KR)
d.t(52, 264, "질의 왕복 1회. 이름을 짧게 부르는 편의가 여기서는 값이 거의 없다", 11, MUTED, KR, "start")

# ── 아래 띠: 클러스터 밖 이름 — 헛발질 넷을 소진한 뒤에야 맞는다
band(32, 310, 936, 212, BAD)
d.t(52, 336, "클러스터 밖 이름 · api.pay.example.com", 12, BAD, KR, "start", 600)
TRIES = [("1차", "…default.svc…", True), ("2차", "…svc.cluster.local", True),
         ("3차", "…cluster.local", True), ("4차", "호스트 검색 경로", False)]
for i, (no, name, mono) in enumerate(TRIES):
    x = 52 + i * 180
    step(x, 350, 168, 56, BAD, 1.1, no, name, INK, mono)
    d.t(x + 84, 426, "없음", 11, BAD, KR)
    d.path(f"M {x + 172} 378 L {x + 176} 378", BAD, 1.4, m="bad")
step(772, 350, 164, 56, OK, 1.4, "마지막", "이름 그대로", OK, False)
d.t(854, 426, "있다", 11, OK, KR)

d.box(52, 444, 884, 58, PAPER, RULE, 0.9, 6)
d.t(72, 468, "헛발질을 다 소진한 뒤에야 정답에 닿는다. 그리고 시도마다 A 와 AAAA 두 질의를 내보내므로",
    11, MUTED, KR, "start")
d.t(72, 490, "실제 패킷은 그 두 배다. 이름 하나에 왕복 열 번이 나갈 수 있다", 11, BAD, KR, "start")

d.t(36, 558, "ndots 의 5 는 질의 횟수가 아니다. 점이 5개 미만이면 검색 경로를 먼저 돈다는 임계값이고, "
             "위 이름은 점이 3개라 걸린다", 12, MUTED, KR, "start")
d.legend(576, [("헛발질", BAD), ("맞은 시도", OK)])
d.save("04-03.dns-search-path.svg")
print("ok dns-search-path")
