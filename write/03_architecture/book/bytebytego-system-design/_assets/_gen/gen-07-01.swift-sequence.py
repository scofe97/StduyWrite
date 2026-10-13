# 타입 스펙: type-sequence — 뉴욕의 은행 A 가 낸 송금 메시지가 지역 처리기와 슬라이스 처리기에 저장되고 런던의 은행 B 까지 전달된 뒤 수신 확인(UAK)과 보고서가 되돌아오는 왕복(레인 6, 항목 15).
# 사실 출처: 추출본 v1.txt 1868~1960행(Step 1~17: Regional/Slice Processor, ACK/NAK, MON(공식 용어 미확인이라 도식에서는 '출력 번호'), UAK/UNK; 용어는 developer.swift.com 용어집 FIN·Slice Processor), PDF 78쪽 그림 번호 1~17 중 1~14 는 행 1~14 와 같고 행 15 는 16(보고서 사본), 15·17(보고서 저장)은 생략.
#   Swift 보도자료 2025-11-25 의 "does not hold funds or manage accounts" · 벨기에 본부. 이 처리 단계는 Swift 공식 명세가 아닌 공개 설명이라 출력 번호(공개 설명의 MON) 검증 순서는 공식 문서로 확인하지 못했다.
# Layout conventions: 레인 6·폭 128·간격 160, 메시지 한 건의 stride 48(라벨 y-9, 부라벨 y+17), 첫 메시지 y=204. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_07_01_seq import SeqKR

W, H = 1000, 996
d = SeqKR(W, H, "BYTEBYTEGO · 07-01 §3",
          "FIN 에서 MT 송금 메시지는 허가된 뒤에야 상대 은행에 닿는다",
          "MT 메시지가 처리기 네 곳에 저장되고 은행 B 에 닿으며, ACK 와 UAK 와 보고서가 되돌아옵니다.",
          "저장과 허가를 거친 메시지만 상대 은행에 전달됩니다")
A, RA, SA, RB, SB, B = "은행 A", "지역 처리기 A", "슬라이스 A", "지역 처리기 B", "슬라이스 B", "은행 B"
d.lanes([(A, "뉴욕"), (RA, "입력 검증"), (SA, "저장·라우팅"), (RB, "출력 큐"), (SB, "저장·라우팅"), (B, "런던")], 100, 128)
d.rails(H - 80)

Y0, S = 204, 48
r = 0


def y():
    return Y0 + r * S + (8 if r >= 13 else 0)


d.msg(A, RA, "1 송금 메시지", y(), MUTED, "ar", sub="수신 은행 B"); r += 1
d.msg(RA, SA, "2 형식 검증 후 전달", y(), MUTED, "ar"); r += 1
d.selfmsg(SA, "3 저장", y(), WARN); r += 1
d.msg(SA, RA, "4 저장 완료", y(), OK, "ok", dash="5 4"); r += 1
d.msg(RA, A, "5 ACK / NAK", y(), OK, "ok", dash="5 4", sub="ACK 면 B 로 보냄"); r += 1
d.msg(SA, RB, "6 메시지 전달", y(), MUTED, "ar"); r += 1
d.selfmsg(RB, "7 임시 저장", y(), WARN); r += 1
d.msg(RB, SB, "8 출력 번호 부여", y(), ACC, "acc"); r += 1
d.selfmsg(SB, "9 출력 번호 검증", y(), WARN); r += 1
d.msg(SB, RB, "10 전달 허가", y(), OK, "ok", dash="5 4"); r += 1
d.msg(RB, B, "11 메시지", y(), MUTED, "ar", dx=-80); r += 1
d.selfmsg(B, "12 저장", y(), WARN, left=True); r += 1
d.msg(B, RB, "13 UAK / UNK", y(), OK, "ok", dash="5 4", sub="UNK 는 체크섬 실패", dx=80); r += 1
d.msg(RB, SB, "14 보고서", y(), MUTED, "ar"); r += 1
d.msg(SB, SA, "15 보고서 사본", y(), MUTED, "ar", dx=-80); r += 1

d.legend(H - 56, [("전달", MUTED), ("저장", WARN), ("확인·허가", OK), ("출력 번호", ACC)])
d.save("07-01.swift-sequence.svg")
