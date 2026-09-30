# 00-02.chapter-overview — 서버 한 번의 수명을 따라 읽은 다섯 장면
# 본문 요구(00-02 학습 목표 지도 문단): 절 순서가 서버가 뜨고·기다리고·FD 를 쥐고·닫히고·닫힌 뒤의 시간 순서다.
# 타입 스펙: type-timeline — 가로 기준선 위 다섯 눈금, 눈금마다 장면·그때 본 출력·다루는 절. focal 은 가장 많이 막힌 §3.
# 사실 출처: gonet-lab Phase 0 실습 출력 (2026-09-27).
from dd import D, INK, MUTED, SOFT, RULE, ACC, KR, MONO
from ddk import kr

W, H = 960, 316
X0, STEP, BY = 100, 190, 200
d = D(W, H, "TIMELINE · 00-02 OVERVIEW", "서버 한 번의 수명을 따라 읽은 다섯 장면",
      "gonet 서버를 strace 아래에서 띄우고 끄는 동안의 다섯 장면을 시간 순서로 놓은 지도. 뜨기는 socket·bind·listen, "
      "기다리기는 accept4 의 EAGAIN, FD 쥐기는 /proc/pid/fd, 닫기는 kill -INT 뒤의 close, 닫힌 뒤는 FIN-WAIT-2 와 "
      "CLOSE-WAIT 를 보고, 각 장면이 문서의 §1~§5 에 대응한다.",
      lead="눈금마다 그 장면에서 본 출력과, 그것을 읽는 절을 적었습니다.")
d.line(48, BY, W - 48, BY, RULE, 1.2)
scenes = [("뜨기", "socket · bind · listen", "§1 strace 읽기"),
          ("기다리기", "accept4 = EAGAIN", "§2 논블로킹"),
          ("FD 쥐기", "/proc/<pid>/fd", "§3 FD 표"),
          ("닫기", "kill -INT → close", "§4 코드 close"),
          ("닫힌 뒤", "FIN-WAIT-2 · CLOSE-WAIT", "§5 상태 · 에러")]
for i, (t, obs, sec) in enumerate(scenes):
    x = X0 + i * STEP
    c = ACC if i == 2 else SOFT
    d.tone(x - 6, BY - 6, 12, 12, c, 2, "40", 1.2)
    d.t(x, 144, t, 15, ACC if i == 2 else INK, KR, "middle", 600)
    d.t(x, 168, obs, 12, MUTED, kr(obs), "middle")
    d.chip(x, 236, sec, ACC if i == 2 else MUTED, 12)
d.legend(268, [("가장 많이 막힌 곳", ACC)])
d.save("00-02.chapter-overview.svg")
print("ok 00-02 overview")
