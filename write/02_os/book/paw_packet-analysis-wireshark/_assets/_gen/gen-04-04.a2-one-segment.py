# 04-04 A2 — 서버의 네 메시지가 프레임 7 한 세그먼트에 레코드 넷으로 담겨 온다. look-tls.sh 표의 실측값만 쓴다.
# 타입 스펙: type-sequence — 프레임 단위 왕복. focal 은 레코드 넷을 실은 프레임 7 하나.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import seq, text_w, ACC, INFO, MUTED, PAPER, MONO
d = seq("A2", "A2 · 메시지 넷, 프레임 하나",
        "ServerHello·Certificate·ServerKeyExchange·ServerHelloDone 네 핸드셰이크 메시지가 프레임 7 한 세그먼트 안에 레코드 넷으로 실려 온다. 메시지 수와 패킷 수는 다르다.",
        "화살표 하나가 패킷 하나이고, 그 안의 칸이 레코드입니다", 500)
d.rails(432)
d.msg("클라이언트", "서버", "ClientHello", 200, INFO, "info", sub="프레임 5 · 레코드 1개 · 303")
d.msg("서버", "클라이언트", "프레임 7 · 세그먼트 하나", 280, ACC, "acc")
recs = ["ServerHello 65", "Certificate 796", "ServerKeyExchange 300", "ServerHelloDone 4"]
ws = [text_w(r, 11) + 16 for r in recs]; gap = 8
x = 428 - (sum(ws) + gap * (len(ws) - 1)) / 2
for r, w in zip(recs, ws):
    d.o.append(f'<rect x="{x:.1f}" y="{296}" width="{w:.1f}" height="24" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1"/>')
    d.t(x + w / 2, 312, r, 11, ACC, MONO)
    x += w + gap
d.t(428, 340, "handshake.type 2 · 11 · 12 · 14 · 레코드 길이 바이트", 11, MUTED)
d.msg("클라이언트", "서버", "프레임 9", 392, INFO, "info", sub="레코드 3개 · 37 · 1 · 40")
d.legend(452, [("레코드 넷을 실은 세그먼트", ACC), ("클라이언트 쪽 세그먼트", INFO)])
d.save("04-04.a2-one-segment.svg")
