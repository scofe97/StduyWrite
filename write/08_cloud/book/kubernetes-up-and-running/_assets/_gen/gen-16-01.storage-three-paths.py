# 16-01 §스토리지를 들이는 세 갈래
# 본문이 축을 준다 — "뒤로 갈수록 클러스터에 더 깊이 들이는 대신 복잡도가 올라간다".
# 그러니 셋을 나란한 카드로 늘어놓으면 안 되고 방향이 있어야 한다. 그리고 셋 다 무언가를
# 내주므로, 얻는 것 옆에 *포기하는 것* 칸을 같은 자리에 두어야 고르는 데 쓸 수 있다.
# 초점은 둘째다 — 본문이 "이 장에서 가장 값진 대목" 이라 적고 이 노트가 서 있는 자리다.
# 타입 스펙: type-process.md — 세 갈래가 같은 의미 슬롯(번호 · 이름 · 얻는 것 · 포기하는 것)으로
#           반복되고, 아래 방향 화살표가 읽는 순서를 나른다. 본문이 "뒤로 갈수록 깊이 들이고
#           복잡도가 올라간다" 라고 축을 주므로 나란한 카드가 아니라 방향이 있어야 한다.
#           어긋나는 지점: 정본의 lane 은 행위 주체인데 여기 열은 *대안* 이다 — 자매 책에서도
#           같은 자리에서 적어 둔 메뉴 공백이다. matrix 는 기각 — 저자가 방향을 명시했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 560
d = D(W, H, "KUBERNETES UP AND RUNNING · 16-01",
      "깊이 들일수록 복잡도를 치른다",
      "ReplicaSet 같은 프리미티브는 모든 컨테이너가 동일하고 교체 가능하다고 전제한다. "
      "대부분의 스토리지 솔루션은 그렇지 않다. 그 어긋남을 푸는 길이 셋이다.",
      "셋 다 무언가를 내준다 — 무엇을 내주는지가 고르는 기준이다")

Y0, CH = 140, 292      # 카드 높이는 안쪽 배치의 합으로 잡는다 (마지막 상자 268 + 여백 24)
Y1 = Y0 + CH
CARDS = [
    ("01 · 밖에 둔다", "이름만 가져온다", "ExternalName Service 가 CNAME 을 채운다",
     ["쿠버네티스의 이름 짓기와 디스커버리를 그대로 쓴다",
      "테스트와 운영이 같은 이름의 Service 를 본다"],
     "헬스 체킹을 전혀 하지 않는다", "믿을 만한지는 전적으로 사용자 책임이다", BAD, None),
    ("02 · 안으로 들인다", "복제를 포기한다", "데이터베이스 파드를 하나만 띄운다",
     ["복제된 스토리지의 난제가 애초에 생기지 않는다",
      "단일 머신에서 돌리는 것보다 덜 신뢰할 만하지 않다"],
     "업그레이드와 머신 장애 때의 다운타임", "포기하는 것은 이것 하나뿐이다", ACC, None),
    ("03 · 네이티브로 간다", "StatefulSet 으로 복제한다", "고유 인덱스가 붙은 호스트명 · 순서 있는 생성",
     ["StatefulSet 과 PVC 와 liveness 프로빙을 합친다",
      "견고하고 확장 가능한 클라우드 네이티브 설치가 된다"],
     "설정과 운영의 복잡도", "얻는 것이 가장 많고 치를 것도 가장 많다", WARN, "저자의 종착지"),
]
CW, GAP = 386, 18
for i, (eb, title, sub, gains, loss, lossub, c, tag) in enumerate(CARDS):
    x = 24 + i * (CW + GAP)
    focal = c is ACC
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y0}" width="{CW}" height="{Y1-Y0}" rx="8" '
                   f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y0, CW, Y1 - Y0, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, Y0 + 26, eb, 8, SOFT, MONO, "start")
    if tag: d.t(x + CW - 20, Y0 + 26, tag, 9, SOFT, KR, "end")
    d.t(x + 20, Y0 + 54, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, Y0 + 76, ddx.fit(sub, 10, CW - 40, sub), 10, SOFT, KR, "start")
    d.line(x + 20, Y0 + 92, x + CW - 20, Y0 + 92, RULE, 0.8)

    d.t(x + 20, Y0 + 116, "얻는 것", 9, SOFT, KR, "start")
    for j, g in enumerate(gains):
        yy = Y0 + 128 + j * 30
        d.o.append(f'<rect x="{x+20}" y="{yy}" width="{CW-40}" height="24" rx="4" '
                   f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
        d.t(x + 32, yy + 16, ddx.fit(g, 10, CW - 64, g), 10, MUTED, KR, "start")

    d.t(x + 20, Y0 + 206, "포기하는 것", 9, SOFT, KR, "start")
    d.o.append(f'<rect x="{x+20}" y="{Y0+216}" width="{CW-40}" height="52" rx="5" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    d.t(x + CW / 2, Y0 + 238, ddx.fit(loss, 12, CW - 60, loss), 12, c, KR, "middle", 600)
    d.t(x + CW / 2, Y0 + 258, ddx.fit(lossub, 10, CW - 60, lossub), 10, c, KR)

AY = Y1 + 28
d.path(f"M 24 {AY} L {24 + CW*3 + GAP*2} {AY}", SOFT, 1.4, m="soft")
d.t((24 + 24 + CW * 3 + GAP * 2) / 2, AY - 10,
    "뒤로 갈수록 클러스터에 더 깊이 들이고, 그만큼 복잡도가 올라간다", 11, SOFT, KR)
d.t(24, AY + 26, "둘째가 성립하지 않는 거래라면 첫째로 물러나거나 셋째로 넘어가라고 저자가 길을 열어 둔다. "
                 "대규모·미션 크리티컬에는 둘째의 다운타임이 받아들일 수 없는 것일 수 있다.",
     11, MUTED, KR, "start")

d.legend(AY + 52, [("이 노트가 서는 자리", ACC), ("아무도 확인해 주지 않는다", BAD), ("치러야 할 복잡도", WARN)])
d.save("16-01.storage-three-paths.svg")
print("h 필요:", AY + 52 + 48, " 실제:", H)
