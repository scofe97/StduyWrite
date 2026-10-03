# 07-03 §3 — 안 될 때 curl 의 종료 코드가 어느 층인지 가른다.
# 원문("The curl Command"): 저자는 -v 를 "verbose ... use it to troubleshoot" 라고만 적고
#       무엇을 어떻게 가르는지는 말하지 않는다.
# 노트의 읽기: 2026-09-07 Phase 3 실습에서 직접 잰 종료 코드 셋을 요청이 *어디까지 갔는가* 로
#       늘어놓은 것. 실측값 — 6 "Could not resolve host", 7 "Failed to connect ... after 0 ms",
#       28 "Connection timed out after 6005 milliseconds".
#       2026-10-03 보강 — TCP 가 붙은 뒤의 두 단계를 더했다. curl 8.7.1(macOS) 로 로컬 서버에 잰 값:
#       35 "SSL connect error"(평문 포트에 https), 60 "SSL certificate problem: self signed certificate",
#       22(-f 에서 404·503), 52 "Empty reply from server", 47 "Maximum (5) redirects followed".
#       번호와 뜻은 man curl EXIT CODES 축자 대조. accept 큐가 찬 포트는 7 이 아니라 28 로 끝났다
#       (OrbStack ubuntu, backlog 3 · accept 안 함 · 클라이언트 여섯 — ss 의 LISTEN 행 Recv-Q 4 · Send-Q 3).
#       논점은 0 ms 와 6005 ms 다. 즉시 실패는 상대가 대답했다는 뜻이라 도달에는 성공한 것이고,
#       한도를 다 채운 실패는 아무도 대답하지 않은 것이라 길이나 중간을 봐야 한다.
# 타입 스펙: type-process — 요청이 지나는 단계를 왼쪽에서 오른쪽으로 늘어놓고 각 단계에서
#       빠져나가는 실패를 아래로 떨군다. 07-03.chapter-overview 도 같은 타입이지만 그쪽은
#       문서의 읽는 순서를 그리고 이쪽은 요청의 진행 단계를 그린다 — 대상이 다르다.
#       coral 은 하나뿐이며 아무도 대답하지 않아 한도까지 기다린 자리다.
#       축약: 층 이름(L3·L4·L7)은 앞 두 편이 이미 세웠으므로 단계 이름만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 726
d = D(W, H, "LEARNING MODERN LINUX · 07-03 §3",
      "종료 코드가 요청이 어디까지 갔는지를 말해 준다",
      "curl 한 방이면 어느 층에서 끊겼는지 부류가 갈린다. 6 은 이름에서, 7 은 포트에서, "
      "28 은 아무 대답도 못 받고 한도까지 기다린 것이다. 35·60 은 TLS 에서, 22·52·47 은 응답에서 끊긴 것이다.",
      "0 ms 와 6005 ms 가 갈라 줍니다")

SX, SW, SGAP, SY, SH = 24, 140, 20, 168, 62
stages = [
    ("이름 해석", "이름 → IP"),
    ("길 찾기", "라우팅 테이블"),
    ("상대 도착", "패킷이 건너간다"),
    ("포트 열림", "듣는 소켓이 있나"),
    ("TLS", "인증서를 확인한다"),
    ("응답", "HTTP 가 돌아온다"),
]
for i, (name, note) in enumerate(stages):
    x = SX + i * (SW + SGAP)
    d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, SY + 26, name, 12.5, INK, KR, "middle", 600)
    d.t(x + SW / 2, SY + 46, note, 11.5, MUTED, KR)
    if i < len(stages) - 1:
        d.arrow([(x + SW + 1, SY + SH / 2), (x + SW + SGAP - 2, SY + SH / 2)], SOFT, "soft", 1.3)

# 각 실패가 어느 단계에서 빠져나가는가 — (단계 index, 코드, 메시지, 시간, 색, 다음에 볼 것)
FY = 292
exits = [
    (0, "exit 6", "Could not resolve host", None, INFO, "dig · resolv.conf"),
    (3, "exit 7", "Failed to connect", "0 ms", OK, "상대에서 ss -tlnp"),
    (2, "exit 28", "Connection timed out", "6005 ms", ACC, "라우팅 · 방화벽"),
    (4, "exit 35·60", ("핸드셰이크 실패", "인증서 검증 실패"), None, WARN, "openssl s_client"),
    (5, "exit 22·52·47", ("-f 일 때 4xx·5xx", "빈 응답 · 리다이렉트"), None, WARN, "curl -v · 서버 로그"),
]
for idx, code, msg, ms, col, nxt in exits:
    x = SX + idx * (SW + SGAP)
    focal = (col is ACC)
    # 단계에서 아래로 떨어지는 실패
    d.arrow([(x + SW / 2, SY + SH + 4), (x + SW / 2, FY - 4)], col,
            "acc" if focal else {OK: "ok", WARN: "warn"}.get(col, "info"), 1.3, dash="4 4")
    if focal:
        d.tone(x, FY, SW, 96, ACC, 8, "12", 1.5)
    else:
        d.box(x, FY, SW, 96, PAPER2, col, 1.2, 8)
    d.t(x + SW / 2, FY + 24, code, 14, col, MONO, "middle", 600)
    if isinstance(msg, tuple):
        for j, line in enumerate(msg):
            d.t(x + SW / 2, FY + 44 + j * 18, line, 11, MUTED, KR)
    else:
        d.t(x + SW / 2, FY + 44, msg, 10, MUTED, MONO)
    if ms:
        d.chip(x + SW / 2, FY + 64, ms, col, 11.5)
    d.t(x + SW / 2, FY + 88, nxt, 11.5, MUTED, KR)

BY = FY + 116
d.tone(24, BY, W - 48, 78, ACC)
d.t(44, BY + 26, "0 ms 는 상대가 대답했다는 뜻입니다", 13, INK, KR, "start", 600)
d.t(44, BY + 48, "즉시 거절당하려면 패킷이 거기까지 갔다 와야 합니다. 도달에는 성공했고 그 포트만 안 열린 것입니다.",
    12, MUTED, KR, "start")
d.t(44, BY + 68, "한도를 다 채웠다면 아무도 대답하지 않은 것이라, 길이 없거나 중간의 무엇이 조용히 버린 것입니다.",
    12, MUTED, KR, "start")

OY = BY + 96
d.t(24, OY, "가른 뒤의 순서", 12.5, INK, KR, "start", 600)
steps = [
    ("1", "curl", "부류를 가른다 — 6·7·28"),
    ("2", "route -n get", "길이 있는지 (28 일 때)"),
    ("3", "ping", "상대가 살아 있는지"),
    ("4", "traceroute", "어디까지 갔는지 좁힌다"),
]
OW, OG = 190, 24
for i, (n, cmd, why) in enumerate(steps):
    x = 24 + i * (OW + OG)
    d.box(x, OY + 14, OW, 52, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, OY + 38, n, 12, SOFT, MONO, "start", 600)
    d.t(x + 32, OY + 36, cmd, 12, INK, MONO, "start", 600)
    d.t(x + 32, OY + 56, why, 11, MUTED, KR, "start")
    if i < len(steps) - 1:
        d.arrow([(x + OW + 1, OY + 40), (x + OW + OG - 2, OY + 40)], SOFT, "soft", 1.2)

d.t(24, OY + 90, "넷이 다 멀쩡한데 28 이 나면 마지막 후보가 accept 큐 포화입니다 — 상대에서 ss -tln 의 Recv-Q 가 Send-Q 를 넘었는지 봅니다.",
    11.5, MUTED, KR, "start")

d.legend(OY + 110, [("이름에서 끊김", INFO), ("도달했고 포트만", OK), ("아무 대답 없음", ACC), ("연결 뒤에서 끊김", WARN)])
d.save("07-03.curl-exit-triage.svg")
print("ok 07-03.curl-exit-triage")
