# 02-05.ladder-narrowing — 사다리를 밟을 때마다 용의자 범위가 줄어든다
# 본문 요구: §2 는 단마다 "물은 것 / 답 / 좁혀진 범위"를 표로 정리하고(L271~277),
#           "L7 까지 갈 필요가 없었다"로 닫는다. 표는 다섯 줄을 나란히 두기만 해
#           *줄어든다*는 사실이 안 보인다. 아래 띠의 폭이 그 축소를 나른다.
# 타입 스펙: type-process.md — 단마다 "물은 것 / 실제 답 / 도구 / 남은 범위"라는 같은 슬롯이
#           반복되는 Stage framework with semantic slots. 02-03.triage-ladder 와 같은 근거이며
#           같은 폴더에서 같은 형태에 같은 타입을 쓴다는 selection 규칙을 따른다.
#           coral 은 원인이 확정된 칸 하나.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 632
d = D(W, H, "LADDER · SUSPECT RANGE NARROWS",
      "네 단을 밟자 원인이 한 칸으로 줄었다",
      "단마다 무엇을 물었고 실제로 무엇이 돌아왔는지, 그래서 남은 용의자가 어디까지 줄었는지를 "
      "같은 자리에 반복해 둡니다. 아래 띠의 폭이 남은 범위입니다.",
      lead="아래 띠의 폭이 곧 남은 용의자 — 네 번째에서 한 칸으로 줄어든다")

BW, GAP, X0 = 164, 26, 38
CY = 268
ddx.stage_chain(d, CY,
    ["이름이 풀리나", "닿나", "밖에서 붙나", "안에 소켓이 있나", "대화가 되나"],
    [("getent 만 성공", "dig +short 는 빈 줄", "/etc/hosts 로만 붙음", None),
     ("ttl=64 응답", "ping -c 3", "네트워크 무죄", None),
     ("8080 closed", "nmap -Pn · 밖에서", "밖과 소켓 사이", None),
     ("127.0.0.1:8080", "ss -tlnp · 안에서", "바인딩 한 칸", ACC),
     ("200 OK", "curl -v · 고친 뒤", "확인만 남음", None)],
    ["", "", "", ""],   # 코리도어 폭이 22px 라 라벨을 두면 넘친다 — 단 이름이 이미 물음을 말한다
    bw=BW, gap=GAP, x0=X0, sizes=(11.5, 11, 11))

CX = [X0 + BW // 2 + i * (BW + GAP) for i in range(5)]

# 남은 용의자 띠 — 폭이 곧 범위다. 마지막 두 칸은 원인이 확정된 뒤라 좁다.
d.t(36, 386, "남은 용의자", 11, SOFT, KR, "start", 600)
# 폭은 순서만 나른다 — 좁아진다는 사실이 논지이고 수치를 붙이지 않는다.
# 다섯째 칸은 원인이 확정된 뒤라 남은 용의자가 없다. 넷째와 같은 폭으로 그리면
# 안 줄어든 것처럼 읽히므로 상자를 아예 그리지 않는다.
RATIO = [1.00, 0.78, 0.52, 0.20, 0.00]
LABEL = ["전 구간", "이름 제외", "네트워크 제외", "바인딩", "없음"]
BAR_Y, BAR_H = 400, 26
for i, (cx, r) in enumerate(zip(CX, RATIO)):
    w = BW * r
    if i == 3:
        d.tone(cx - w / 2, BAR_Y, w, BAR_H, ACC, 4, "22", 1.3)
    elif r > 0:
        d.box(cx - w / 2, BAR_Y, w, BAR_H, PAPER2, RULE, 1.0, 4)
    d.t(cx, BAR_Y + 17, LABEL[i], 11, ACC if i == 3 else (SOFT if r == 0 else MUTED), KR)

d.t(36, 470, "네 번째 단에서 원인이 확정됐으므로 다섯 번째는 확인일 뿐입니다.", 12, MUTED, KR, "start")
d.t(36, 492, "아래가 깨져 있으면 위는 볼 필요가 없다 — 사다리의 원칙 그대로입니다.", 12, MUTED, KR, "start")
d.t(36, 520, "실무 순서는 아래부터 오르는 것이 아니라 curl 로 위에서 한 번 찔러 보고", 12, MUTED, KR, "start")
d.t(36, 542, "멈춘 지점부터 아래로 파는 것입니다. 사다리는 어디를 팔지 정하는 지도입니다.", 12, MUTED, KR, "start")
d.legend(572, [("원인이 확정된 단", ACC)])
d.save("02-05.ladder-narrowing.svg")
print("ok ladder-narrowing")
