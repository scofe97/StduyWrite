# 타입 스펙: type-sequence — 사용자 A 의 메시지가 채팅 서버 1 에서 ID(901)를 받고 큐에 올라 저장된 뒤, 접속 중인 사용자 B 에게는 채팅 서버 2 를 거쳐 닿고 오프라인이면 푸시로 가는 다섯 레인 흐름.
# 사실 출처: 추출본 v2.txt 3405~3419행(1:1 흐름 6 단계: 서버 1 → ID 생성기 → 메시지 동기화 큐 → 키-값 저장소 → 5.a 온라인이면 서버 2 / 5.b 오프라인이면 PN 서버 → 사용자 B)·PDF 191쪽 그림 12-12.
#   설명용 예시(그림·추출본에 없는 값): 메시지 ID 901. ID 생성기와 키-값 저장소는 레인 대신 자체 호출로 접어 레인 5 개 한도를 지켰다. 메시지 5 개.
# Layout conventions: 레인 폭 160, x = 100·300·500·700·900, 메시지 stride 52. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=160):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13 if _kr(label) == KR else 12, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 14, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub), "start")


W, H = 1000, 640
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 12-01 §7",
          "메시지 901 은 ID 를 받고 큐를 지난 뒤 저장되고 전달된다",
          "채팅 서버 1 이 ID 를 받아 큐에 올리면 저장과 전달이 갈리고, 사용자 B 가 오프라인이면 푸시로 간다.",
          "사용자 A 가 사용자 B 에게 보낸 메시지")

d.lanes([("사용자 A", "보내는 쪽"), ("채팅 서버 1", "웹소켓"), ("메시지 큐", "동기화 큐"), ("채팅 서버 2", "웹소켓"), ("사용자 B", "받는 쪽")],
        (100, 300, 500, 700, 900))
d.rails(528)

d.msg("사용자 A", "채팅 서버 1", "1 · 메시지", 212, MUTED, sub="to B")
d.selfmsg("채팅 서버 1", "2 · ID 901", 276, INFO, sub="ID 생성기")
d.msg("채팅 서버 1", "메시지 큐", "3 · 901 적재", 340, MUTED)
d.selfmsg("메시지 큐", "4 · 저장", 392, INFO, sub="키-값 저장소")
d.msg("메시지 큐", "채팅 서버 2", "5.a · 온라인", 456, OK)
d.msg("채팅 서버 2", "사용자 B", "6 · 전달", 504, ACC)
d.tone(380, 536, 240, 40, WARN, 4, "22", 1.1)
d.t(500, 561, "5.b 오프라인이면 PN 서버가 푸시", 13, WARN, KR, "middle")

d.legend(H - 40, [("요청", MUTED), ("다른 구성 요소 호출", INFO), ("온라인 전달", OK), ("오프라인", WARN), ("도착", ACC)])
d.save("12-01.message-flow-seq.svg")
