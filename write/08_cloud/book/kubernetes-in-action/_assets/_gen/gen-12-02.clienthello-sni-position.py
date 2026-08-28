# 12-02 §2 — 평문 구간은 생각보다 짧다
# 캡션이 "핸드셰이크 앞의 두 메시지뿐"을 요구한다. 메시지 순서 위에 평문 구간을 대괄호로
# 묶어야 그 짧음이 보인다. SNI 가 실린 자리 하나만 focal.
# 타입 스펙: type-gantt.md — 메시지 순서를 축으로 삼고 평문·암호화 구간을 대괄호로 잰다. 시간축이 아니라 순서축이지만
#           구간의 시작과 끝이 논지라는 점은 같다 — SNI 가 평문 구간 안에 든다는 것이 결론이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1160, 684, "KUBERNETES IN ACTION · 12-02",
      "SNI 는 첫 메시지 안에 있다",
      "TLS 1.3 에서는 ServerHello 직후 키 교환이 끝나 그 뒤로는 서버 인증서마저 암호화되어 전송된다. "
      "프록시가 passthrough 에서 건질 수 있는 것은 맨 앞 두 메시지뿐이다.",
      "클라이언트가 TLS 를 시작하는 순간")

MSG = [("ClientHello", "SNI · 지원 암호군 · 키 공유", ACC, True),
       ("ServerHello", "고른 암호군 · 키 공유", None, False),
       ("Certificate", "서버 인증서", WARN, False),
       ("Finished", "핸드셰이크 종료", WARN, False),
       ("Application Data", "HTTP 요청 · Host 헤더", WARN, False)]
Y0, H, GP = 168, 62, 14
for i, (t, s, c, focal) in enumerate(MSG):
    y = Y0 + i * (H + GP)
    if focal:
        d.o.append(f'<rect x="220" y="{y}" width="560" height="{H}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(220, y, 560, H, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(260, y + 26, t, 13, tc, MONO, "start", 600)
    d.t(260, y + 47, s, 11, MUTED, KR, "start")

ddx.bracket(d, 180, Y0, Y0 + 2 * H + GP, "평문", SOFT)
ddx.bracket(d, 180, Y0 + 2 * (H + GP), Y0 + 5 * H + 4 * GP, "암호화", WARN)
d.t(812, 200, "여기 실린 server_name 을", 11, ACC, KR, "start")
d.t(812, 222, "프록시가 암호 없이 읽는다", 11, ACC, KR, "start")
d.t(812, 400, "TLS 1.3 에서는 인증서까지", 11, WARN, KR, "start")
d.t(812, 422, "암호화되어 실린다", 11, WARN, KR, "start")

d.t(24, 570, "Host 헤더와 값이 같아 헷갈리기 쉬운데 층이 다르다. SNI 는 TLS 의 필드라 암호화 전에 오가고, "
             "Host 는 HTTP 의 헤더라 암호화 후에 실린다.", 11, MUTED, KR, "start")
d.legend(596, [("암호 없이 읽히는 자리", ACC), ("암호 뒤", WARN)])
d.save("12-02-clienthello-sni-position.svg")
print("ok")
