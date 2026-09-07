# 타입 스펙: type-sequence — 사용자와 게이트웨이와 외부 호스트가 시간 축을 따라 두 연결을 잇는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.9.1 Figure 8.35 (책 619~620쪽) —
#   필터 설정, 인증, 두 연결의 중계, 단점 셋은 원문 그대로.
#   원문이 첫 단계를 Telnet 이라 적은 것은 오기이며 본문에 정오로 병기했다. 여기서는 SSH 로 그린다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO


def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, kr(sub))


W, H = 1000, 632
d = SeqKR(W, H, "SECTION 8.9.1 · APPLICATION GATEWAY",
          "게이트웨이가 두 연결을 이어 붙입니다",
          "사용자 신원은 헤더에 없고 응용 데이터에 있다. 그래서 응용을 이해하는 서버가 사이에 선다.",
          "필터 설정과 중계 절차는 원문 Figure 8.35 의 것입니다")
d.lanes([("내부 사용자", "client"), ("응용 게이트웨이", "SSH 서버이자 클라이언트"), ("외부 호스트", "server")],
        y0=118, lane_w=248)
d.rails(408)

d.msg("내부 사용자", "응용 게이트웨이", "SSH 세션", 190, INFO)
d.msg("응용 게이트웨이", "내부 사용자", "ID · 비밀번호 요구", 232, INFO)
d.msg("내부 사용자", "응용 게이트웨이", "자격 제출", 274, INFO)
d.state("응용 게이트웨이", "권한 확인", 306, ACC)
d.msg("응용 게이트웨이", "외부 호스트", "SSH 세션", 348, OK, sub="게이트웨이가 시작하므로 필터가 허용합니다")
d.msg("응용 게이트웨이", "내부 사용자", "양쪽을 중계", 408, ACC, dash="5 4")

NY = 436
d.box(24, NY, 470, 100, PAPER2, RULE, 1.0)
d.t(44, NY + 28, "필터가 함께 하는 일", 12, INK, KR, "start", 600)
d.t(44, NY + 54, "게이트웨이의 IP 에서 출발한 것 말고는", 11, MUTED, KR, "start")
d.t(44, NY + 76, "모든 SSH 연결을 막습니다. 그래서 우회가 없습니다.", 11, MUTED, KR, "start")

d.tone(514, NY, 462, 100, BAD, 8, "12", 1.3)
d.t(534, NY + 28, "치르는 값 셋", 12, BAD, KR, "start", 600)
d.t(534, NY + 52, "응용마다 다른 게이트웨이 · 모든 데이터가 거치는 성능 대가", 11, MUTED, KR, "start")
d.t(534, NY + 74, "클라이언트가 게이트웨이를 알아야 함", 11, MUTED, KR, "start")

d.legend(556, [("인증 구간", INFO), ("바깥으로 나가는 연결", OK), ("판정과 중계", ACC), ("대가", BAD)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-05.application-gateway.svg"
d.save(out); print("→", out.name)
