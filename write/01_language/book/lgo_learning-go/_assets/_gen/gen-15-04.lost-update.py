# 15-04.lost-update — 두 고루틴이 counter 를 같은 값으로 읽어 각자 1 을 더해 쓰면 증가 하나가 사라진다. -race 가 race.go:12 를 짚는다
# 본문 요구(15-04 §3 「-race 는 잠금 없이 같은 변수를 건드리는 곳을 찾습니다」): counter++ 는 읽기 · 더하기 · 쓰기 세 단계라, 두 고루틴이
#           같은 값 n 을 읽으면 둘 다 n+1 을 쓰고 증가 하나가 사라진다. 그래서 5,000 이 아니라 3,256~4,322 가 나왔다.
# 타입 스펙: type-sequence — 레인 셋(고루틴 A · counter · 고루틴 B), 시간은 위→아래. 값은 기호 n 으로 적는다(특정 실행값이 아님).
#           focal 은 뒤늦게 덮어쓰는 B 의 쓰기 화살표 하나.
# 사실 출처: Learning Go 2판 15장 「Finding Concurrency Problems with the Data Race Detector」, go1.27.1 실행(2026-09-28) —
#           10회 중 7회 실패(3,256~4,322), -race 출력 Read/Previous write 모두 race.go:12.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520
d = Seq(W, H, "SEQUENCE · 15-04 §3",
        "두 고루틴이 같은 값을 읽고 쓰면 한쪽의 증가가 사라집니다",
        "counter++ 는 읽고 더하고 쓰는 세 단계다. 고루틴 A 와 B 가 잠금 없이 같은 값 n 을 읽으면 둘 다 n+1 을 계산해 쓰고, 나중에 쓴 B 가 A 의 결과를 덮어써 "
        "counter 는 n+2 가 아니라 n+1 이 된다. 다섯 고루틴이 1,000번씩 늘린 결과가 5,000 보다 작게 나온 까닭이다. go test -race 는 이 읽기와 쓰기를 race.go:12 의 데이터 레이스로 보고한다.",
        lead="n 은 두 고루틴이 읽은 같은 값입니다. 위에서 아래로 시간이 흐릅니다.")
d.lanes([("고루틴 A", "counter++"), ("counter", "공유 변수"), ("고루틴 B", "counter++")], y0=96, lane_w=210)
d.rails(420)

d.msg("counter", "고루틴 A", "읽기 · n", 188)
d.msg("counter", "고루틴 B", "읽기 · n", 228)
d.state("고루틴 A", "n + 1 계산", 268, INFO)
d.state("고루틴 B", "n + 1 계산", 268, INFO)
d.msg("고루틴 A", "counter", "쓰기 · n+1", 312)
d.msg("고루틴 B", "counter", "쓰기 · n+1 (덮어씀)", 352, ACC, "acc")
def chip(key, txt, y, c):
    x = d.LX[key]
    w = sum(11.0 if "가" <= ch <= "힣" else 6.9 for ch in txt) + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 11, c, KR, "middle", 600)


chip("counter", "n+1 · 증가 하나가 사라짐", 396, BAD)

d.t(W / 2, 444, "go test -race → WARNING: DATA RACE · Read / Previous write · race.go:12", 12, INFO, MONO, "middle", 600)
d.legend(468, [("계산", INFO), ("덮어쓰는 쓰기", ACC), ("잃은 증가", BAD)])
d.save("15-04.lost-update.svg")
print("ok 15-04 lost-update")
