# 10-01 §6 응답 플래그가 요청이 끝난 자리를 가리킨다.
# 본문(원문 10.3.3 · Envoy response flags 상자): UT 는 "the upstream was very slow according to the
#       timeout configuration". 자주 보는 나머지 넷은 UH(no healthy upstream — 클러스터에 워크로드가 없다),
#       NR(no route configured), UC(upstream connection termination), DC(downstream connection termination).
#       저자는 UT 가 붙어 있어 타임아웃 결정을 애플리케이션이 아니라 프록시가 했다는 것을 구분할 수 있다고 적는다.
# 상자 안의 영문은 저자가 적은 플래그 이름 그대로이고, 전이 라벨은 그 상태로 가는 계기다.
# "응답 대기" 의 부제는 upstream_service_time 이 아니라 라우트 타임아웃으로 적는다 — 원문 JSON 로그에서
#       타임아웃 요청의 upstream_service_time 은 "-" 이고 duration 만 503 으로 찬다.
# 타입 스펙: type-state — 커넥션 수명의 유한 상태. 시작은 채운 점, 끝은 링, 전이마다 라벨,
#           coral 은 독자가 주목할 상태 하나(이 장에서 실제로 만난 UT).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 624
d = D(W, H, "ISTIO IN ACTION · 10-01 §6",
      "플래그는 요청이 어디서 끝났는지를 적는다",
      "요청이 프록시 안에서 지나는 자리마다 실패로 끝날 수 있고, 액세스 로그의 두 글자가 그 자리를 "
      "지목한다. 색이 붙은 상태가 이 장의 504 이고, 그 두 글자 덕에 앱이 아니라 프록시가 끊었음을 안다.",
      "UT 가 있으면 타임아웃을 판정한 쪽이 애플리케이션이 아니라 프록시입니다")

SW, SH = 160, 56
MAIN_Y = 140
def state(x, y, w, h, label, sub, c=None, r=8):
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, r)
    d.t(x + w / 2, y + 24, label, 12, c or INK, KR, "middle", 600)
    d.t(x + w / 2, y + 42, sub, 9, MUTED, MONO)

S1, S2, S3 = 24, 276, 528
END_X, END_W = 780, 184
d.o.append(f'<circle cx="12" cy="{MAIN_Y + SH / 2}" r="6" fill="{INK}"/>')
d.arrow([(32, MAIN_Y + SH / 2), (S1 - 2, MAIN_Y + SH / 2)], MUTED, "ar", 1.4)
for a, b in ((S1, S2), (S2, S3), (S3, END_X)):
    d.arrow([(a + SW, MAIN_Y + SH / 2), (b - 2, MAIN_Y + SH / 2)], MUTED, "ar", 1.4)
for a_end, b_start, lab in ((S1 + SW, S2, "라우트 매칭"), (S2 + SW, S3, "커넥션"),
                            (S3 + SW, END_X, "응답 도착")):
    mx = (a_end + b_start) / 2
    mw = len(lab) * 11 + 12
    d.o.append(f'<rect x="{mx - mw / 2}" y="{MAIN_Y + SH / 2 - 26}" width="{mw}" height="18" rx="3" fill="{PAPER}"/>')
    d.t(mx, MAIN_Y + SH / 2 - 13, lab, 11, MUTED, KR, "middle")

state(S1, MAIN_Y, SW, SH, "요청 수신", "listener")
state(S2, MAIN_Y, SW, SH, "업스트림 선택", "route -> cluster")
state(S3, MAIN_Y, SW, SH, "응답 대기", "route timeout 0.5s")
state(END_X, MAIN_Y, END_W, SH, "응답 완료", "2xx", OK, r=24)
d.o.append(f'<circle cx="{END_X + END_W + 24}" cy="{MAIN_Y + SH / 2}" r="8" fill="none" stroke="{OK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{END_X + END_W + 24}" cy="{MAIN_Y + SH / 2}" r="5" fill="{OK}"/>')

TERM_Y, TW, TH = 400, 176, 60
terms = [(108, "NR", "no route configured", "라우트가 없다", False,
          f"M 104 {MAIN_Y + SH} V 296 H 108 V {TERM_Y - 4}"),
         (304, "UH", "no healthy upstream", "건강한 워크로드가 없다", False,
          f"M 356 {MAIN_Y + SH} V 296 H 304 V {TERM_Y - 4}"),
         (500, "UC", "upstream connection termination", "업스트림이 끊는다", False,
          f"M 564 {MAIN_Y + SH} V 296 H 500 V {TERM_Y - 4}"),
         (696, "UT", "upstream request timeout", "제한 시간을 넘긴다", True,
          f"M 608 {MAIN_Y + SH} V 320 H 696 V {TERM_Y - 4}"),
         (892, "DC", "downstream connection termination", "다운스트림이 끊는다", False,
          f"M 652 {MAIN_Y + SH} V 296 H 892 V {TERM_Y - 4}")]
for cx, code, eng, trig, focal, p in terms:
    d.path(p, ACC if focal else BAD, 1.4 if focal else 1.1, m="acc" if focal else "bad")
for cx, code, eng, trig, focal, p in terms:
    x = cx - TW / 2
    c = ACC if focal else BAD
    d.o.append(f'<rect x="{x}" y="{TERM_Y}" width="{TW}" height="{TH}" rx="8" fill="{c}12" stroke="{c}" stroke-width="{1.4 if focal else 1.2}"/>')
    d.t(cx, TERM_Y + 26, code, 13, c, MONO, "middle", 600)
    d.t(cx, TERM_Y + 46, eng, 8, MUTED, MONO)
    lw = len(trig) * 12 + 12
    d.o.append(f'<rect x="{cx - lw / 2}" y="{TERM_Y - 26}" width="{lw}" height="18" rx="3" fill="{PAPER}"/>')
    d.t(cx, TERM_Y - 13, trig, 11, c, KR, "middle", 600)

d.t(32, 508, "같은 요청이라도 어느 프록시가 적었는지에 따라 플래그가 갈린다 — 끊은 쪽은 UT, 끊긴 쪽은 DC 다", 11, SOFT, KR, "start")
d.t(32, 532, "전체 목록은 Envoy 공식 문서에 있고 저자는 자주 보는 다섯만 든다", 11, MUTED, KR, "start")
d.legend(556, [("이 장이 만든 504", ACC), ("실패로 끝나는 자리", BAD), ("정상 종료", OK)])
d.save("10-01.flag-states.svg")
