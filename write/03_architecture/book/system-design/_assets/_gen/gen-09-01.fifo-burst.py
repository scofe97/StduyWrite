# 타입 스펙: type-data-flow — FIFO 큐 앞쪽 네 칸이 모두 같은 호스트의 URL 이라, 스레드 넷이 동시에 한 호스트로 요청을 보낸다. 여럿이 하나로 몰리는 fan-in 패턴.
# 사실 출처: 추출본 v2.txt 2481~2487행(FIFO 큐 BFS 와 같은 호스트 링크 몰림), PDF 138쪽 링크 추출 그림의 네 href(/wiki/Cong_Weixi·/wiki/Kay_Hagan·/wiki/Vladimir_Bukovsky·/wiki/John_Conyers),
#   호스트는 en.wikipedia.org 로 통일.
# Layout conventions: 큐 칸 폭 216·높이 40, 세로 stride 56(y=120·176·232·288), 스레드 폭 120, 호스트 상자 폭 216·높이 208. 화살표는 수평만. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, SOFT, KR, MONO

W, H = 960, 420
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 09-01 §3",
      "FIFO 큐는 같은 호스트의 URL 을 한꺼번에 내보낸다",
      "한 페이지의 링크는 대부분 같은 호스트를 가리켜서, 큐 앞쪽 칸이 모두 en.wikipedia.org 의 주소가 되고 스레드가 그 호스트를 동시에 두드린다.",
      "큐 앞 네 칸 = 호스트 하나 = 동시 요청 네 개")

URLS = ("/wiki/Cong_Weixi", "/wiki/Kay_Hagan", "/wiki/Vladimir_Bukovsky", "/wiki/John_Conyers")
QX, QW, QH = 24, 216, 40
TX, TW = 396, 120
HX, HW = 720, 216
Y0, ST = 120, 56

d.t(QX, Y0 - 16, "FIFO 큐 앞쪽", 13, SOFT, KR, "start", 600)
d.t(TX, Y0 - 16, "다운로더 스레드", 13, SOFT, KR, "start", 600)
d.t(HX, Y0 - 16, "대상 호스트", 13, SOFT, KR, "start", 600)

for i, u in enumerate(URLS):
    y = Y0 + i * ST
    d.tone(QX, y, QW, QH, INFO, 6, "10", 1.0)
    d.t(QX + 12, y + 25, u, 12, INK, MONO, "start")
    d.tone(TX, y, TW, QH, OK, 6, "10", 1.0)
    d.t(TX + TW // 2, y + 25, f"스레드 {i + 1}", 13, INK, KR, "middle", 600)
    d.arrow([(QX + QW + 4, y + QH // 2), (TX - 6, y + QH // 2)], MUTED, "ar", 1.4)
    d.arrow([(TX + TW + 4, y + QH // 2), (HX - 6, y + QH // 2)], MUTED, "ar", 1.4)

d.tone(HX, Y0, HW, 3 * ST + QH, ACC, 6, "12", 1.4)
d.t(HX + HW // 2, Y0 + 84, "en.wikipedia.org", 14, INK, MONO, "middle", 600)
d.t(HX + HW // 2, Y0 + 116, "동시 요청 4", 16, ACC, KR, "middle", 600)

d.legend(H - 56, [("큐 칸", INFO), ("스레드", OK), ("몰리는 호스트", ACC)])
d.save("09-01.fifo-burst.svg")
