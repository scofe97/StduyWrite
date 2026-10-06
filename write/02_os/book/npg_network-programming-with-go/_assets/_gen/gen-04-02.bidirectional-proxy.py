# 타입 스펙: type-sequence
# 04-02 양방향 프록시 구조와 half-close 흐름 (io.Copy 및 CloseWrite 보강)
# 사실 출처: NPG Ch.4 Listing 4-14~4-18, pkg.go.dev/net (CloseWrite 보강)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 540
d = D(W, H, "LISTING 4-14 PROXY HALF-CLOSE",
      "양방향 프록시와 half-close",
      "io.Copy 양방향 중계와 CloseWrite 를 통한 단방향 FIN 전달",
      "EOF 감지와 CloseWrite 단방향 종료 전달")

# 참여자 레인
lanes = [
    (160, "Client", "클라이언트"),
    (440, "Proxy", "Go 프록시"),
    (720, "Server", "업스트림 서버"),
]

y_top = 104
y_bot = 480

for lx, eng, kr in lanes:
    d.box(lx - 70, y_top, 140, 44, fill=PAPER2, stroke=RULE)
    d.t(lx, y_top + 20, eng, 12, INK, MONO, "middle", 600)
    d.t(lx, y_top + 36, kr, 11, MUTED, KR, "middle")
    # 레일
    d.line(lx, y_top + 44, lx, y_bot, RULE, 1.0, "3 5")

def msg(x1, x2, y, label, col, mk="ar"):
    d.arrow([(x1, y), (x2, y)], col, mk, 1.4)
    d.t((x1 + x2) / 2, y - 8, label, 11, col, KR, "middle", 600)

def self_action(x, y, label, col, mk="ar"):
    d.path(f"M {x} {y - 8} L {x + 40} {y - 8} L {x + 40} {y + 8} L {x} {y + 8}", col, 1.3, m=mk)
    d.t(x + 50, y + 4, label, 11, col, KR, "start", 600)

# 1. 클라이언트 요청 전송
msg(160, 440, 175, "요청 데이터 전송", OK, "ok")

# 2. 프록시 요청 중계
msg(440, 720, 210, "io.Copy 요청 중계", OK, "ok")

# 3. 클라이언트 FIN (EOF)
msg(160, 440, 250, "FIN 세그먼트 (EOF)", ACC, "acc")

# 4. 프록시 CloseWrite() (보강)
self_action(440, 288, "CloseWrite() 호출", ACC, "acc")

# 5. 프록시 FIN 전달 (업스트림 쓰기 종료)
msg(440, 720, 328, "FIN 단방향 전달", ACC, "acc")

# 6. 서버 잔여 응답 전송 (하프 클로즈 상태 유지)
msg(720, 440, 368, "잔여 응답 수신", OK, "ok")

# 7. 프록시 응답 중계
msg(440, 160, 404, "io.Copy 응답 중계", OK, "ok")

# 8. 서버 FIN (EOF)
msg(720, 440, 442, "서버 FIN (EOF)", BAD, "bad")

# 9. 소켓 완전 종료
self_action(440, 474, "소켓 완전 Close()", BAD, "bad")

d.legend(H - 46, [("데이터 전달", OK), ("단방향 종료 (보강)", ACC), ("완전 종료", BAD)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-02.bidirectional-proxy.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
