# 09-02.graceful-shutdown — 종료 신호가 Shutdown 을 거쳐 main 의 <-done 을 풀기까지
# 타입 스펙: type-sequence
# 본문 요구(09-02 §6): os.Interrupt → 종료 고루틴이 srv.Shutdown 호출 → ListenAndServe 가 곧바로 ErrServerClosed 반환(main 은 <-done 에서 대기)
#           → Shutdown 이 처리 중 요청을 마치고 반환 → close(done) → main 이 풀려 return.
# 사실 출처: NPG Listing 9-20 코드(txt 1749~1796줄), net/http Server.Shutdown 공식 문서,
#           go1.25.1 에서 2초짜리 핸들러로 직접 돌린 결과(2026-11-06): <-done 이 있으면 curl 200, 없으면 main 이 즉시 끝나 curl exit 52.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 580
d = D(W, H, "SEQUENCE · 09-02 §6",
      "종료 신호를 받아도 main 은 done 이 닫힐 때까지 기다립니다",
      "Ctrl+C 가 오면 종료 고루틴이 srv.Shutdown 을 부른다. ListenAndServe 는 그 즉시 ErrServerClosed 를 돌려주지만 "
      "main 은 <-done 에서 기다리고, Shutdown 이 처리 중 요청을 마치고 돌아오면 고루틴이 close(done) 으로 main 을 풀어 준다.",
      lead="ListenAndServe 가 먼저 돌아와도 main 은 done 을 기다립니다.")

y0 = 104
lane_w = 170
LX = {"sig": 130, "gor": 360, "srv": 590, "main": 820}
roles = [
    ("sig", "OS 신호", "Ctrl+C · os.Interrupt"),
    ("gor", "종료 고루틴", "signal.Notify 로 대기"),
    ("srv", "http.Server", "srv"),
    ("main", "main 고루틴", "ListenAndServe 를 부른 쪽"),
]
for key, name, sub in roles:
    x = LX[key]
    d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    d.t(x, y0 + 19, name, 12, INK, KR, "middle", 600)
    d.t(x, y0 + 35, sub, 11, MUTED, KR, "middle")

lane_top = y0 + 44
y_bot = 500
for x in LX.values():
    d.line(x, lane_top + 6, x, y_bot, RULE, 1.0, "3 6")


def msg(k1, k2, y, label, col, mk="ar", dash=None, sub=None):
    x1, x2 = LX[k1], LX[k2]
    d.arrow([(x1, y), (x2, y)], col, mk, 1.4, dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y - 8, label, 11, col, MONO if any(c.isascii() and c.isalpha() for c in label) else KR, "middle", 600)
    if sub:
        d.t(mx, y + 16, sub, 11, MUTED, KR, "middle")


def note(k, y, label, col, left=False):
    x = LX[k]
    if left:
        d.t(x - 14, y, label, 11, col, KR, "end", 600)
    else:
        d.t(x + 14, y, label, 11, col, KR, "start", 600)


msg("sig", "gor", 196, "c <- os.Interrupt", MUTED, "ar")
msg("gor", "srv", 244, "srv.Shutdown(ctx)", INFO, "ar", sub="리스너를 닫고 처리 중 요청을 기다림")
msg("srv", "main", 306, "ErrServerClosed", WARN, "warn", dash="3 3", sub="ListenAndServe 가 곧바로 반환")
note("main", 346, "err = nil 로 바꾸고 <-done 에서 대기", WARN, left=True)
note("srv", 372, "처리 중이던 요청이 끝날 때까지 블록", MUTED, left=True)
msg("srv", "gor", 420, "Shutdown 반환", OK, "ok", dash="3 3")
msg("gor", "main", 468, "close(done)", OK, "ok")
note("main", 492, "<-done 이 풀리고 return nil", OK, left=True)

d.legend(H - 44, [("종료 요청", INFO), ("먼저 돌아온 반환값", WARN), ("종료 완료", OK)])
d.save(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "09-02.graceful-shutdown.svg")))
print("ok 09-02 graceful-shutdown")
