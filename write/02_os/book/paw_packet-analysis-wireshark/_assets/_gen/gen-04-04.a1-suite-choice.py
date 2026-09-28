# 04-04 A1 — 클라이언트가 제안한 28개 중 서버가 무엇을 고르나. 실측값(a1-handshake.pcap)만 쓴다.
# 타입 스펙: type-sequence — 두 주체 사이의 시간순 메시지. focal 은 1순위를 건너뛴 ServerHello 선택 하나.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import seq, ACC, INFO, WARN
d = seq("A1", "A1 · 서버는 1순위를 고르지 않는다",
        "ClientHello 가 묶음 28개를 제안하고 1순위는 ECDHE_ECDSA 계열이다. 서버 인증서가 RSA 키라 ECDSA 서명을 할 수 없어, 서버는 그 계열을 건너뛰고 0xc030 을 고른다.",
        "서버의 선택 범위는 인증서의 키 종류가 좁힙니다", 460)
d.rails(392)
d.msg("클라이언트", "서버", "ClientHello", 200, INFO, "info", sub="프레임 5 · 묶음 28개 제안 · 1순위 ECDHE_ECDSA 계열")
d.state("서버", "인증서 키 = RSA", 252, WARN)
d.state("서버", "ECDSA 계열 건너뜀", 284, WARN)
d.msg("서버", "클라이언트", "ServerHello · 0xc030", 348, ACC, "acc", sub="TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384")
d.legend(412, [("서버가 고른 묶음", ACC), ("클라이언트의 제안", INFO), ("선택을 좁히는 조건", WARN)])
d.save("04-04.a1-suite-choice.svg")
