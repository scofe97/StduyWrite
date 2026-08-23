# 20-01 §켜는 순서 — deny 로 시작하지 않습니다
# 본문이 순서를 못 박는다 — "dryrun 으로 먼저 걸고 감사로 확인한 뒤에 deny 로 올려라".
# 그러니 세 모드를 나란한 카드로 늘어놓으면 안 되고 *올라가는 사다리* 여야 한다.
# 각 칸에 "넣으면 무엇이 돌아오는가" 를 실측 문자열로 붙여, 모드 차이가 설명이 아니라
# 응답으로 보이게 한다(17-01 랩 도식과 같은 형태). 초점은 첫 칸이다 — 여기서 목록을
# 얻지 않고 바로 deny 로 가면 스케일링 순간에 터진다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 620
d = D(W, H, "KUBERNETES UP AND RUNNING · 20-01",
      "막기 전에 세고, 세고 나서 막는다",
      "제약은 CREATE 와 UPDATE 에서만 평가된다. 켜 둔 직후엔 조용하다가 스케일링 순간에 "
      "터지므로, dryrun 으로 목록을 먼저 얻는다.",
      "kind 로컬 클러스터 실측 — 응답은 실제로 받은 문자열 · 감사 주기 기본 60초")

LX, LW = 24, 336
RX, RW = 376, 560
CX, CW = 952, 264
Y0, RH, GAP = 136, 108, 14

d.t(LX, 116, "enforcementAction", 9, SOFT, KR, "start")
d.t(RX, 116, "위반 파드를 넣으면", 9, SOFT, KR, "start")
d.t(CX, 116, "이 칸에서 얻는 것", 9, SOFT, KR, "start")

ROWS = [
    ("01", "dryrun", "만들어지고, 감사가 센다",
     "pod/nginx-noncompliant created\nstatus.totalViolations: 1", OK,
     "고쳐야 할 목록을 얻는다", ACC, True),
    ("02", "warn", "만들어지고, 경고가 돌아온다",
     "Warning: [repo-is-kuar-demo] …<nginx-warn>…\npod/nginx-warn created", WARN,
     "개발자에게 미리 알린다", WARN, False),
    ("03", "deny", "거부되고, 이유가 돌아온다",
     "Error from server (Forbidden): …has an\ninvalid image repo <nginx>", BAD,
     "이제 올려도 안 터진다", BAD, False),
]
for i, (no, mode, what, resp, rc, gain, c, focal) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    if focal:
        d.tone(LX, y, LW, RH, c, 8, "0C", 1.5)
    else:
        d.box(LX, y, LW, RH, PAPER2, RULE, 1.0, 8)
    d.t(LX + 18, y + 32, no, 11, c, MONO, "start", 600)
    d.t(LX + 48, y + 32, mode, 15, c if focal else INK, MONO, "start", 600)
    d.t(LX + 18, y + 62, ddx.fit(what, 10, LW - 36, what), 10, MUTED, KR, "start")
    if i == 0:
        d.t(LX + 18, y + 84, "감사 주기가 지나야 status 에 쌓인다", 9, SOFT, KR, "start")

    d.o.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" rx="8" '
               f'fill="{rc}0C" stroke="{rc}" stroke-width="{1.4 if focal else 1.0}"/>')
    for j, ln in enumerate(resp.split("\n")):
        d.t(RX + 18, y + 40 + j * 22, ddx.fit(ln, 11, RW - 36, ln), 11, rc, MONO, "start")
    d.arrow([(LX + LW + 4, y + RH / 2), (RX - 6, y + RH / 2)], SOFT, "soft", 1.2)

    d.t(CX, y + RH / 2 + 5, ddx.fit(gain, 11, CW, gain), 11, c, KR, "start", 600 if focal else 400)
    if i < len(ROWS) - 1:
        d.arrow([(LX + LW / 2, y + RH + 1), (LX + LW / 2, y + RH + GAP - 1)], SOFT, "soft", 1.2)

BY = Y0 + 3 * (RH + GAP) + 8
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "제약 대상이 Pod 인데 ReplicaSet 을 만들면 오류가 사용자에게 안 온다. "
                 "Pod 를 만들려던 컨트롤러에게 가므로 그 리소스의 이벤트 로그를 봐야 한다.",
    11, MUTED, KR, "start")
d.legend(BY + 40, [("먼저 재는 자리", ACC), ("허용하고 센다", OK), ("허용하고 알린다", WARN), ("거부", BAD)])
d.save("../20-01.enforcement-ladder.svg")
print("필요 h:", BY + 40 + 48, "· 실제:", H)
