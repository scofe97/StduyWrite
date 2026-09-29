# 16-04.handle-roundtrip — Person 은 Go 의 핸들 표에 남고 C 에는 uintptr 손잡이만 건너가며, processor 가 손잡이로 값을 되찾고 Delete 한다
# 본문 요구(16-04 §2 「cgo.Handle 은 값을 정수 손잡이로 바꿔…」): main 이 cgo.NewHandle(p) → 손잡이(uintptr) → C.in_c(handle) →
#           in_c 가 processor(handle) → processor 가 h.Value().(Person) 으로 Person 을 되찾아 찍고 h.Delete().
# 타입 스펙: type-sequence — 레인 넷(Go main · C in_c · Go processor · 핸들 표). 핸들 표를 맨 오른쪽에 둬 processor 와의 왕복이 이웃 레인 사이로만 오간다, 시간은 위→아래. focal 은 C 를 건너는 손잡이 화살표 하나.
# 사실 출처: Learning Go 2판 16장, 원서 저장소 sample_code/handle, go1.27.1 실행(2026-09-29) — Jon 21.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 600
d = Seq(W, H, "SEQUENCE · 16-04 §2",
        "값은 Go 에 남고 C 에는 정수 손잡이만 건너갑니다",
        "Person 에는 포인터를 품은 string 필드가 있어 C 로 그대로 넘길 수 없다. main 이 cgo.NewHandle(p) 로 값을 Go 쪽 핸들 표에 맡기고 정수 손잡이를 받아 "
        "C.uintptr_t 로 바꿔 in_c 에 넘긴다. in_c 는 손잡이를 그대로 Go 의 processor 에 넘기고, processor 는 h.Value() 와 타입 단언으로 Person 을 되찾아 찍은 뒤 h.Delete() 로 지운다.",
        lead="위에서 아래로 시간이 흐릅니다. C 레인에는 정수만 지나갑니다.")
d.lanes([("Go · main", "p := Person{...}"), ("C · in_c", "show_handle.c"), ("Go · processor", "//export processor"), ("핸들 표", "Go 런타임 쪽")], y0=96, lane_w=180)
d.rails(520)


def state(key, txt, y, c):
    # Seq.state 는 반투명 칩이라 레일이 비치고 한글 폭을 작게 어림한다 — 불투명 바탕과 글자별 폭으로 다시 그린다
    x = d.LX[key]
    w = sum(11.0 if "가" <= ch <= "힣" else 6.9 for ch in txt) + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 11, c, MONO, "middle", 600)

d.msg("Go · main", "핸들 표", "cgo.NewHandle(p)", 188)
d.msg("핸들 표", "Go · main", "handle (uintptr)", 228, MUTED, "ar", dash="5 4")
d.msg("Go · main", "C · in_c", "C.in_c(handle)", 276, ACC, "acc", sub="정수만 C 를 건넘")
d.msg("C · in_c", "Go · processor", "processor(handle)", 340)
d.msg("Go · processor", "핸들 표", "h.Value()", 388)
d.msg("핸들 표", "Go · processor", "Person{Jon 21}", 428, OK, "ok")
state("Go · processor", "Println → Jon 21", 466, INFO)
d.msg("Go · processor", "핸들 표", "h.Delete()", 504, MUTED, "ar", dash="5 4")

d.legend(544, [("C 를 건너는 손잡이", ACC), ("되찾은 값", OK), ("출력", INFO)])
d.save("16-04.handle-roundtrip.svg")
print("ok 16-04 handle-roundtrip")
