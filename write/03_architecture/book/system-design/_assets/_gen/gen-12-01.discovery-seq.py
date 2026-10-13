# 타입 스펙: type-sequence — 사용자 A 가 로그인해 인증을 마치고, 서비스 탐색이 채팅 서버 2 를 골라 알려 주면 그 서버에 웹소켓으로 붙는 다섯 레인 흐름.
# 사실 출처: 추출본 v2.txt 3386~3400행(서비스 탐색 4 단계: 로그인 → 로드 밸런서 → API 서버 → 서비스 탐색이 서버 2 선택 → 웹소켓)·PDF 190쪽 그림 12-11.
#   ZooKeeper 가 서버 목록을 쥐는 방식은 https://zookeeper.apache.org/doc/r3.9.6/zookeeperProgrammers.html (Ephemeral Nodes). 서버 2 선택은 그림의 예시 값이다.
#   레인 5 개, 메시지 6 개(스펙 한도 이내).
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


W, H = 1000, 596
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 12-01 §6",
          "로그인 뒤 서비스 탐색이 채팅 서버 2 를 골라 사용자 A 에게 알린다",
          "인증은 API 서버가, 서버 선택은 서비스 탐색이 맡고, 연결은 사용자 A 가 직접 건다.",
          "채팅 서버 1 … N 중 2 가 뽑힌다")

d.lanes([("사용자 A", "앱"), ("로드 밸런서", "경로 분기"), ("API 서버", "인증"), ("서비스 탐색", "ZooKeeper"), ("채팅 서버 2", "웹소켓")],
        (100, 300, 500, 700, 900))
d.rails(520)

d.msg("사용자 A", "로드 밸런서", "1 · 로그인", 212, MUTED)
d.msg("로드 밸런서", "API 서버", "2 · 로그인 요청", 264, MUTED)
d.msg("API 서버", "서비스 탐색", "3 · 서버 찾기", 316, INFO, sub="인증 뒤")
d.msg("서비스 탐색", "API 서버", "채팅 서버 2", 380, OK, dash="5 4")
d.msg("API 서버", "사용자 A", "서버 정보 · 채팅 서버 2", 432, OK, dash="5 4", dx=100)
d.msg("사용자 A", "채팅 서버 2", "4 · ws 연결", 488, ACC, dx=-100)

d.legend(H - 40, [("요청", MUTED), ("서버 선택", INFO), ("선택 결과", OK), ("연결", ACC)])
d.save("12-01.discovery-seq.svg")
