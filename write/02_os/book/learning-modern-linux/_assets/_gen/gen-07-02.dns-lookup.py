# 07-02 §7 — 이름 하나를 주소로 바꾸는 여정과 그 길목마다의 TTL.
# 원문("DNS Lookups"): dig 헤더가 ";; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 2,
#       ADDITIONAL: 5" 이고 ANSWER 의 A 레코드가 "mhausenblas.info. 1799 IN A 185.199.111.153",
#       AUTHORITY 가 "mhausenblas.info. 1800 IN NS dns1.registrar-servers.com.".
#   Resolvers: "Programs that extract information from name servers in response to client requests.
#       They are machine local, and no explicit protocol is defined for the interaction between a
#       resolver and a client."
#   "In the query process, the resolver would iteratively query authoritative name servers (NS)
#       starting from the root or, if supported, using a recursive query where an NS queries others
#       on behalf of a resolver."
#   저자의 격언 — "It's always DNS." 이유는 캐시가 여러 층에 있기 때문.
# 노트의 읽기: 앞 회차의 이 도식은 루트와 TLD 를 "루트에서부터 반복 질의" 한 줄로 뭉쳐 두었다.
#       2026-09-06 학습 세션에서 학습자가 "정작 필요한 건 조회하고 응답하는 흐름"이라고 지적해
#       그 축약을 편다. 리졸버가 루트 → TLD → 권한 세 번을 각각 묻는다는 것이 이 그림의 논지다.
#       TTL 은 §7 의 새 절이 다루는 축이라 걸음마다 어디에 붙는지를 함께 적는다.
#       수치는 원서 출력에 있는 것만 쓴다 — 1799 는 책에 있고, 위임 NS 의 TTL 값은 책에 없어
#       숫자를 적지 않고 "여기에도 TTL 이 붙는다"까지만 말한다.
# 타입 스펙: type-sequence — 시간축 위의 주고받음. 참여자 5(상한 5), 메시지 9(상한 12),
#       프래그먼트 0. 반환 메시지는 점선 + 채운 마커. coral 은 하나뿐이며 캐시가 끼어드는 자리다.
#       라벨이 남의 레인 위에 앉지 않도록, 레인을 가로지르는 메시지는 화살표만 msg 로 그리고
#       라벨은 빈 구간에 따로 놓는다(type-sequence 안티패턴 "Labels sitting over another lifeline").
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 800
d = Seq(W, H, "LEARNING MODERN LINUX · 07-02 §7",
        "이름 하나가 주소가 되기까지 세 번을 묻는다",
        "리졸버는 루트에게 .info 를 누가 아는지 묻고, 그 답을 들고 TLD 에게 다시 묻고, "
        "또 그 답을 들고 권한 있는 네임서버에 묻습니다. 걸음마다 답에는 TTL 이 붙습니다.",
        "캐시가 답을 쥐고 있으면 이 여정은 시작도 하지 않습니다")

LANE_W = 140
LX = d.lanes([("앱 · dig", "클라이언트"),
              ("리졸버", "기계에 딸림"),
              ("루트 서버", "13개 · 루트 존"),
              ("TLD 서버", ".info 존"),
              ("권한 있는 NS", "dns1.registrar")], y0=104, lane_w=LANE_W)

APP, RES, ROOT, TLD, AUTH = ("앱 · dig", "리졸버", "루트 서버", "TLD 서버", "권한 있는 NS")
GAP_RT = (LX[ROOT] + LX[TLD]) / 2      # 루트–TLD 사이 빈 구간
GAP_TA = (LX[TLD] + LX[AUTH]) / 2      # TLD–권한 사이 빈 구간


def crossing(a, b, label, sub, y, c, lx, mk="ar", dash=None):
    """레인을 가로지르는 메시지 — 화살표만 그리고 라벨은 빈 구간 lx 에 둔다.

    d.msg 는 라벨을 두 레인의 중점에 두는데, 그 중점이 가로지르는 레인 위라 라벨이
    남의 lifeline 에 앉는다. 그래서 화살표 경로만 d.msg 와 같은 식으로 직접 긋는다.
    """
    x1, x2 = LX[a], LX[b]
    step = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * step} {y} L {x2 - 12 * step} {y}", c, 1.5, m=mk, dash=dash)
    d.t(lx, y - 9, label, 11, c, MONO, "middle", 600)
    if sub:
        d.t(lx, y + 16, sub, 11, MUTED)


# ── 1. 앱이 리졸버에게 ──────────────────────────────────────────────
d.msg(APP, RES, "mhausenblas.info. A", 196, INFO,
      sub="정해진 프로토콜이 없다")

# ── 2. 캐시 — 여정이 시작되지 않는 유일한 길 (coral 하나) ───────────
d.selfmsg(RES, "캐시 확인", 246, ACC, sub="TTL 남았으면 끝")

# ── 3~4. 루트에게 ──────────────────────────────────────────────────
d.msg(RES, ROOT, ".info 는 누가 아나", 306, SOFT)
d.msg(ROOT, RES, ".info NS 는 저기", 350, OK, mk="ok", dash="5 4",
      sub="이 답에도 TTL 이 붙는다")

# ── 5~6. TLD 에게 (리졸버→TLD 는 루트 레인을 가로지른다) ────────────
crossing(RES, TLD, "mhausenblas.info 는", None, 410, SOFT, GAP_RT)
crossing(TLD, RES, "권한 NS 는 저기", "위임의 연쇄", 454, OK, GAP_RT,
         mk="ok", dash="5 4")

# ── 7~8. 권한 있는 네임서버에게 ────────────────────────────────────
crossing(RES, AUTH, "A 레코드를 주십시오", None, 514, SOFT, GAP_TA)
crossing(AUTH, RES, "185.199.110.153", "TTL 1799", 558, OK, GAP_TA,
         mk="ok", dash="5 4")

# ── 9. 앱에게 ──────────────────────────────────────────────────────
d.msg(RES, APP, "NOERROR · ANSWER 4", 618, INFO, mk="info", dash="5 4",
      sub="네 절로 나뉜 답")

d.rails(650)

d.tone(24, 668, W - 48, 74, ACC)
d.t(44, 694, "언제나 DNS 탓이라는 말의 뜻", 13, INK, KR, "start", 600)
d.t(44, 716, "이 여정의 어느 걸음에도 캐시가 앉을 수 있습니다. 앱 안의 로컬 캐시부터 리졸버까지, "
             "나와 네임서버 사이의 모든 것이 그렇습니다.", 12, MUTED, KR, "start")
d.t(44, 734, "권한 NS 가 준 1799 는 초입니다. 무엇을 고쳐도 그만큼은 옛 답이 돌아옵니다.", 12, MUTED, KR, "start")

d.legend(752, [("사람과 응답", INFO), ("리졸버가 묻는다", SOFT),
               ("서버가 답한다", OK), ("여정이 멈추는 자리", ACC)])
d.save("07-02.dns-lookup.svg")
print("ok 07-02.dns-lookup")
