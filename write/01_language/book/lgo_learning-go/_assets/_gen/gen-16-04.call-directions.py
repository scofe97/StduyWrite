# 16-04.call-directions — Go 의 main 이 C 의 add 를 부르고, add 는 //export 한 Go 함수 doubler 를 불러 결과를 더해 돌려준다
# 본문 요구(16-04 §1 「//export 로 Go 함수를 C 에 내보냅니다」): main 이 C.add(3, 2) → example.c 의 add 가 _cgo_export.h 로 doubler(3) 호출 →
#           6 반환 → add 가 6 + 2 = 8 을 돌려줌 → main 이 8 을 찍는다.
# 타입 스펙: type-sequence — 레인 셋(Go main · C add · Go doubler), 시간은 위→아래. focal 은 C 가 Go 를 부르는 화살표 하나.
# 사실 출처: Learning Go 2판 16장 「Cgo Is for Integration, Not Performance」, 원서 저장소 sample_code/call_go_from_c, go1.27.1 실행(2026-09-29) — 8.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520
d = Seq(W, H, "SEQUENCE · 16-04 §1",
        "Go 에서 C 로, C 에서 다시 Go 로 부릅니다",
        "main 이 import \"C\" 앞 주석에 선언한 C 함수 add 를 C.add(3, 2) 로 부른다. example.c 의 add 는 cgo 가 만든 _cgo_export.h 를 포함해 "
        "//export 로 내보낸 Go 함수 doubler 를 doubler(3) 으로 부르고 6 을 받는다. add 는 6 에 2 를 더한 8 을 돌려주고 main 이 8 을 찍는다.",
        lead="위에서 아래로 시간이 흐릅니다. 가운데 레인이 C 코드입니다.")
d.lanes([("Go · main", "main.go"), ("C · add", "example.c"), ("Go · doubler", "//export doubler")], y0=96, lane_w=210)
d.rails(440)


def state(key, txt, y, c):
    # Seq.state 는 반투명 칩이라 레일이 비치고 한글 폭을 작게 어림한다 — 불투명 바탕과 글자별 폭으로 다시 그린다
    x = d.LX[key]
    w = sum(11.0 if "가" <= ch <= "힣" else 6.9 for ch in txt) + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 11, c, MONO, "middle", 600)

d.msg("Go · main", "C · add", "C.add(3, 2)", 188)
d.msg("C · add", "Go · doubler", "doubler(3)", 236, ACC, "acc", sub="_cgo_export.h 로 선언을 얻음")
d.msg("Go · doubler", "C · add", "6", 300, OK, "ok")
state("C · add", "6 + 2", 344, INFO)
d.msg("C · add", "Go · main", "8", 392, OK, "ok")
state("Go · main", "fmt.Println → 8", 428, INFO)

d.legend(464, [("C 가 Go 를 부름", ACC), ("반환 값", OK), ("계산", INFO)])
d.save("16-04.call-directions.svg")
print("ok 16-04 call-directions")
