# 타입 스펙: type-sequence — alice@outlook.com 이 bob@gmail.com 에게 보낸 메일 한 통이 제출 → MX 조회 → SMTP 대화(220·250·354·221) 순으로 가고, 받는 서버가 닫혀 있으면 다음 MX 와 큐 재시도로 가는 왕복(레인 4, 항목 10).
# 사실 출처: dig MX gmail.com 실측(2026-10-12T17:28Z 에 5·10·20·30·40 다섯 줄, 바뀔 수 있음), RFC 5321 §5.1(MX 조회·낮은 값 우선)·§4.5.4.1(재시도 간격 30분 이상·포기 4~5일)·부록 D.1(220·250·354·221 대화 형식),
#   RFC 6409(제출 587, 중계는 포트 25 유지), Microsoft Support Outlook.com POP·IMAP·SMTP 설정 문서(SMTP 587 STARTTLS, 2026-10-13 열람; 465 는 RFC 8314 §3.3 의 일반 규격이라 라벨에서 뺌), 추출본 v1.txt 2763~2787행(Alice → Outlook → Gmail → Bob).
#   outlook 서버의 EHLO 호스트 이름은 쓰지 않았고 Gmail 의 실제 응답 문구는 RFC 부록 D.1 의 형식을 따른 것이다.
# Layout conventions: 레인 4·폭 196·간격 244, 호출 한 건의 stride 60(라벨 y-9, 부라벨 y+17), 첫 메시지 y=192, 구분선은 마지막 메시지 +60. SMTP 구간 라벨은 DNS 레인을 비켜 dx=122. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_08_02_seq import SeqKR

W, H = 1000, 940
d = SeqKR(W, H, "BYTEBYTEGO · 08-02 §1",
          "메일 한 통은 MX 조회로 받는 서버를 찾아 SMTP 대화로 넘어간다",
          "RFC 5321 부록의 대화 형식에 alice@outlook.com → bob@gmail.com 을 넣었고 MX 값은 2026-10-12 실측입니다.",
          "MX 값은 2026-10-12 실측이고 응답 코드의 형식은 RFC 5321 부록 D.1 을 따랐습니다")
C, O, N, G = "Alice 앱", "outlook 메일 서버", "DNS", "gmail 메일 서버"
d.lanes([(C, "alice@outlook.com"), (O, "SMTP 클라이언트"), (N, "MX 조회"), (G, "SMTP 서버")], 100, 196)
d.rails(H - 80)

Y0, ST = 192, 60
d.msg(C, O, "제출 587", Y0 + 0 * ST, MUTED, "ar", sub="수신인 bob@gmail.com")
d.msg(O, N, "MX gmail.com ?", Y0 + 1 * ST, INFO, "info")
d.msg(N, O, "5 gmail-smtp-in.l.google.com", Y0 + 2 * ST, INFO, "info", dash="5 4", sub="예비 10 · 20 · 30 · 40")
d.msg(G, O, "220", Y0 + 3 * ST, OK, "ok", dash="5 4", dx=122)
d.msg(O, G, "EHLO · MAIL FROM · RCPT TO", Y0 + 4 * ST, MUTED, "ar", sub="포트 25 · 줄마다 250 으로 답함", dx=122)
d.msg(O, G, "DATA · 본문 · .", Y0 + 5 * ST, MUTED, "ar", sub="DATA 에는 354 로 답함", dx=122)
d.msg(G, O, "250", Y0 + 6 * ST, OK, "ok", dash="5 4", dx=122)
d.msg(O, G, "QUIT", Y0 + 7 * ST, MUTED, "ar", sub="221 로 연결을 닫음", dx=122)
d.divider(Y0 + 8 * ST + 4, "받는 서버가 열리지 않을 때", ACC)
d.selfmsg(O, "다음 MX 로 같은 대화", Y0 + 9 * ST + 16, WARN, sub="낮은 값에서 높은 값으로 10 → 40")
d.selfmsg(O, "큐에 보관", Y0 + 10 * ST + 16, BAD, sub="30분 이상 간격 재시도 · 4~5일 이상 뒤 포기")

d.legend(H - 56, [("요청", MUTED), ("DNS", INFO), ("응답", OK), ("다음 후보", WARN), ("실패", BAD), ("분기", ACC)])
d.save("08-02.mx-sequence.svg")
