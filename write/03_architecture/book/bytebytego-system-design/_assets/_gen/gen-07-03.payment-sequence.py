# 타입 스펙: type-sequence — 구매 버튼 한 번이 결제 이벤트 하나가 되고 결제 주문으로 쪼개져 실행기·PSP·지갑·원장을 차례로 지나며 단계마다 저장 값이 남는 왕복(레인 6, 단계 10).
# 사실 출처: 추출본 v1.txt 3767~3830행(결제 단계 열 개: 이벤트 저장·주문마다 실행기 호출·주문 저장·PSP 호출·지갑 갱신·원장 추가·밤마다 정산 파일) 와 PDF 154쪽 그림(시스템 안쪽에 결제 서비스·실행기·지갑·원장, 바깥쪽에 PSP).
#   PE-1001·PO-A·PO-B·금액 30.00 = 20.00 + 10.00 USD 는 문서용 예시다.
# Layout conventions: 레인 6·폭 148·간격 156, 메시지 stride 52(라벨 y-9, 부라벨 y+17), 첫 메시지 y=192, 구분선 뒤 +4. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
sys.path.insert(0, "_gen")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO
from _cc_07_03_seq import SeqKR

W, H = 1000, 880
d = SeqKR(W, H, "BYTEBYTEGO · 07-03 §1",
          "결제 이벤트 하나는 주문 둘로 쪼개져 지갑과 원장까지 열 단계를 지난다",
          "PE-1001 이벤트 30.00 USD 가 판매자 둘의 주문 20.00 과 10.00 으로 나뉘어 처리되는 순서입니다.",
          "금액과 번호는 문서용 예시이고 PSP 는 시스템 경계 바깥입니다")
U, S, E, P, Wl, L = "사용자", "결제 서비스", "결제 실행기", "PSP", "지갑", "원장"
d.lanes([(U, "user"), (S, "payment service"), (E, "payment executor"), (P, "외부"), (Wl, "wallet"), (L, "ledger")], 100, 148)
d.rails(H - 80)

Y0, ST = 192, 52
d.msg(U, S, "1 결제 이벤트", Y0 + 0 * ST, MUTED, "ar", sub="PE-1001 30.00 USD")
d.state(S, "2 이벤트 저장", Y0 + 1 * ST, INFO)
d.msg(S, E, "3 결제 주문 2건", Y0 + 2 * ST, MUTED, "ar", sub="PO-A 20.00 USD")
d.state(E, "4 주문 저장", Y0 + 3 * ST, INFO)
d.msg(E, P, "5 카드 결제", Y0 + 4 * ST, WARN, "warn", sub="20.00 USD")
d.msg(S, Wl, "6 잔액 갱신", Y0 + 5 * ST, OK, "ok", sub="판매자 A +20.00")
d.state(Wl, "7 잔액 저장", Y0 + 6 * ST, INFO)
d.msg(S, L, "8 원장 갱신", Y0 + 7 * ST, OK, "ok", sub="거래 20.00 추가", dx=80)
d.state(L, "9 원장 추가", Y0 + 8 * ST, INFO)
d.divider(Y0 + 9 * ST, "매일 밤", ACC)
d.msg(P, S, "10 정산 파일", Y0 + 10 * ST + 4, ACC, "acc", dash="5 4", sub="당일 거래 전체")
d.state(E, "PO-B 10.00 은 4~9 반복", Y0 + 11 * ST + 8, MUTED)

d.legend(H - 56, [("요청", MUTED), ("외부 호출", WARN), ("갱신 호출", OK), ("저장", INFO), ("정산 파일", ACC)])
d.save("07-03.payment-sequence.svg")
