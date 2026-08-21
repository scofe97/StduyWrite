# 09-03 §2 — 체인 밖에 있어 교체가 닿지 않는다
# 앞 도식이 "..data 하나만 튼다"를 세웠으므로, 여기서는 그 교체가 어디까지 전파되는지가
# 주제다. subPath 를 0 단으로 그려 체인 밖이라는 사실이 그림에서 나와야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 700, "KUBERNETES IN ACTION · 09-03",
      "체인 밖이라 교체가 닿지 않는다",
      "subPath 는 마운트 시점에 ..data 가 가리키던 실제 파일 하나를 대상 경로에 직접 연결한다. "
      "..data 를 새 디렉터리로 틀어도 그 교체는 ..data 를 경유하는 파일에만 전파된다.",
      "같은 볼륨을 /etc/live 와 /etc/frozen/app.conf 에 함께 마운트")

ddx.band(d, 100, 336, "일반 마운트 — 2 단 체인", x=24, w=1172)
CH = [("/etc/live/app.conf", "심링크", 200), ("..data/app.conf", "심링크", 520),
      ("..2026_…_17_07_32/app.conf", "실파일 · after", 880)]
for t, s, cx in CH:
    ddx.node(d, cx, 236, t, s, 300, 76, ACC if cx == 520 else INFO)
for a, b in ((350, 370), (670, 730)):
    d.path(f"M {a} 236 L {b} 236", ACC, 1.5, m="acc")
d.t(1150, 236, "갱신된다", 11, OK, KR, "end")
d.t(520, 300, "여기만 틀면 뒤가 따라온다", 10, ACC, KR)

ddx.band(d, 360, 596, "subPath 마운트 — 0 단", x=24, w=1172)
ddx.node(d, 200, 496, "/etc/frozen/app.conf", "실파일 · -rw-r--r--", 300, 76, BAD)
ddx.node(d, 880, 496, "..2026_…_17_06_11/app.conf", "마운트 시점의 실파일 · before", 340, 76, INFO)
d.path("M 350 496 L 706 496", BAD, 1.5, m="bad")
d.t(528, 476, "마운트 시점에 직접 연결됐다", 11, BAD, KR)
d.t(528, 520, "..data 를 거치지 않는다", 11, BAD, KR)
d.t(1150, 496, "갱신되지 않는다", 11, BAD, KR, "end")

d.t(24, 624, "우회하려면 볼륨 전체를 다른 디렉터리에 마운트하고, 원하는 위치에 그 파일을 가리키는 심링크를 "
                  "컨테이너 이미지에 미리 만들어 둔다.", 11, MUTED, KR, "start")
d.legend(652, [("체인 위의 링크", ACC), ("체인 밖 실파일", BAD), ("가리켜지는 실체", INFO)])
d.save("09-03-subpath-no-update.svg")
print("ok")
