# 00-01.fd-lifetimes — listener FD 와 연결 FD 의 수명
# 본문 요구(00-01 「연결 소켓은 따로 닫아야 하는 이유」): "세 막대의 끝이 서로 다른 사건에 묶여 있다는
#           것이 두 소켓의 수명이 따로라는 말의 뜻입니다" — 막대의 시작·끝이 논지라 막대 길이가 곧 구간이다.
# 타입 스펙: type-gantt — 막대 길이가 곧 FD 가 열려 있는 구간. 시간 축은 사건 다섯 개의 순서뿐이다.
#           focal 은 conns 루프가 닫아야 끝나는 FD 8 하나다.
# 사실 출처: gonet-lab internal/tcp/server.go·client.go (2026-09-26). FD 번호 6·7·8 은 본문이 밝힌 예시다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 1000, 388
TX0, P = 200, 160                   # 시간 축 시작 · 사건 간격 (t0..t4 = 200..840)
RY0, RS, BH = 144, 56, 24           # 첫 줄 y · 줄 간격 · 막대 높이
LX = 24                             # 왼쪽 라벨 칸
GX = 960                            # 닫지 않았을 때의 점선 끝

d = D(W, H, "GANTT · 00-01 FD LIFETIMES",
      "listener FD 와 연결 FD 의 수명",
      "클라이언트 둘이 붙은 gonet 서버에서 FD 세 개가 언제 생기고 닫히는지를 시간 막대로 그린 도식. "
      "listener FD 는 종료 신호에, 클라이언트 1 의 연결 FD 는 클라이언트가 보낸 FIN 에, 접속만 걸어 둔 "
      "클라이언트 2 의 연결 FD 는 종료 뒤 conns 루프의 close 에 끝이 묶여 있다.",
      lead="세 막대의 끝이 서로 다른 사건에 묶여 있습니다.")

# 사건 눈금
events = ("net.Listen", "Accept", "Accept", "클라 1 FIN", "종료 신호")
for k, lab in enumerate(events):
    x = TX0 + k * P
    fam = KR if any("가" <= c <= "힣" for c in lab) else MONO
    d.t(x, 116, lab, 12, SOFT, fam, "start" if k == 0 else "middle")
    d.line(x, 128, x, 316, RULE, 0.8, "3 5")
d.line(TX0, 128, GX, 128, RULE, 0.8)

def row(i, name, sub, start, end, c, text, focal=False):
    y = RY0 + i * RS
    d.t(LX, y + 20, name, 13, INK, KR if any("가" <= c <= "힣" for c in name) else MONO, "start", 600)
    d.t(LX, y + 38, sub, 12, MUTED, KR, "start")
    x, w = TX0 + start * P, (end - start) * P
    d.tone(x, y + 12, w, BH, c, 4, "14" if focal else "10", 1.4 if focal else 1.0)
    d.t(x + 12, y + 29, text, 12, c, KR, "start", 600 if focal else 400)
    return y

row(0, "FD 6 listener", "remote 없음", 0, 4, INFO, "LISTEN · 종료 신호에 ln.Close")
row(1, "FD 7 연결", "클라이언트 1", 1, 3, OK, "ESTAB · FIN 받고 defer close")
y = row(2, "FD 8 연결", "클라이언트 2 · 접속만", 2, 4, ACC, "ESTAB · conns 루프가 close", focal=True)

# conns 루프가 없을 때 — 종료 뒤에도 열려 있음
d.line(TX0 + 4 * P, y + 24, GX, y + 24, WARN, 1.4, "5 4")
d.t(GX, y + 52, "루프가 없으면 계속 열림", 12, WARN, KR, "end")

d.legend(344, [("listener", INFO), ("스스로 닫힌 연결", OK), ("서버가 닫은 연결", ACC), ("닫지 않은 경우", WARN)])
d.save("00-01.fd-lifetimes.svg")
print("ok fd-lifetimes")
