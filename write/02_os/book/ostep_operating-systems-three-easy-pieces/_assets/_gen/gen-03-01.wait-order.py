# 03-01 「부모를 막아 순서 고정하기」 — 부모가 먼저 도는 경우와 자식이 먼저 도는 경우 모두 자식의 출력이 부모의 출력보다 앞선다.
# 본문 근거: 이 노트 「2. wait 로 자식의 끝 기다리기」.
# 값 근거: 개념 도식이라 값은 없다. 막대 길이는 상대 순서만 뜻하며 실제 시간이 아니다.
# 공식 근거: OSTEP 5장 §5.2 — wait() 는 자식이 실행을 마칠 때까지 부모의 실행을 늦춘다. p2.c 는 항상 child 를 먼저 찍는다.
# 타입 스펙: type-gantt — 두 경우를 같은 시간축에 놓고 부모·자식 막대의 앞뒤를 본다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 920, 500
d = D(W, H, "OSTEP · 03-01 §2",
      "wait() 가 있으면 어느 쪽이 먼저 돌아도 child 가 먼저 찍힌다",
      "부모가 먼저 도는 경우 부모는 fork 뒤 wait 에서 막혀 있고 자식이 출력하고 끝나면 막힘이 풀려 부모가 출력한다. "
      "자식이 먼저 도는 경우 부모는 CPU 를 기다리다가 자식이 끝난 뒤 wait 를 부르면 바로 돌아와 출력한다. 두 경우 모두 자식의 출력이 부모의 출력보다 앞선다.",
      lead="막대 길이는 순서만 뜻하며 실제 시간이 아닙니다.")

X0, BH = 200, 30


def bar(x1, x2, y, label, c, dash=None, op="22"):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    d.o.append(f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="{BH}" rx="4" fill="{c}{op}" stroke="{c}" stroke-width="1.1"{ds}/>')
    d.t((x1 + x2) / 2, y + 20, label, 12, c, KR, "middle", 600)


def case(y0, title, yp, yc):
    d.t(24, y0, title, 13, INK, KR, "start", 600)
    d.line(24, y0 + 10, W - 48, y0 + 10, RULE, 0.8)
    d.t(24, yp + 20, "부모", 12, MUTED, KR, "start", 600)
    d.t(24, yc + 20, "자식", 12, MUTED, KR, "start", 600)


# 경우 가: 부모가 먼저
yp, yc = 150, 214
case(120, "부모가 먼저 도는 경우", yp, yc)
bar(X0, 300, yp, "fork()", INFO)
bar(300, 480, yp, "wait() 에서 막힘", WARN, "5 4")
bar(480, 680, yp, "parent of … 출력", ACC)
bar(300, 480, yc, "child 출력 후 종료", OK)
d.arrow([(480, yc), (480, yp + BH + 2)], OK, "ok", 1.4)
d.t(490, yc - 11, "끝나면 막힘이 풀림", 11, MUTED, KR, "start")

# 경우 나: 자식이 먼저
yp, yc = 320, 384
case(290, "자식이 먼저 도는 경우", yp, yc)
bar(X0, 300, yp, "fork()", INFO)
bar(300, 480, yp, "CPU 를 기다림", SOFT, "5 4")
bar(480, 620, yp, "wait() 즉시 반환", WARN)
bar(620, 800, yp, "parent of … 출력", ACC)
bar(300, 480, yc, "child 출력 후 종료", OK)

d.t(X0, 440, "시간 →", 11, SOFT, KR, "start")
d.legend(H - 40, [("fork", INFO), ("자식 출력", OK), ("부모 출력", ACC), ("막힘 · 대기", WARN)])
d.save("03-01.wait-order.svg")
print("ok 03-01 wait-order")
