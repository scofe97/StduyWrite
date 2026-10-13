# 타입 스펙: type-sequence — 미들웨어가 쓴 세션의 읽기를 복제본으로 보냈다가 1초 안에 적용되지 않아 주 DB 로 돌려보내는 왕복.
# 사실 출처: MySQL Router 8.4 문서 3.5.1 Configuration(access_mode=auto 면 읽기는 read_only 로, 쓰기는 read_write 로. wait_for_my_writes 가 1 이면 읽기 쿼리가 그 세션의 마지막 쓴 트랜잭션을 기다림. wait_for_my_writes_timeout 기본 1초, 넘으면 read_write 대상으로 폴백) https://dev.mysql.com/doc/mysql-router/8.4/en/router-read-write-splitting-configuration.html. 추출본 v1.txt 2549~2606행(미들웨어가 쓰기는 주 DB 로, 읽기는 복제본으로 라우팅).
# Layout conventions: 레인 4·폭 180, 단일 화살표 stride 52, 첫 화살표 y=200. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


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
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        lo, hi = sorted((x1, x2))
        mids = [x for x in s.LX.values() if lo + 40 < x < hi - 40]
        if mids:
            # 중간 레인 레일이 라벨을 가르지 않게 출발 쪽 구간의 가운데에 단다
            near = min(mids, key=lambda x: abs(x - x1))
            lx = (x1 + near) / 2
        else:
            lx = (x1 + x2) / 2
        s.t(lx, y - 9, label, 12, c, _kr(label), "middle", 600)

    def state(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 960, 640
d = SeqKR(W, H, "BYTEBYTEGO · 01-02 §4",
          "쓴 세션의 읽기는 복제본을 기다리다 1초 뒤 주 DB 로 간다",
          "복제본이 그 쓰기를 적용하지 못하면 미들웨어가 같은 읽기를 read_write 대상으로 다시 보냅니다",
          "access_mode=auto · wait_for_my_writes=1 · wait_for_my_writes_timeout=1")
CL, RT, PR, RP = "클라이언트", "MySQL Router", "주 DB", "복제본"
d.lanes([(CL, "한 세션"), (RT, "읽기·쓰기 분할"), (PR, "read_write"), (RP, "read_only")], 100, 180)
d.rails(H - 80)

Y0, S = 200, 52
d.msg(CL, RT, "INSERT", Y0, MUTED, "ar")
d.msg(RT, PR, "INSERT", Y0 + S, MUTED, "ar")
d.msg(CL, RT, "SELECT", Y0 + 2 * S, MUTED, "ar")
d.msg(RT, RP, "SELECT", Y0 + 3 * S, ACC, "acc")
d.state(RT, "1초 대기", Y0 + 3 * S + 28, WARN, dx=0)
d.state(RP, "쓰기 미적용", Y0 + 3 * S + 28, BAD, dx=0)
d.msg(RT, PR, "SELECT · 폴백", Y0 + 4 * S + 28, ACC, "acc")
d.msg(PR, RT, "1 row", Y0 + 5 * S + 28, OK, "ok", dash="5 4")
d.msg(RT, CL, "1 row", Y0 + 6 * S + 28, OK, "ok", dash="5 4")

d.legend(H - 56, [("복제본을 기다림 · 폴백", ACC), ("대기 시간 초과", WARN), ("미적용", BAD), ("응답", OK)])
d.save("01-02.router-sequence.svg")
