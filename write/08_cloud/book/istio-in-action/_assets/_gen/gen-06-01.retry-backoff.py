# 06-01 §5 원 요청과 두 번의 재시도, 그 사이의 백오프.
# 본문: "attempts: 2 는 최대 세 번 전달을 뜻한다. 원 요청 한 번과 재시도 두 번. 재시도 사이에 Istio 는 25ms 를 기준으로
# 물러나며 각 재시도는 (25ms × 시도 번호)만큼 기다린다. 이 기준값은 현재 고정이다."
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 반환은 점선 + 채운 마커, 백오프는 자기 메시지 루프,
#           coral 은 마지막 성공 응답 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 640
d = Seq(W, H, "ISTIO IN ACTION · 06-01 §5",
        "원 요청과 두 번의 재시도, 그 사이의 백오프",
        "attempts: 2 는 최대 세 번 전달을 뜻한다. 원 요청이 503 을 받으면 25ms 를 기다려 첫 재시도를, 다시 50ms 를 기다려 두 번째 재시도를 보낸다. "
        "마지막이 200 이면 호출자에게는 실패가 보이지 않는다.",
        "백오프는 (25ms × 시도 번호)이고 이 대기도 전체 타임아웃을 함께 갉아먹습니다")

LX = d.lanes([("simple-web 사이드카", "Istio proxy"), ("simple-backend", "75% 가 503")], y0=104, lane_w=230)
XA, XB = LX["simple-web 사이드카"], LX["simple-backend"]
d.rails(560)

def call(label, y, sub=None, c=MUTED):
    d.path(f"M {XA + 10} {y} L {XB - 12} {y}", c, 1.5, m="ar")
    d.t((XA + XB) / 2, y - 8, label, 12, c, KR)
    if sub: d.t((XA + XB) / 2, y + 16, sub, 11, SOFT, MONO)

def back(label, y, c=WARN, mk="ar"):
    d.path(f"M {XB - 10} {y} L {XA + 12} {y}", c, 1.4, m=mk, dash="4 3")
    d.t((XA + XB) / 2, y - 8, label, 12, c, MONO)

def wait(txt, y):
    d.path(f"M {XA + 10} {y - 12} L {XA + 64} {y - 12} L {XA + 64} {y + 12} L {XA + 13} {y + 12}", SOFT, 1.4, m="soft")
    d.t(XA + 74, y + 4, txt, 12, SOFT, KR, "start")

call("원 요청", 200, "attempt 1 / 3")
back("503", 240)
wait("백오프 25ms", 288)
call("재시도 1", 340, "attempt 2 / 3")
back("503", 380)
wait("백오프 50ms", 428)
call("재시도 2", 480, "attempt 3 / 3")
d.path(f"M {XB - 10} 520 L {XA + 12} 520", ACC, 1.6, m="acc", dash="4 3")
d.t((XA + XB) / 2, 512, "200", 12, ACC, MONO)
d.t((XA + XB) / 2, 542, "호출자에게는 실패가 안 보인다", 12, ACC, KR)

d.legend(596, [("재시도가 감춘 실패", WARN), ("호출자가 받는 응답", ACC), ("고정된 백오프", SOFT)])
d.save("06-01.retry-backoff.svg")
