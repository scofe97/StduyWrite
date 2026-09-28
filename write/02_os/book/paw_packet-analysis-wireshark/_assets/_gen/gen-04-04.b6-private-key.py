# 04-04 B6 — 같은 서버 개인키(a.test.key)를 두 캡처에 물렸을 때 갈리는 결과. follow,tls 출력의 실측값만 쓴다.
# 타입 스펙: type-flowchart — 캡처의 키 교환 방식으로 갈리는 판단. focal 은 개인키로도 비는 ECDHE 쪽 끝.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import W, EYEBROW, Flow, ACC, OK, MUTED, INK, KR
H = 520
d = Flow(W, H, EYEBROW + "B6", "B6 · 서버 개인키가 여는 것",
         "uat:rsa_keys 로 a.test.key 를 물려 두 캡처를 연다. 정적 RSA 캡처는 잠긴 비밀 값을 풀어 요청과 응답이 평문으로 나오고, ECDHE 캡처는 풀 대상이 없어 스트림이 빈다.",
         "키가 틀린 것이 아니라 그 키로 풀 대상이 캡처에 없습니다")
CX, RX = 300, 700
d.oval(CX, 96, 280, 40, "a.test.key 물림 · uat:rsa_keys")
d.arrow([(CX, 136), (CX, 164)], MUTED, "ar", 1.4)
d.diamond(CX, 168, 124, 40, "캡처의 키 교환")
# 오른쪽 — 정적 RSA
d.arrow([(CX + 124, 208), (RX - 144, 208)], MUTED, "ar", 1.4)
d.t(CX + 136, 196, "정적 RSA · B5", 11, MUTED, KR, "start", 600)
d.step(RX, 172, 280, 72, "잠긴 비밀 값을 풂", "ClientKeyExchange 262 바이트 안")
d.arrow([(RX, 244), (RX, 380)], MUTED, "ar", 1.4)
d.oval(RX, 384, 280, 40, "GET / HTTP/1.1 · 200 ok", OK)
# 아래 — ECDHE
d.arrow([(CX, 248), (CX, 276)], MUTED, "ar", 1.4)
d.t(CX + 12, 268, "ECDHE · A1", 11, MUTED, KR, "start", 600)
d.step(CX, 280, 280, 72, "개인키는 서명에만", "세션 키 계산에 관여 안 함")
d.arrow([(CX, 352), (CX, 380)], MUTED, "ar", 1.4)
d.oval(CX, 384, 280, 40, "Node 0: :0 · 빈 스트림", focal=True)
d.legend(H - 56, [("개인키로도 열리지 않는 연결", ACC), ("열린 연결", OK)])
d.save("04-04.b6-private-key.svg")
