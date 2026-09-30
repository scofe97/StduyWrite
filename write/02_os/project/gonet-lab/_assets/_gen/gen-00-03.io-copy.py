# 00-03.io-copy — io.Copy 가 끝나는 조건은 src 가 정한다
# 본문 요구(00-03 §2): "src 가 EOF 에 닿거나 에러가 날 때까지 반복하고 EOF 로 끝나면 nil" · "src 가 키보드라면 …
#           이 호출은 돌아오지 않습니다" — Read 결과에 따라 갈라지는 반복 논리다.
# 타입 스펙: type-flowchart — Read → 무엇이 왔나 → 데이터면 Write 후 다시 Read(위쪽 되돌림), EOF·에러·무소식 셋으로 갈림.
#           focal 은 끝나지 않는 갈래.
# 사실 출처: go doc io.Copy (go1.25.1).
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, KR, MONO
from ddk import node, harrow, varrow

W, H = 960, 452
Y, NH = 150, 52
d = D(W, H, "FLOWCHART · 00-03 IO.COPY", "io.Copy 가 끝나는 조건은 src 가 정합니다",
      "io.Copy(dst, src) 는 src.Read 결과에 따라 갈라진다. 데이터가 오면 dst 에 쓰고 다시 Read 로 돌아가고, EOF 면 nil, "
      "에러면 그 에러를 돌려주며 끝난다. 아무것도 오지 않으면 Read 에서 계속 기다리며 끝나지 않는다.",
      lead="데이터가 오는 한 위쪽 고리를 돌고, 끝나는 길은 EOF 와 에러 둘뿐입니다.")
node(d, 24, Y, 176, NH, "io.Copy(dst, src)", None, None, False, 13)
node(d, 240, Y, 150, NH, "src.Read", None)
node(d, 430, Y, 170, NH, "무엇이 왔나", None)
node(d, 646, Y, 150, NH, "dst.Write", None)
harrow(d, 206, 234, Y + NH / 2)
harrow(d, 396, 424, Y + NH / 2)
harrow(d, 606, 640, Y + NH / 2, label="데이터")
d.arrow([(721, Y - 4), (721, 124), (315, 124), (315, Y - 6)], SOFT, "soft", 1.3)
d.t(518, 116, "다시 Read", 12, MUTED, KR, "middle")
d.line(515, Y + NH + 4, 515, 268, SOFT, 1.3)
d.line(188, 268, 768, 268, SOFT, 1.3)
outs = [(88, "EOF", "nil 반환", OK, False), (415, "에러", "err 반환", BAD, False), (648, "아무것도 안 옴", "Read 에서 계속 대기", ACC, True)]
for x, t, s, c, f in outs:
    w = 240 if f else 200
    cx = x + w / 2
    d.arrow([(cx, 268), (cx, 300)], SOFT, "soft", 1.3)
    node(d, x, 304, w, 60, t, s, c, f)
d.legend(392, [("정상 종료", OK), ("에러 종료", BAD), ("끝나지 않는 경우", ACC)])
d.save("00-03.io-copy.svg")
print("ok io-copy")
