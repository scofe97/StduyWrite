# 07-01 §1 — template 을 만난 질의가 어디로 갈라지는가. 정규식 불일치의 행선지가 이 절의 함정이다.
# 원문 근거: "The top-line arguments of CLASS TYPE and ZONE (s) are used to match the incoming
#            request. Next, the regular expression defined in match is checked; if it does not
#            meet the criteria, the query will just be passed on." / 현재 공식 문서:
#            "Without `fallthrough`, when the template's ZONE matches a query but no regex match
#            then a `SERVFAIL` response is returned."
# 타입 스펙: type-flowchart — 분기가 논지다. 마름모 셋의 출구가 서로 다른 곳으로 가고,
#           그중 하나가 원서 산문이 말하지 않은 SERVFAIL 이다. 마름모는 마커 없는 path 라
#           dd-lint 의 diagonal 검사 대상이 아니다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 660
d = D(W, H, "LEARNING COREDNS · 07-01 §1",
      "template 을 만난 질의가 갈라지는 자리",
      "질의가 template 플러그인을 지날 때의 분기. 마름모 셋을 차례로 통과해야 답이 만들어지고, "
      "마지막 마름모에서 fallthrough 가 없으면 SERVFAIL 이 돌아간다.",
      "주황이 원서 산문이 말하지 않는 출구입니다")

SP, RT = 250, 620          # 왼쪽 척추 · 오른쪽 열
HW, HH = 130, 36


def diamond(cx, cy, l1, l2, c=MUTED):
    d.path(f"M {cx} {cy - HH} L {cx + HW} {cy} L {cx} {cy + HH} L {cx - HW} {cy} Z", c, 1.2)
    d.t(cx, cy - 3, l1, 12, INK, MONO)
    d.t(cx, cy + 16, l2, 12, INK, KR)


# 시작
d.box(SP - 90, 96, 180, 40, PAPER2, RULE, 1.0, 20)
d.t(SP, 121, "질의 도착", 13, INK, KR, "middle", 600)
d.arrow([(SP, 136), (SP, 172)], MUTED, "ar", 1.4)

diamond(SP, 210, "CLASS · TYPE · ZONE", "이 요청과 맞는가")
d.arrow([(SP, 246), (SP, 302)], MUTED, "ar", 1.4)
d.t(SP + 12, 278, "예", 11, MUTED, KR, "start")
d.arrow([(SP + HW, 210), (RT - 122, 210)], MUTED, "ar", 1.4)
d.t((SP + HW + RT - 122) / 2, 200, "아니오", 11, MUTED, KR)

diamond(SP, 340, "match 정규식이", "맞는가")
d.arrow([(SP, 376), (SP, 436)], OK, "ok", 1.5)
d.t(SP + 12, 410, "예", 11, OK, KR, "start")
d.arrow([(SP + HW, 340), (RT - HW - 2, 340)], MUTED, "ar", 1.4)
d.t((SP + HW + RT - HW) / 2, 330, "아니오", 11, MUTED, KR)

diamond(RT, 340, "fallthrough 가", "적혀 있는가")
d.arrow([(RT, 304), (RT, 244)], MUTED, "ar", 1.4)
d.t(RT + 12, 278, "예", 11, MUTED, KR, "start")
d.arrow([(RT, 376), (RT, 458)], BAD, "bad", 1.5)
d.t(RT + 12, 422, "아니오", 11, BAD, KR, "start")

# 오른쪽 위 — 체인으로 넘김
d.box(RT - 120, 182, 240, 60, PAPER2, RULE, 1.0)
d.t(RT, 208, "다음 플러그인으로", 13, INK, KR, "middle", 600)
d.t(RT, 227, "forward · file · kubernetes", 10, MUTED, MONO)

# 왼쪽 아래 — 답 생성
d.tone(SP - 120, 438, 240, 64, OK, 6, "12", 1.4)
d.t(SP, 464, "answer 를 전개해 응답", 13, OK, KR, "middle", 600)
d.t(SP, 484, "{{ .Name }} 이 질문 이름", 11, OK, MONO)

# 오른쪽 아래 — SERVFAIL
d.tone(RT - 120, 460, 240, 56, BAD, 20, "14", 1.5)
d.t(RT, 484, "SERVFAIL", 15, BAD, MONO, "middle", 600)
d.t(RT, 503, "원서 산문이 말하지 않는 출구", 11, BAD, KR)

# 곁주석 — 같은 예제 안에서 두 블록이 갈린다
d.box(20, 532, 840, 56, PAPER, RULE, 0.8)
d.t(36, 554, "같은 Corefile 의 두 블록이 여기서 갈린다", 12, INK, KR, "start", 600)
d.t(36, 576, "A 템플릿은 fallthrough 를 적었고, PTR 템플릿은 적지 않았다", 11, MUTED, KR, "start")

d.legend(600, [("답이 만들어지는 출구", OK), ("체인으로 넘기는 출구", MUTED), ("실패로 끝나는 출구", BAD)])
d.save("07-01.template-branch.svg")
