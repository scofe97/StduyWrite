# 06-02 §3 스택 프레임 — square() 가 실행되는 동안 main·doCalc·square 의 프레임이 쌓인 모습
# 근거: TLPI 6.5 Figure 6-3(PDF 12쪽 그림 대조), Listing 6-1 의 주석("Allocated in frame for …")
# 값 근거: 프레임별 변수 이름은 Listing 6-1 주석이다(main: argc·argv·p, doCalc: val·t, square: x·result). 호출 연결 정보는 6.5 본문(호출된 함수 프레임에 부른 쪽 레지스터 사본).
# 타입 스펙: type-layers — 프레임을 위에서 아래로 쌓고 자라는 방향과 스택 포인터를 표지로 단다
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 520
BX, BW = 250, 440
d = D(W, H, "TLPI · 06-02 §3",
      "호출마다 스택 프레임이 한 겹 쌓인다",
      "square() 가 실행되는 동안의 스택. main() 이 doCalc() 를, doCalc() 가 square() 를 불렀고 프레임마다 변수와 호출 연결 정보가 든다.",
      "프레임 위에는 C 런타임 시작 함수의 프레임이 있고, 스택 포인터는 가장 나중에 쌓인 프레임을 가리킵니다.")

# 시작 함수 프레임 (점선)
y = 104
d.path(f"M {BX} {y} h{BW} v40 h-{BW} z", SOFT, 1.2, dash="5 4")
d.t(BX + BW / 2, y + 25, "C 런타임 시작 함수의 프레임", 13, MUTED, KR, "middle", 500)

frames = [
    ("main()", "argc · argv · p", None),
    ("doCalc()", "val · t", None),
    ("square()", "x · result", ACC),
]
fy = 152
FH, FS = 72, 80
for name, vars_, focal in frames:
    if focal:
        d.tone(BX, fy, BW, FH, focal, 6, "14", 1.6)
    else:
        d.box(BX, fy, BW, FH, PAPER2, RULE, 1.0, 6)
    d.t(BX - 14, fy + FH / 2 + 5, name, 14, focal or INK, MONO, "end", 600)
    d.tone(BX + 8, fy + 8, 256, 56, INFO, 4, "14", 1.0)
    d.t(BX + 20, fy + 28, "인자·지역 변수", 12, MUTED, KR, "start")
    d.t(BX + 20, fy + 49, vars_, 13, INFO, MONO, "start", 600)
    d.tone(BX + 272, fy + 8, 160, 56, WARN, 4, "14", 1.0)
    d.t(BX + 284, fy + 28, "호출 연결 정보", 12, MUTED, KR, "start")
    d.t(BX + 284, fy + 49, "PC 등 사본", 13, WARN, KR, "start", 600)
    fy += FS
bottom = fy - (FS - FH)

# 스택 포인터
d.arrow([(BX + BW + 96, bottom - 4), (BX + BW + 4, bottom - 4)], ACC, "acc", 1.5)
d.chip(BX + BW + 140, bottom - 4, "스택 포인터", ACC, 12, 7)

# 자라는 방향
d.arrow([(30, 156), (30, bottom - 4)], MUTED, "ar", 1.4)
d.t(44, 266, "스택이", 12, MUTED, KR, "start", 500)
d.t(44, 284, "자라는 방향", 12, MUTED, KR, "start", 500)

# 아직 쓰지 않은 영역
d.path(f"M {BX} {bottom + 16} h{BW} v44 h-{BW} z", RULE, 1.0, dash="5 4")
d.t(BX + BW / 2, bottom + 43, "다음 호출이 프레임을 놓을 자리", 13, SOFT, KR, "middle", 500)

d.legend(H - 40, [("인자·지역 변수", INFO), ("호출 연결 정보", WARN), ("실행 중인 함수", ACC), ("시작 함수 프레임", SOFT)])
d.save("06-02.stack-frames.svg")
print("ok 06-02.stack-frames.svg")
