# 타입 스펙: type-process
# 사실 출처: NPG Ch.13 Listing 13-1, 13-4, go doc log
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 920, 480
d = D(W, H, "LOG LINE ASSEMBLY · PROCESS",
      "log 패키지의 플래그·접두어 결합과 출력 줄 조립 과정",
      "l.Print 호출 시 전달된 메시지에 파일 위치 플래그와 접두어가 결합되어 "
      "최종 개행 문자가 붙은 바이트 열로 조립되는 순서입니다.",
      lead="Lshortfile 과 Lmsgprefix 플래그가 적용되어 접두어 위치가 조정됩니다.")

# 4개 단계 박스 (가로 배치)
Y0 = 130
BW, BH = 180, 200
GAP = 45
X0 = 36

steps = [
    ("1. 호출 수신", "메시지 인자 전달", INFO, [
        ("함수 호출", "l.Print(...)"),
        ("원시 메시지", "\"Canada is south...\""),
        ("버퍼 할당", "[]byte 준비"),
    ]),
    ("2. 파일 위치 확인", "Lshortfile 적용", OK, [
        ("런타임 호출", "runtime.Caller(...)"),
        ("파일명·줄", "log_test.go:27:"),
        ("버퍼 기록", "줄 머리에 위치"),
    ]),
    ("3. 접두어 위치 조정", "Lmsgprefix 적용", ACC, [
        ("설정 접두어", "\"example: \""),
        ("플래그 효과", "위치를 메시지 앞으로"),
        ("접두어 결합", "파일명 뒤에 덧붙임"),
    ]),
    ("4. 최종 줄 완성", "개행 추가 및 전달", WARN, [
        ("메시지 결합", "\"Canada is south...\""),
        ("종결자 추가", "\\n (개행 추가)"),
        ("출력 위임", "w.Write(p) 호출"),
    ]),
]

for i, (stitle, ssub, col, items) in enumerate(steps):
    x = X0 + i * (BW + GAP)
    d.tone(x, Y0, BW, BH, col, 6, "12", 1.2)
    d.t(x + BW / 2, Y0 + 26, stitle, 12, col, KR, "middle", 600)
    d.t(x + BW / 2, Y0 + 46, ssub, 11, SOFT, KR, "middle")
    d.line(x + 12, Y0 + 58, x + BW - 12, Y0 + 58, RULE, 0.8)

    for j, (lbl, val) in enumerate(items):
        iy = Y0 + 78 + j * 38
        d.t(x + 16, iy, lbl, 11, MUTED, KR, "start")
        d.t(x + 16, iy + 17, val, 11, INK, MONO, "start")

    if i < len(steps) - 1:
        ax1 = x + BW + 4
        ax2 = ax1 + GAP - 8
        ay = Y0 + BH / 2
        d.arrow([(ax1, ay), (ax2, ay)], SOFT, "soft", 1.4)

# 하단 최종 조립 문자열 배너
BY = 360
d.box(X0, BY, W - 72, 70, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(X0 + 20, BY + 26, "조립 완료된 최종 로그 줄 (Writer 로 전달)", 11, OK, KR, "start", 600)
d.t(X0 + 20, BY + 50, "log_test.go:27: example: Canada is south of Detroit\\n", 13, INK, MONO, "start", 600)

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.log-line-assembly.svg"
d.save(str(svg_path))
print("ok 13-01 log-line-assembly")
