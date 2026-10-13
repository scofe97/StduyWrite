# 타입 스펙: type-sequence — 사용자 A 의 미스가 원 서버를 거쳐 TTL 캐시가 되고, 사용자 B 는 TTL 안에서 적중하며, TTL 이 지난 뒤에는 CDN 이 원 서버에 확인한다.
# 사실 출처: 추출본 v2.txt 299~311행(미스 → 원 서버 → TTL 헤더 → 캐시 → B 적중), RFC 9111 §5.1 Age(초 단위)·§5.2.2.1 max-age,
#   CloudFront 개발자 안내서 Expiration(기본 TTL 24시간 = 86400초, 만료 뒤 원 서버 확인에 304 Not Modified 또는 200 OK) —
#   https://www.rfc-editor.org/rfc/rfc9111 · https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html .
#   max-age=86400 과 Age: 3600(B 가 한 시간 뒤에 요청)은 설계 가정이며 경로 /image.png 는 이미지 하나의 예시 이름이다.
# Layout conventions: 레인 3개 폭 210, 메시지 stride 44~56, 상태 칩은 CDN 레인 옆. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 13 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13 if _kr(label) == KR else 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13 if _kr(sub) == KR else 12, MUTED, _kr(sub))


W, H = 960, 904
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 01-02 §2",
          "CDN 은 TTL 동안 원 서버 대신 답한다",
          "A 의 미스가 이미지를 86400초 캐시로 만들고, B 는 3600초 뒤에도 원 서버 없이 받는다.",
          "응답 헤더 max-age 가 TTL 이고 Age 는 원 서버가 만든 뒤 흐른 초")

d.lanes([("사용자", "A 와 B"),
         ("CDN 서버", "정적 파일 캐시"),
         ("원 서버", "웹 서버 · 저장소")])
d.rails(852)

d.t(12, 188, "A · 미스", 13, SOFT, KR, "start", 600)
d.msg("사용자", "CDN 서버", "GET /image.png", 216, MUTED, sub="사용자 A")
d.state("CDN 서버", "MISS", 248, WARN)
d.msg("CDN 서버", "원 서버", "GET /image.png", 292, MUTED)
d.msg("원 서버", "CDN 서버", "200 · max-age=86400", 340, INFO, dash="5 4", sub="TTL 헤더를 단 응답")
d.state("CDN 서버", "TTL 86400s", 380, OK)
d.msg("CDN 서버", "사용자", "200", 424, MUTED, dash="5 4", sub="A 에게")

d.line(12, 460, W - 48, 460, RULE, 0.8, "3 6")
d.t(12, 480, "B · TTL 안", 13, SOFT, KR, "start", 600)
d.msg("사용자", "CDN 서버", "GET /image.png", 508, MUTED, sub="사용자 B · 3600초 뒤")
d.state("CDN 서버", "HIT", 540, OK)
d.msg("CDN 서버", "사용자", "200 · Age: 3600", 576, ACC, dash="5 4", sub="원 서버 호출 없음")

d.line(12, 612, W - 48, 612, RULE, 0.8, "3 6")
d.t(12, 632, "TTL 만료", 13, SOFT, KR, "start", 600)
d.msg("사용자", "CDN 서버", "GET /image.png", 664, MUTED, sub="86400초 뒤")
d.msg("CDN 서버", "원 서버", "조건부 요청", 724, WARN)
d.msg("원 서버", "CDN 서버", "304 Not Modified", 772, INFO, dash="5 4", sub="바뀐 것 없음")
d.msg("CDN 서버", "사용자", "200", 824, MUTED, dash="5 4", sub="저장된 파일")

d.legend(H - 40, [("미스·만료", WARN), ("원 서버 쪽", INFO), ("캐시에 저장", OK), ("적중 응답", ACC)])
d.save("01-02.cdn-ttl-seq.svg")
