# 00-03.chapter-overview — 물음 하나를 풀려고 쌓는 다섯 고리
# 본문 요구(00-03 학습 목표 지도 문단): §1~§4 가 기다림이 생기는 고리이고 §5 가 그 사슬을 끊는 도구다 — 절이 한 줄로 이어진다.
# 타입 스펙: type-flowchart — 다섯 단계를 가로로 잇는 흐름. 앞 넷은 기다림이 생기는 자리(warn), 마지막이 끊는 도구(focal).
# 사실 출처: 본문 §1~§5.
from dd import D, INK, MUTED, SOFT, ACC, WARN, KR
from ddk import node, harrow

W, H = 960, 300
X, NW, NH, STEP, Y = 24, 164, 76, 187, 132
steps = [("§1 main", "멈추면 안 끝남"), ("§2 io.Copy", "src 가 끝나야 끝남"),
         ("§3 defer", "return 해야 실행"), ("§4 WaitGroup", "Done 이 와야 끝남"),
         ("§5 context", "바깥에서 Close")]
d = D(W, H, "FLOWCHART · 00-03 OVERVIEW", "서버가 안 꺼지는 이유를 푸는 다섯 고리",
      "§1 main goroutine 이 멈추면 프로그램이 끝나지 않고, §2 io.Copy 는 src 가 끝나야 끝나며, §3 defer 는 return 해야 "
      "실행되고, §4 WaitGroup 은 Done 이 와야 끝난다. 이 넷이 기다림의 사슬을 만들고 §5 context 가 바깥에서 자원을 닫아 끊는다.",
      lead="왼쪽 넷이 기다림이 생기는 고리, 오른쪽 끝이 그 사슬을 끊는 도구입니다.")
for i, (t, s) in enumerate(steps):
    x = X + i * STEP
    node(d, x, Y, NW, NH, t, s, ACC if i == 4 else WARN, i == 4)
    if i < 4:
        harrow(d, x + NW + 4, x + STEP - 4, Y + NH / 2)
d.legend(248, [("기다림이 생기는 고리", WARN), ("사슬을 끊는 도구", ACC)])
d.save("00-03.chapter-overview.svg")
print("ok 00-03 overview")
