# 45-01 「3. 솔트 붙은 느린 해시로 지키는 비밀번호」 — 같은 비밀번호도 솔트가 다르면 해시가 다르고, 같은 솔트면 해시가 같다.
# 본문 근거: 이 노트 「솔트가 같은 비밀번호를 다른 해시로 만든다」 절.
# 값 근거: 2026-11-08 openssl 3.6.4 의 openssl passwd -6 -salt <솔트> hunter2 를 세 번 돌렸다.
#   aaaaaaaa → $6$aaaaaaaa$n5EoGxOUiOpqF.NaoAr7vijY0cdUp7kCsOEW4XjuJ1NOfOte9MuYHzrEUkCfPs1xm9eiWcvSQevkZoGO.VhFZ1 (두 번 모두 같음)
#   bbbbbbbb → $6$bbbbbbbb$5crrZLm9nFVREgN2nAVy649lIT4uUhwgG8kJI2STZ5cDEZOasNNKoq/.CuPEk657EQRmvUqU/9VipN3/uqXnZ/
#   hunter2 는 예시용 비밀번호이고 passwd -6 은 솔트 효과를 보이려는 용도다(권장 방식이 아님).
# 공식 근거: NIST SP 800-63B-4 §3.1.1.2(솔트는 32비트 이상, 저장된 해시끼리 겹치지 않게).
# 타입 스펙: type-data-flow — 실행마다 입력 → 해시 연산 → 출력, 출력끼리 같은지 다른지를 오른쪽에 표시.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, KR, MONO

W, H = 880, 392
d = D(W, H, "OSTEP · 45-01 §3",
      "같은 비밀번호도 솔트가 다르면 해시가 달라진다",
      "세 번의 실행이 같은 비밀번호 hunter2 를 해시한다. 첫째와 둘째는 솔트 aaaaaaaa 를 쓰고 출력이 서로 같다. "
      "셋째는 솔트 bbbbbbbb 를 쓰고 출력의 앞자리가 5crrZL 로 첫째의 n5EoGx 와 다르다.")

IN_X, IN_W = 52, 180
FN_X, FN_W = 268, 152
OUT_X, OUT_W = 456, 280
ROW_Y, STRIDE, RH = 112, 76, 56

runs = [
    ("aaaaaaaa", "$6$aaaaaaaa$n5EoGx…", OK, "기준", MUTED),
    ("aaaaaaaa", "$6$aaaaaaaa$n5EoGx…", OK, "= 1번과 같음", OK),
    ("bbbbbbbb", "$6$bbbbbbbb$5crrZL…", ACC, "≠ 1번과 다름", ACC),
]
for i, (salt, out, c, note, nc) in enumerate(runs):
    y = ROW_Y + i * STRIDE
    cy = y + RH / 2
    d.chip(28, cy, str(i + 1), MUTED, 12, 6)
    d.tone(IN_X, y, IN_W, RH, SOFT, 6, "14", 1.1)
    d.t(IN_X + 14, y + 24, "hunter2", 12, INK, MONO, "start", 600)
    d.t(IN_X + 14, y + 44, "salt = " + salt, 12, MUTED, MONO, "start")
    d.arrow([(IN_X + IN_W + 2, cy), (FN_X - 4, cy)], MUTED, "ar", 1.4)
    d.tone(FN_X, y, FN_W, RH, INFO, 6, "14", 1.1)
    d.t(FN_X + FN_W / 2, y + 24, "해시 연산", 12.5, INK, KR, "middle", 600)
    d.t(FN_X + FN_W / 2, y + 44, "passwd -6", 12, MUTED, MONO, "middle")
    d.arrow([(FN_X + FN_W + 2, cy), (OUT_X - 4, cy)], MUTED, "ar", 1.4)
    d.tone(OUT_X, y, OUT_W, RH, c, 6, "14", 1.6 if c == ACC else 1.1)
    d.t(OUT_X + OUT_W / 2, cy + 4, out, 12, INK, MONO, "middle", 600)
    d.chip(796, cy, note, nc, 12)

d.legend(352, [("입력", SOFT), ("해시 연산", INFO), ("같은 해시", OK), ("다른 해시", ACC)])
d.save("45-01.salted-hash.svg")
