# 타입 스펙: type-sequence — 링크 하나가 끊어졌을 때 컨트롤러 안팎에서 벌어지는 여섯 단계.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.5.3 Figure 5.16 의 1~6 단계
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, KR, MONO

W, H = 1000, 700
d = Seq(W, H, "SECTION 5.5.3 · LINK-STATE CHANGE",
        "링크 하나가 끊어지면 여섯 걸음",
        "s1 과 s2 사이 링크가 끊어졌을 때 SDN 제어 평면이 밟는 순서. 다익스트라는 스위치 밖의 앱에서 돌고, 스위치는 서로가 아니라 컨트롤러에게만 알린다.",
        "앞 편에서는 라우터끼리 알렸습니다 — 여기서는 컨트롤러에게만 알립니다")

LX = d.lanes([("s1", "패킷 스위치"), ("링크 상태 관리자", "컨트롤러 안"),
              ("라우팅 앱", "다익스트라"), ("흐름 표 관리자", "컨트롤러 안")], y0=110, lane_w=196)
d.rails(506)

d.msg("s1", "링크 상태 관리자", "port-status", 180, BAD, "bad", sub="1 · s2 로 가는 링크가 끊겼습니다")
d.selfmsg("링크 상태 관리자", "DB 갱신", 248, INFO, sub="2 · 링크 상태 DB 를 고칩니다")
d.msg("링크 상태 관리자", "라우팅 앱", "알림", 314, INFO, "info", sub="3 · 미리 등록해 둔 앱에게")
d.msg("라우팅 앱", "링크 상태 관리자", "상태 조회", 374, MUTED, "ar", sub="4 · 새 최소 비용 경로를 계산합니다")
d.msg("라우팅 앱", "흐름 표 관리자", "새 경로", 434, ACC, "acc", sub="5 · 고칠 표를 정합니다")
d.msg("흐름 표 관리자", "s1", "modify-state", 490, ACC, "acc", sub="6 · s1 · s2 · s4 의 표를 고칩니다")

d.t(30, 548, "s4 는 끊어진 링크에 닿아 있지도 않은데 표가 바뀝니다. s1 이 s4 를 거쳐 보내게 되므로 s2 는 이제 s4 에서 받고,", 12, MUTED, KR, "start")
d.t(30, 568, "s4 는 s1 이 s2 로 보내는 패킷을 나르게 됩니다. 한 곳에서 계산하니 세 스위치가 한꺼번에 맞춰집니다.", 12, MUTED, KR, "start")
d.t(30, 596, "앞 편의 라우터별 제어에서는 이 조율을 프로토콜이 시간을 들여 수렴시켜야 했습니다.", 11, ACC, KR, "start")

d.legend(618, [("장애 보고", BAD), ("컨트롤러 내부", INFO), ("표를 고치는 길", ACC)])
d.t(960, 672, "KUROSE-ROSS 9E FIG 5.16", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.link-failure.svg"
d.save(out)
print("→", out)
