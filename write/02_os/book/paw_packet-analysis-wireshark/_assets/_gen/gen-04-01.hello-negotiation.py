# 04-01 §3 「협상 결과를 화면에서 읽어야 할 때」 — ClientHello 가 내민 것 중 ServerHello 가 무엇을 돌려주는가.
# 본문 요구: "ClientHello는 지원하는 조건을 제안하고 ServerHello는 사용할 조건을 선택합니다."
#            "공통 조합이 없으면 협상할 수 없습니다." 필드마다 줄어드는 방식이 달라, 한 줄 산문으로는
#            '목록 → 하나' 가 어느 필드 얘기인지 안 선다.
# 필드별 사실은 RFC 5246 원문 기준이다.
#   버전   §7.4.1.2 client_version "the latest (highest valued) version supported by the client" — 목록이 아니라 값 하나
#          §7.4.1.3 server_version "the lower of that suggested by the client ... and the highest supported by the server"
#   suite  §7.4.1.3 "The single cipher suite selected by the server from the list in ClientHello.cipher_suites"
#          §7.4.1.2 "if no acceptable choices are presented, return a handshake failure alert"
#   확장   §7.4.1.3 "only extensions offered by the client can appear in the server's list" — 하나가 아니라 부분집합
# 타입 스펙: type-data-flow — 클라이언트 → 서버 → 응답으로 필드 셋이 건너가며 줄어든다(데이터가 칸을 건넌다).
#           §2 공식은 728 폭·9px 글자를 내 스타일 계약(880~1000 폭·한글 12px 이상)과 충돌하므로,
#           같은 폴더 client-key-exchange 와 같은 3열 좌표계로 축약했다. 행 stride 112.
#           focal 은 ServerHello 의 cipher suite 칸 — 본문이 "답은 Server Hello 한 줄에 있다" 고 짚는 자리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 680
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §3",
      "Client Hello 가 내밀고 Server Hello 가 고른다",
      "TLS 1.2 기준으로 필드 셋이 ClientHello 에서 ServerHello 로 건너가며 어떻게 줄어드는지 그렸다. "
      "버전은 클라이언트가 원하는 가장 높은 값 하나와 서버의 최고 버전 중 낮은 쪽이 되고, "
      "cipher suite 는 선호 순 목록에서 하나가 되며, 확장은 제안된 것 안에서 응답할 것만 돌아온다. "
      "고를 cipher suite 가 없으면 서버는 handshake_failure Alert 로 끝낸다.",
      "TLS 1.2 · 목록이 하나로 줄어드는 것은 cipher suite 입니다")

CW, CH = 288, 80                  # 좌우 카드
L, R = 24 + CW / 2, W - 24 - CW / 2   # 168 · 792
M, MW, MH = W / 2, 184, 44        # 가운데 규칙 칸
Y = [224, 336, 448]               # 버전 · 확장 · cipher suite — suite 를 맨 아래에 두어 실패 갈래가 다른 행을 건너지 않게 한다

for cx, lab in ((L, "ClientHello 가 내미는 것"), (M, "서버가 고르는 규칙"), (R, "ServerHello 가 돌려주는 것")):
    d.t(cx, 160, lab, 13, SOFT, KR)

def card(cx, cy, title, field, what, c=None, focal=False):
    x, y = cx - CW / 2, cy - CH / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, CW, CH, c, 8)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    col = ACC if focal else (c if c else INK)
    d.t(x + 18, y + 28, title, 13, col, KR, "start", 600)
    d.t(x + CW - 18, y + 28, field, 12, MUTED, MONO, "end")
    d.t(x + 18, y + 58, what, 12, INK if focal else MUTED, KR, "start")

def rule(cy, txt, c=MUTED):
    d.box(M - MW / 2, cy - MH / 2, MW, MH, PAPER, c, 1.0, 22)
    d.t(M, cy + 5, txt, 12, c if c is not MUTED else INK, KR)

# 연결선 먼저(z-order)
for y in Y:
    d.arrow([(L + CW / 2, y), (M - MW / 2 - 8, y)], MUTED, "ar", 1.4)
    d.arrow([(M + MW / 2, y), (R - CW / 2 - 8, y)], ACC if y == Y[2] else MUTED, "acc" if y == Y[2] else "ar", 1.5)

card(L, Y[0], "버전", "client_version", "지원하는 가장 높은 값 하나")
rule(Y[0], "둘 중 낮은 쪽")
card(R, Y[0], "버전", "server_version", "TLS 1.2 · 0x0303")

card(L, Y[1], "확장", "extensions", "요청하는 확장 목록")
rule(Y[1], "제안된 것 안에서만")
card(R, Y[1], "확장", "extensions", "응답할 확장만")

card(L, Y[2], "cipher suite", "cipher_suites", "선호 순 목록 · 여럿", c=INFO)
rule(Y[2], "목록에서 하나", INFO)
card(R, Y[2], "cipher suite", "cipher_suite", "그중 하나 · 0xc030", focal=True)

# 고를 suite 가 없을 때 — 가운데 칸에서 곧장 아래로 빠진다
FAIL_Y = 572
d.arrow([(M, Y[2] + MH / 2), (M, FAIL_Y - 24 - 8)], BAD, "bad", 1.4, "5 4")
d.t(M - 14, Y[2] + MH / 2 + 34, "고를 suite 없음", 12, BAD, KR, "end")
d.tone(M - 136, FAIL_Y - 24, 272, 48, BAD, 8)
d.t(M, FAIL_Y - 2, "Alert · handshake_failure(40)", 13, BAD, MONO, "middle", 600)
d.t(M, FAIL_Y + 16, "ServerHello 대신 연결 종료", 12, MUTED, KR)
d.t(R - CW / 2, FAIL_Y + 4, "버전이 안 맞을 때는 protocol_version(70)", 12, SOFT, KR, "start")

d.legend(H - 40, [("본문이 짚는 선택 결과", ACC), ("목록이 하나로 줄어드는 필드", INFO), ("협상 실패", BAD)])
d.save("04-01.hello-negotiation.svg")
