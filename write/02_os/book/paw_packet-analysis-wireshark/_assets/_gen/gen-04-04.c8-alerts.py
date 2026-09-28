# 04-04 C8 — 협상 조건을 두 번 어긋나게 했을 때 선에 남는 것. c8-alerts.pcap 의 Alert 두 줄 실측값만 쓴다.
# 타입 스펙: type-sequence — alt 결합 조각 두 구역(cipher 불일치 · 버전 불일치). focal 은 두 경우에 공통인 "ServerHello 없음".
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import seq, ACC, INFO, BAD
d = seq("C8", "C8 · 협상이 서지 못한 두 연결",
        "서버에 없는 묶음만 제안하면 desc 40 handshake_failure, TLS 1.1 을 제안하면 desc 70 protocol_version 이 온다. 두 경우 모두 ServerHello(2) 없이 2 바이트 Alert 레코드 하나로 끝난다.",
        "실패의 단서는 Alert 번호와, 오지 않은 종류 2 입니다", 620)
d.rails(552)
FX, FW = 104, 648
d.frame(FX, 172, FW, 312, "ALT", "[cipher 불일치 · -cipher AES256-SHA]")
d.msg("클라이언트", "서버", "ClientHello", 232, INFO, "info", sub="서버는 AES128-SHA 만")
d.msg("서버", "클라이언트", "Alert · 프레임 7", 300, BAD, "bad", sub="level 2 · desc 40 handshake_failure · 2 바이트")
d.divider(FX, 336, FW, "[버전 불일치 · -tls1_1 · SECLEVEL=0]")
d.msg("클라이언트", "서버", "ClientHello", 392, INFO, "info", sub="TLS 1.1 제안")
d.msg("서버", "클라이언트", "Alert · 프레임 17", 452, BAD, "bad", sub="level 2 · desc 70 protocol_version")
d.ghost(428, 516, "두 경우 모두 ServerHello(2) 없음", ACC)
d.legend(572, [("공통 단서", ACC), ("Alert 레코드", BAD), ("클라이언트의 제안", INFO)])
d.save("04-04.c8-alerts.svg")
