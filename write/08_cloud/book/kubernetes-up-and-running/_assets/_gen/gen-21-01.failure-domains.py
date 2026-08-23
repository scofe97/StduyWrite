# 21-01 §리전 클러스터로도 부족한 이유
# 본문이 반전 구조로 논증한다 — 단일 클러스터의 약점을 리전 클러스터가 메우는데,
# 그러고 나서 "Kubernetes 자체가 단일 장애점" 이라고 뒤집는다. 그러니 셋을 나란한
# 카드로 놓으면 안 되고, *막는 것* 과 *못 막는 것* 이 같은 자리에서 대비돼야 한다.
# 가운데 칸에 초점을 준다 — 리전 클러스터를 충분하다고 읽는 것이 이 절이 깨려는 오해다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 588
d = D(W, H, "KUBERNETES UP AND RUNNING · 21-01",
      "인프라 장애 도메인과 소프트웨어 장애 도메인은 다르다",
      "리전 클러스터는 존을 나눠 인프라 장애를 견딘다. 그래도 클러스터는 특정 Kubernetes "
      "버전에 묶여 있고, 업그레이드가 애플리케이션을 깨뜨릴 수 있다.",
      "원서 21장 논증 그대로 — 저자는 여기까지만 말하고 처방을 붙이지 않는다")

CW, GAP = 386, 18
Y0, CH = 132, 296
CARDS = [
    ("단일 클러스터", "한 곳에 배포", MUTED, False,
     ["—"],
     ["데이터센터 정전·광케이블 절단", "잘못 나간 소프트웨어 배포", "Kubernetes 업그레이드"]),
    ("리전 클러스터", "여러 독립 존에 걸침", ACC, True,
     ["데이터센터 정전·광케이블 절단", "존 단위 인프라 장애"],
     ["Kubernetes 업그레이드", "API 폐기·동작 변경", "릴리스에 섞여 든 버그"]),
    # ⚠ 초판은 여기에 "버전을 갈라 굴림 / Kubernetes 버전 자체를 막는다" 라고 적었다가
    #   적대적 검증에서 반증됐다. 원서는 클러스터 간 버전 분리를 한 번도 권하지 않고,
    #   오히려 버전 스큐를 피해야 할 것으로 다룬다. 원서가 멈춘 자리에서 함께 멈춘다.
    ("멀티클러스터", "클러스터를 여럿 둔다", OK, False,
     ["앞의 것 전부", "한 클러스터의 사고가 전부를 끌고 가지 않는다"],
     ["운영 복잡도가 오른다", "일관성을 직접 지켜야 한다"]),
]
for i, (title, sub, c, focal, blocks, leaks) in enumerate(CARDS):
    x = 24 + i * (CW + GAP)
    if focal:
        d.tone(x, Y0, CW, CH, c, 8, "0C", 1.5)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, Y0 + 30, title, 14, c, KR, "start", 600)
    d.t(x + CW - 20, Y0 + 30, sub, 10, SOFT, KR, "end")
    d.line(x + 20, Y0 + 46, x + CW - 20, Y0 + 46, RULE, 0.8)

    d.t(x + 20, Y0 + 70, "막는다", 9, OK, KR, "start")
    for j, b in enumerate(blocks):
        yy = Y0 + 80 + j * 28
        d.o.append(f'<rect x="{x+20}" y="{yy}" width="{CW-40}" height="22" rx="4" '
                   f'fill="{OK}0C" stroke="{OK}" stroke-width="0.8"/>')
        d.t(x + 32, yy + 15, ddx.fit(b, 10, CW - 64, b), 10, OK, KR, "start")

    LY = Y0 + 176
    # 셋째 칸이 아래에 적는 것은 "안 막히는 장애" 가 아니라 "치르는 비용" 이다.
    # 같은 라벨을 붙이면 종류가 다른 것을 같은 것처럼 읽게 된다.
    d.t(x + 20, LY, "못 막는다" if i < 2 else "치르는 것", 9, BAD, KR, "start")
    for j, b in enumerate(leaks):
        yy = LY + 10 + j * 28
        d.o.append(f'<rect x="{x+20}" y="{yy}" width="{CW-40}" height="22" rx="4" '
                   f'fill="{BAD}0C" stroke="{BAD}" stroke-width="0.8"/>')
        d.t(x + 32, yy + 15, ddx.fit(b, 10, CW - 64, b), 10, BAD, KR, "start")
    if i < 2:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + CW + GAP - 2, Y0 + CH / 2)], SOFT, "soft", 1.3)

BY = Y0 + CH + 26
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "가운데 칸을 충분하다고 읽는 것이 이 절이 깨려는 오해다. "
                 "존을 나눠도 클러스터는 여전히 한 버전에 묶여 있다.", 11, ACC, KR, "start")
d.legend(BY + 40, [("오해가 생기는 자리", ACC), ("막아 주는 것", OK), ("새는 것", BAD)])
d.save("../21-01.failure-domains.svg")
print("필요 h:", BY + 40 + 48, "· 실제:", H)
