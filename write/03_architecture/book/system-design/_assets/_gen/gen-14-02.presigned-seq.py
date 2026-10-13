# 타입 스펙: type-sequence — 클라이언트·API 서버·원본 저장소 세 레인에서 업로드 요청, 사전 서명 URL 응답, URL 로 PUT, 객체 생성이 차례로 오가고, 만료 전에 같은 URL 로 다시 PUT 하면 객체가 교체된다.
# 사실 출처: 흐름은 추출본 v2.txt 4229~4239행(클라이언트가 API 서버에 요청 → 사전 서명 URL 응답 → 그 URL 로 업로드), PDF 239쪽 그림(POST /upload).
#   S3 사전 서명 URL 의 PUT·만료 시간·같은 키 덮어쓰기·만료 전 반복 사용은 Amazon S3 User Guide(https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html, 2026-10-13 확인).
#   객체 키 videos/ab12/original 과 만료 600 s 는 설명을 위해 정한 값이고 funny.mov 300 MB 는 14-01 편의 예시다.
# Layout conventions: 레인 3개 폭 200, x = 136·480·824, 메시지 stride 52~64, 요청 둘 사이 구분선. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=104, lane_w=200):
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


W, H = 960, 596
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 14-02 §6",
          "사전 서명 URL 은 발급 한 번에 업로드 권한을 키 하나로 좁힌다",
          "클라이언트가 POST /upload 로 요청하면 API 서버가 객체 키와 PUT 과 만료를 담은 URL 을 돌려주고, 클라이언트는 그 URL 로 원본 저장소에 올린다. URL 은 만료 전까지 다시 쓸 수 있다.",
          "키 videos/ab12/original · 만료 600 s 는 설명용 값")

d.lanes([("클라이언트", "funny.mov · 300 MB"), ("API 서버", "URL 서명 발급"), ("원본 저장소", "BLOB")],
        (136, 480, 824))
d.rails(536)

d.t(12, 188, "발급과 업로드", 13, SOFT, KR, "start", 600)
d.msg("클라이언트", "API 서버", "POST /upload", 220, MUTED)
d.msg("API 서버", "클라이언트", "사전 서명 URL", 280, INFO, dash="5 4", sub="videos/ab12/original · PUT · 만료 600 s", dx=0)
d.msg("클라이언트", "원본 저장소", "PUT <사전 서명 URL>", 344, ACC, sub="funny.mov 300 MB", dx=170)
d.msg("원본 저장소", "클라이언트", "객체 생성", 400, OK, dash="5 4", dx=-60)

d.line(12, 440, W - 48, 440, RULE, 0.8, "3 6")
d.t(12, 464, "만료 전에 같은 URL", 13, SOFT, KR, "start", 600)
d.msg("클라이언트", "원본 저장소", "PUT <같은 URL>", 496, WARN, dx=90)
d.msg("원본 저장소", "클라이언트", "같은 키의 객체 교체", 532, WARN, dash="5 4", dx=-60)

d.legend(H - 40, [("요청", MUTED), ("URL 발급", INFO), ("업로드", ACC), ("객체 생성", OK), ("만료 전 재사용", WARN)])
d.save("14-02.presigned-seq.svg")
