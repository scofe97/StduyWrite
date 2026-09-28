# 04-04 C9 — 서버의 지원 목록을 밖에서 복원하는 반복. 140개 제안 · 서버에 건 세 묶음만 남는 실측.
# 타입 스펙: type-sequence — loop 결합 조각 안에서 제안 하나 → 수락·거절의 alt. focal 은 복원 결과.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import seq, ACC, INFO, OK, BAD
d = seq("C9", "C9 · 하나씩 붙여 목록을 복원한다",
        "서버에는 자기 목록을 알려 주는 메시지가 없다. 훑는 쪽은 ALL:@SECLEVEL=0 의 140개를 한 번에 하나씩 제안하고, ServerHello 가 온 것만 모은다. 서버에 세 묶음을 걸면 그 셋만 되돌아온다.",
        "nmap ssl-enum-ciphers 도 같은 방식으로 목록을 모읍니다", 576)
d.rails(508)
FX, FW = 104, 648
d.frame(FX, 172, FW, 272, "LOOP", "[140개 묶음마다 · -cipher 하나]")
d.msg("클라이언트", "서버", "ClientHello · 묶음 하나", 232, INFO, "info")
d.divider(FX, 260, FW, "[서버 목록에 있음]")
d.msg("서버", "클라이언트", "ServerHello", 316, OK, "ok", dash="5 4", sub="이 묶음을 목록에 적음")
d.divider(FX, 352, FW, "[서버 목록에 없음]")
d.msg("서버", "클라이언트", "Alert", 408, BAD, "bad", dash="5 4", sub="다음 묶음으로")
d.selfmsg("클라이언트", "모은 목록 = 서버에 건 세 묶음", 476, ACC)
d.legend(528, [("복원된 목록", ACC), ("수락", OK), ("거절", BAD), ("제안", INFO)])
d.save("04-04.c9-cipher-scan.svg")
