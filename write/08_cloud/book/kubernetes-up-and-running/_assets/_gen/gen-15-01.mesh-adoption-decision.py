# 15-01 §정말 필요한가 — 저자의 판단 순서
# 본문이 마지막에 스스로 교정한다. "메시 없음" 은 정당한 답이지만 장 전체의 결론은
# "선택할 수 있다면 관리형 메시를 쓰라" 쪽이다. 그러니 관리형을 맨 앞 갈림에 두고 초점으로
# 삼아야 하고, "메시 없음" 을 사다리 끝 종착지로 그리면 본문이 틀려진다.
# 맨 위 전제(실패하면 앱 전체가 멈춘다) 는 곁가지가 아니라 이 순서가 성립하는 이유다.
# 타입 스펙: type-flowchart.md — 관문 둘에서 갈라져 결과 셋으로 가는 판정 라우팅이고, 정본이
#           요구하는 대로 나가는 화살표에 전부 라벨(예 · 아니오)이 붙고 초점은 한 경로에만 있다.
#           어긋나는 지점: 판정 칸이 마름모가 아니라 상자다 — 둘째 관문이 조건 셋을 칩으로
#           품어야 해서 마름모에 안 들어간다. 정본의 "마름모는 3 출구 이하" 를 지키려면 조건을
#           밖으로 빼야 하는데, 그러면 무엇을 감당해야 하는지가 판정에서 떨어져 나간다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 658
d = D(W, H, "KUBERNETES UP AND RUNNING · 15-01",
      "직접 떠안지 말라는 쪽이 결론이다",
      "서비스 메시는 애플리케이션 설계에 복잡도를 더하는 분산 시스템이고, 마이크로서비스의 핵심 "
      "통신에 깊이 통합된다. 도입은 기능 비교가 아니라 운영 각오의 문제다.",
      "저자는 장을 '선택할 수 있다면 관리형 메시를 쓰라' 로 맺는다")

d.o.append(f'<rect x="12" y="110" width="{W-36}" height="66" rx="8" '
           f'fill="{BAD}0E" stroke="{BAD}" stroke-width="1.2"/>')
d.t(W / 2, 138, "전제 — 메시는 핵심 통신에 깊이 통합되므로, 메시가 실패하면 애플리케이션 전체가 멈춘다.",
     12, BAD, KR)
d.t(W / 2, 160, "아래 순서는 그 장애 반경을 누가 떠안을 것인가를 묻는다.", 11, BAD, KR)

GX, GW = 40, 420
OX, OW = 560, 640

def gate(y0, y1, title, chips=()):
    d.box(GX, y0, GW, y1 - y0, PAPER2, RULE, 1.1, 6)
    d.t(GX + GW / 2, y0 + 34, ddx.fit(title, 13, GW - 40, title), 13, INK, KR, "middle", 600)
    for i, ch in enumerate(chips):
        yy = y0 + 50 + i * 26
        d.o.append(f'<rect x="{GX+20}" y="{yy}" width="{GW-40}" height="22" rx="4" '
                   f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
        d.t(GX + 32, yy + 15, ddx.fit(ch, 10, GW - 64, ch), 10, MUTED, KR, "start")

def outcome(y0, y1, title, subs, c, focal=False, eyebrow=None):
    if focal:
        d.o.append(f'<rect x="{OX}" y="{y0}" width="{OW}" height="{y1-y0}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(OX, y0, OW, y1 - y0, PAPER2, c, 1.1, 6)
    if eyebrow:
        d.t(OX + OW - 20, y0 + 20, eyebrow, 9, SOFT, KR, "end")
    d.t(OX + 24, y0 + 34, title, 14, c, KR, "start", 600)
    for i, s in enumerate(subs):
        d.t(OX + 24, y0 + 58 + i * 20, ddx.fit(s, 11, OW - 48, s), 11,
            c if focal else MUTED, KR, "start")

gate(210, 286, "클라우드 제공자가 관리형 메시를 주는가")
gate(320, 456, "이 셋을 감당할 수 있는가",
     ("문제가 생겼을 때 고칠 수 있다는 확신",
      "보안·버그 수정을 놓치지 않게 릴리스를 계속 지켜본다",
      "애플리케이션에 영향을 주지 않고 새 버전을 롤아웃한다"))

outcome(200, 296, "관리형 메시를 쓴다",
        ["지원·디버깅·매끄러운 새 릴리스를 클라우드 제공자가 맡는다",
         "그래도 개발자가 배워야 할 복잡도는 남는다"], ACC, focal=True)
outcome(320, 396, "메시 없음",
        ["많은 소규모 애플리케이션에 메시는 불필요한 복잡도다"], MUTED)
outcome(430, 526, "직접 운영한다",
        ["화려한 데모와 기능 약속에 끌려가지 않는다",
         "메시 API 는 구현에 종속적이라 시간이 쌓이면 바꾸기 어렵다"], WARN,
        eyebrow="사실상의 표준으로 자리 잡은 메시는 아직 없다")

d.path(f"M {GX+GW} 248 L {OX-4} 248", ACC, 1.5, m="acc")
d.t((GX + GW + OX) / 2, 236, "예", 11, ACC, KR)
d.path(f"M 250 286 L 250 316", MUTED, 1.4, m="ar")
d.t(264, 306, "아니오", 10, SOFT, KR, "start")
d.path(f"M {GX+GW} 358 L {OX-4} 358", MUTED, 1.4, m="ar")
d.t((GX + GW + OX) / 2, 346, "아니오", 11, SOFT, KR)
d.path(f"M 250 456 L 250 478 L {OX-4} 478", WARN, 1.4, m="warn")
d.t(264, 472, "예", 10, WARN, KR, "start")

d.t(GX, 566, "판단은 애플리케이션 팀 또는 플랫폼 팀이 클러스터 수준에서 한다 — 서비스 하나하나가 각자 정할 일이 아니다.",
     11, MUTED, KR, "start")
d.t(GX, 588, "이득을 최대로 하려면 클러스터의 모든 마이크로서비스가 동시에 채택하는 편이 좋다. 책은 그 이유까지 적지 않는다.",
     11, MUTED, KR, "start")

d.legend(610, [("저자가 권하는 쪽", ACC), ("감당해야 할 것", WARN), ("전제 — 장애 반경", BAD)])
d.save("15-01.mesh-adoption-decision.svg")
print("h 필요:", 610 + 48, " 실제:", H)
