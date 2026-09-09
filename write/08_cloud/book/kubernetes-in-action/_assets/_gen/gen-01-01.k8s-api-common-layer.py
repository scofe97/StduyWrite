# 01-01 §3-3 — 표준 쿠버네티스 API 라는 공통 레이어
# 본문 근거(01-01 §3 세 번째 흐름 '클라우드 사용 방식의 표준화'):
#   "클라우드 제공자마다 API 가 다르므로, 특정 벤더에 종속되지 않으려면 인프라·API 를 추상화하는
#    별도 작업이 필요합니다." · "주요 클라우드 제공자들이 앞다퉈 쿠버네티스를 자사 제품에 통합했고,
#    그 결과 고객은 표준화된 쿠버네티스 API 하나로 어느 클라우드에든 애플리케이션을 배포할 수
#    있게 됐습니다." · "애플리케이션을 특정 벤더의 고유 API 가 아니라 쿠버네티스 API 위에 지으면,
#    다른 제공자로 옮기는 일도 상대적으로 쉬워집니다."
#   본문 직후 문장: "쿠버네티스 API라는 공통 레이어 하나만 배우면 됩니다."
# 타입 스펙: type-layers.md — 본문이 '공통 레이어' 라고 형태를 직접 지정한다.
#   관례를 따른다: 전폭 밴드 4층(856px), 층 높이 64px, 인덱스 태그 mono 9px,
#   층 이름 15px 600, 부제는 오른쪽, accent 는 한 층에만, 방향 표시는 스택 바깥 왼쪽 여백.
#   층마다 다른 색을 칠하지 않는다(안티패턴) — 초점 한 층만 accent.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER, PAPER2, KR, MONO
import ddx

X0, BWID, LH, TOP = 72, 856, 64, 136        # 스택 — 관례 범위(폭 800~880 · 높이 56~72) 안에서 고정
N = 4
BOT = TOP + N * LH                          # 392
NOTE1, NOTE2, LEG_Y = BOT + 36, BOT + 60, BOT + 88
W, H = 1000, LEG_Y + 40

d = D(W, H, "KUBERNETES IN ACTION · 01-01",
      "공통 레이어 하나만 배우면 된다",
      "클라우드 제공자마다 고유 API 가 다르다. 쿠버네티스 API 가 그 위에 표준 한 벌로 서면서, "
      "애플리케이션은 아래층이 어느 제공자인지 모른 채 같은 매니페스트로 배포된다.",
      lead="주요 제공자들이 쿠버네티스를 자사 제품에 통합했기 때문에 이 층이 성립한다")

LAYERS = [
    ("L1", "애플리케이션 · 배포 매니페스트", "벤더 고유 API 를 직접 쓰지 않는다", False),
    ("L2", "쿠버네티스 API", "표준 한 벌 — 이 층만 배우면 된다", True),
    ("L3", "각 제공자의 쿠버네티스 서비스", "GKE · AKS · EKS 등으로 통합돼 있다", False),
    ("L4", "클라우드 제공자 고유 API", "Amazon AWS · IBM Cloud · Google Cloud · Microsoft Azure", False),
]

for i, (tag, name, sub, focal) in enumerate(LAYERS):
    y = TOP + i * LH
    if focal:
        d.o.append(f'<rect x="{X0}" y="{y}" width="{BWID}" height="{LH}" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{X0}" y="{y}" width="{BWID}" height="{LH}" '
                   f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(X0 + 20, y + LH // 2 + 4, tag, 9, SOFT, MONO, "start")
    d.t(X0 + 64, y + LH // 2 + 5, ddx.fit(name, 15, 380, name), 15,
        ACC if focal else INK, KR, "start", 600)
    d.t(X0 + BWID - 20, y + LH // 2 + 4, ddx.fit(sub, 10, 400, sub), 10,
        ACC if focal else MUTED,
        MONO if all(ord(c) < 128 or c in '·' for c in sub) else KR, "end")

# 방향 표시 — 스택 바깥 왼쪽 여백
d.t(44, 124, "추상화", 12, SOFT, KR, "middle")
d.path(f"M 44 {BOT - 12} L 44 {TOP + 12}", SOFT, 1.2, m="soft")

d.t(24, NOTE1, "고유 API 를 직접 쓰는 길도 있다 — 다만 그 길로 지으면 다른 제공자로 옮길 때 "
               "배포 로직을 다시 짜야 한다.", 11, MUTED, KR, "start")
d.t(24, NOTE2, "쿠버네티스 API 위에 지으면 같은 매니페스트가 AWS 든 GCP 든 그대로 간다. "
               "이동이 쉬워지는 이유가 이 한 층이다.", 11, MUTED, KR, "start")

d.legend(LEG_Y, [("표준 한 벌이 서는 층", ACC)])
d.save("01-01-k8s-api-common-layer.svg")
print("ok k8s-api-common-layer")
