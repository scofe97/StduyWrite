# 2026-09-12 B(1초) 문항 · 원인 분석 — 두 단계 사이의 틈에서 같은 포트가 두 번 나간다.
# 회차에서 학습자가 "여유롭다는데 꽉 찰 수가 있나"로 포화를 스스로 지웠다.
# 포화가 아니라 경쟁이라는 것, 그리고 그 틈이 어디인지를 한 장에 고정한다.
# 타입 스펙: type-swimlane — 두 주체가 같은 시간축 위에서 각자 단계를 밟고,
#           레인 간 어긋남이 사건을 만든다. sequence 를 검토했으나 둘 사이에
#           주고받는 메시지가 없어 기각. flowchart 도 분기가 아니라 병행이라 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 828, 468
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-12 B",
      "같은 자리를 두 번 집습니다",
      "커널은 포트를 배정하는 일과 장부에 적는 일을 두 단계로 한다. 그 틈에 다른 흐름이 "
      "같은 포트를 배정받으면, 늦게 도착한 쪽이 장부에 못 들어가고 패킷이 버려진다.",
      lead="자리가 모자란 것이 아니라 같은 자리가 두 번 나간 것입니다")

LX, LW = 150, 640
STEPS = [("① 포트 배정", "패킷을 고친다"), ("틈", "아직 장부에 없다"), ("② 장부에 기록", "insert")]
for i, (t, sub) in enumerate(STEPS):
    x = LX + 24 + i * 208
    d.t(x + 80, 118, t, 12, SOFT, KR, "middle", 600)
    d.t(x + 80, 136, sub, 11, MUTED, MONO, "middle")

def lane(y, name, color, port_txt, result, rc):
    d.t(LX - 16, y + 34, name, 12, INK, KR, "end", 600)
    d.box(LX, y, LW, 66, PAPER2, RULE, 1.0, 6)
    d.tone(LX + 24, y + 13, 160, 40, color, 5)
    d.t(LX + 104, y + 38, port_txt, 12, color, MONO, "middle")
    d.arrow([(LX + 184, y + 33), (LX + 228, y + 33)], MUTED, "ar", 1.2)
    d.box(LX + 232, y + 13, 160, 40, PAPER2, RULE, 0.9, 5)
    d.t(LX + 312, y + 38, "이동 중", 12, SOFT, KR, "middle")
    d.arrow([(LX + 392, y + 33), (LX + 436, y + 33)], MUTED, "ar", 1.2)
    d.tone(LX + 440, y + 13, 176, 40, rc, 5)
    d.t(LX + 528, y + 38, result, 12, rc, KR, "middle", 600)

lane(156, "흐름 A", ACC, "포트 34817", "장부에 들어감", OK)
lane(240, "흐름 B", ACC, "포트 34817", "삽입 실패 · 폐기", BAD)

d.t(LX + 104, 322, "같은 값", 12, BAD, KR, "middle", 600)
d.path(f"M {LX + 104} {310} L {LX + 104} {228}", BAD, 1.4, dash="4 4")

d.t(W // 2, 366, "버려진 것은 연결을 여는 SYN 이라 커널이 1 · 3 · 7 초로 재전송합니다",
    13, MUTED, KR, "middle")
d.t(W // 2, 392, "재전송 때는 다른 포트를 받으므로 끝내 성공합니다", 12, SOFT, KR, "middle")
d.t(W // 2, 420, "conntrack -S 의 insert_failed 와 drop 이 함께 오르는 것이 서명입니다",
    12, ACC, MONO, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-12.snat-race.svg"))
print("ok")
