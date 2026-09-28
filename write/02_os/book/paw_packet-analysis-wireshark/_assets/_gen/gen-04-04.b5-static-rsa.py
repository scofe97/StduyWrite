# 04-04 B5 — 정적 RSA(AES128-SHA)로 붙은 캡처(b5-static-rsa.pcap)의 메시지 구성. 표의 실측값만 쓴다.
# 타입 스펙: type-sequence — 프레임 단위 왕복. focal 은 오지 않은 ServerKeyExchange(12) 자리 하나.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import seq, ACC, INFO, MUTED
d = seq("B5", "B5 · 정적 RSA 에서 빠지는 메시지",
        "키 교환을 정적 RSA 로 고정하면 서버 메시지가 2·11·14 로 끝나 ServerKeyExchange(12) 가 없다. 대신 ClientKeyExchange 가 RSA 로 잠근 비밀 값을 실어 262 바이트로 커진다.",
        "새로 보낼 공개값이 없어 서버 쪽 메시지 하나가 사라집니다", 500)
d.rails(432)
d.msg("클라이언트", "서버", "ClientHello", 200, INFO, "info", sub="프레임 5 · --ciphers AES128-SHA · 136")
d.msg("서버", "클라이언트", "2 · 11 · 14", 272, MUTED, "ar", sub="프레임 7 · ServerHello · Certificate · ServerHelloDone")
d.ghost(428, 324, "ServerKeyExchange(12) 없음", ACC)
d.msg("클라이언트", "서버", "16 ClientKeyExchange · 262", 392, INFO, "info", sub="프레임 9 · RSA 로 잠근 비밀 값 · A1 의 ECDHE 는 37")
d.legend(452, [("오지 않은 메시지", ACC), ("클라이언트 쪽 메시지", INFO)])
d.save("04-04.b5-static-rsa.svg")
