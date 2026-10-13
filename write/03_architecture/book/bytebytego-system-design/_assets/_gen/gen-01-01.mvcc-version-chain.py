# 타입 스펙: type-data-flow — 한 행의 버전 두 개(roll pointer 로 이어짐)와 네 번의 읽기가 어느 버전에 닿는지. 읽기가 값을 나른다(100·200).
# 사실 출처: MySQL 9.7 문서 17.3 "InnoDB Multi-Versioning"(DB_TRX_ID·DB_ROLL_PTR, https://dev.mysql.com/doc/refman/9.7/en/innodb-multi-versioning.html)
#   · 17.7.2.3 "Consistent Nonlocking Reads"(REPEATABLE READ 는 첫 읽기의 스냅샷, READ COMMITTED 는 읽기마다 새 스냅샷). 값 100·200·trx 200·201 은 추출본 v1.txt 196~221행의 예시.
# Layout conventions: 버전 상자 폭 260·x=312, 읽기 줄 stride 44(같은 상자 안), 상자 사이 간격 32(roll pointer 화살표), 읽기 칩 x=700. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 436
d = D(W, H, "BYTEBYTEGO · 01-01 §2",
      "한 행의 버전 두 개와 네 번의 읽기",
      "트랜잭션 A 가 balance 를 200 으로 바꾸고 아직 커밋하지 않았을 때와 커밋한 뒤, 트랜잭션 B 가 읽는 값",
      "READ COMMITTED 는 커밋 뒤 새 값을, REPEATABLE READ 는 처음 읽은 값을 봅니다")

BX, BW = 312, 260
TOP_Y, TOP_H = 120, 48
BOT_Y, BOT_H = 200, 160   # 읽기 세 줄(stride 44)을 한 상자가 감싼다

# 위 버전 (A 가 만든 새 버전)
d.tone(BX, TOP_Y, BW, TOP_H, INFO, 6, "12", 1.2)
d.t(BX + BW / 2, TOP_Y + 20, "balance 200", 13, INFO, MONO, "middle", 600)
d.t(BX + BW / 2, TOP_Y + 38, "DB_TRX_ID 201", 12, MUTED, MONO)
# 아래 버전 (이전 커밋된 버전)
d.tone(BX, BOT_Y, BW, BOT_H, OK, 6, "12", 1.2)
d.t(BX + BW / 2, BOT_Y + 20, "balance 100", 13, OK, MONO, "middle", 600)
d.t(BX + BW / 2, BOT_Y + 38, "DB_TRX_ID 200", 12, MUTED, MONO)
# roll pointer: 위 버전 → 아래 버전
d.arrow([(BX + BW / 2, TOP_Y + TOP_H + 2), (BX + BW / 2, BOT_Y - 4)], MUTED, "ar", 1.4)
d.t(BX + BW / 2 + 12, TOP_Y + TOP_H + 22, "DB_ROLL_PTR", 12, MUTED, MONO, "start")

# 읽기 칩: 오른쪽, 상자 가장자리로 수평 화살표
RX = 664
reads = [
    (TOP_Y + 24, "READ COMMITTED · A 커밋 후", "200", INFO),
    (BOT_Y + 52, "READ COMMITTED · A 커밋 전", "100", OK),
    (BOT_Y + 96, "REPEATABLE READ · A 커밋 전", "100", OK),
    (BOT_Y + 140, "REPEATABLE READ · A 커밋 후", "100", OK),
]
for y, label, val, c in reads:
    d.t(RX + 12, y + 4, label, 12, INK, MONO, "start")
    d.arrow([(RX - 8, y), (BX + BW + 4, y)], c, "info" if c == INFO else "ok", 1.4)
    d.t(BX + BW + 28, y - 8, val, 12, c, MONO, "middle", 600)

# 왼쪽 주석: 트랜잭션 B 와 A
d.t(24, TOP_Y + 20, "트랜잭션 A", 13, INK, KR, "start", 600)
d.t(24, TOP_Y + 40, "UPDATE balance=200", 12, MUTED, MONO, "start")
d.t(RX + 12, TOP_Y - 12, "트랜잭션 B 의 읽기", 13, INK, KR, "start", 600)
d.t(24, BOT_Y + 20, "이전 커밋 버전", 13, INK, KR, "start", 600)

d.legend(H - 44, [("새 버전 200", INFO), ("이전 버전 100", OK)])
d.save("01-01.mvcc-version-chain.svg")
