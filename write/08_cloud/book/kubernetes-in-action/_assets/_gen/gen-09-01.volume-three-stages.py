# 09-01 §3 — 두 줄이 무엇을 바꾸는지 숫자로 본다
# 본문이 kind 실측 숫자 셋(0 · 1 · 6)을 든다. 설명 대신 그 숫자가 나란히 놓여야
# "두 줄의 무게"라는 말이 근거를 갖는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 09-01",
      "두 줄이 바꾸는 것을 숫자로 본다",
      "같은 quiz 파드를 세 형태로 돌려 mongo 컨테이너를 재시작해 봤다. 볼륨 두 줄과 init 컨테이너가 "
      "각각 무엇을 바꾸는지가 질문 수로 드러난다.",
      "kind k8s-lab v1.35 실측")

STAGE = [("① 볼륨 없이", "컨테이너 파일시스템에 쓴다", "0", "재시작하니 증발했다", BAD),
         ("② emptyDir 를 붙이면", "볼륨에 쓴다", "1", "재시작을 넘어 남았다", OK),
         ("③ init 컨테이너까지", "볼륨을 미리 채운다", "6", "뜰 때 자동으로 채워졌다", ACC)]
BW, GP = 340, 40
X0 = (1240 - (3 * BW + 2 * GP)) // 2
for i, (t, s, n, note, c) in enumerate(STAGE):
    cx = X0 + BW // 2 + i * (BW + GP)
    if c is ACC:
        d.o.append(f'<rect x="{cx-BW//2}" y="176" width="{BW}" height="240" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(cx - BW // 2, 176, BW, 240, PAPER2, c, 1.2, 8)
    d.t(cx, 212, t, 14, c, KR, "middle", 600)
    d.t(cx, 238, s, 11, MUTED, KR)
    d.t(cx, 316, n, 46, c, KR, "middle", 600)
    d.t(cx, 348, "재시작 뒤 질문 수", 10, SOFT, KR)
    d.t(cx, 388, note, 11, c, KR)

d.t(24, 480, "볼륨을 붙이는 변경은 두 줄이다 — 파드에 emptyDir 볼륨을 하나 더하고, 그 볼륨을 컨테이너에 마운트한다. "
             "그 두 줄이 ①과 ②를 가른다.", 11, MUTED, KR, "start")
d.t(24, 502, "③ 은 emptyDir 이 빈 채로 시작한다는 성질을 보완한다. init 컨테이너가 파일을 볼륨에 미리 복사해 두면 "
             "MongoDB 가 첫 시작 때 그것을 읽는다.", 11, MUTED, KR, "start")
d.legend(532, [("사라진다", BAD), ("남는다", OK), ("미리 채워진다", ACC)])
d.save("09-01-volume-three-stages.svg")
print("ok")
