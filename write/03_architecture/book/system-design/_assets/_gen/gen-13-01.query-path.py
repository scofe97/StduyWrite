# 타입 스펙: type-sequence — 브라우저·로드 밸런서·API 서버·Trie 캐시·Trie DB 다섯 레인에서 첫 요청이 캐시 미스로 DB 까지 갔다가 돌아오고, 응답 헤더가 브라우저 캐시를 정한다.
# 사실 출처: 추출본 v2.txt 3762~3790행(질의 서비스 · 로드 밸런서 → API 서버 → Trie 캐시 · 캐시에 없으면 채워 넣는다 · 미스 원인은 캐시 서버 메모리 부족이나 중단) · PDF 214쪽 그림 13-11, 응답 헤더 캡처 215쪽.
#   브라우저 캐시: 같은 URL 요청은 응답의 Cache-Control 로 보관된다(RFC 9111 §5.2.2.1 max-age, §5.2.2.7 private). 값 private, max-age=3600 은 설계 예시다.
#   요청 URL 모양 search?q=tw 와 응답 목록 값 twitter 35 · twitch 29 는 설명용 예시다(표 13-1 의 빈도).
# Layout conventions: 레인 폭 150, 메시지 stride 44(y=196 부터). Seq 계열이 라벨을 mono 로 고정하므로 한글 라벨은 서브클래스에서 KR 로 바꾼다. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, MUTED, INK, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y + 4, label, 13, c, _kr(label), "start")


W, H = 1000, 668
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §6",
          "처음 친 접두사는 DB 까지 가고 응답 헤더가 다음 요청을 브라우저에서 끝낸다",
          "Trie 캐시에 없으면 DB 에서 채워 돌려주고, 응답의 max-age 동안 같은 접두사 요청은 네트워크를 타지 않는다.",
          "예시 접두사 tw · 응답 Cache-Control: private, max-age=3600")
LX = d.lanes([("브라우저", "fetch()"), ("로드 밸런서", "LB"), ("API 서버", "HTTP"),
              ("Trie 캐시", "prefix → top 5"), ("Trie DB", "key → value")], 104, 150)
d.rails(H - 96)

y = 196
d.msg("브라우저", "로드 밸런서", "GET search?q=tw", y, MUTED); y += 44
d.msg("로드 밸런서", "API 서버", "GET search?q=tw", y, MUTED); y += 44
d.msg("API 서버", "Trie 캐시", "get tw", y, MUTED); y += 44
d.msg("Trie 캐시", "Trie DB", "get tw (miss)", y, WARN, dash="5 4"); y += 44
d.msg("Trie DB", "Trie 캐시", "twitter 35 · twitch 29 …", y, OK); y += 44
d.msg("Trie 캐시", "API 서버", "top 5", y, OK); y += 44
d.msg("API 서버", "로드 밸런서", "응답 · max-age=3600", y, ACC); y += 44
d.msg("로드 밸런서", "브라우저", "응답 · max-age=3600", y, ACC); y += 52
d.selfmsg("브라우저", "3600 초 안 캐시 응답", y, ACC)

d.legend(H - 56, [("요청", MUTED), ("캐시 미스", WARN), ("응답", OK), ("브라우저 캐시를 정하는 헤더", ACC)])
d.save("13-01.query-path.svg")
