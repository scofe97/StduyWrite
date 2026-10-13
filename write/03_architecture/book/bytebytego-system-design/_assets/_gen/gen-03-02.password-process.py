# 타입 스펙: type-process — 가입과 로그인 두 레인 × 입력·솔트·해시·저장(비교) 네 단계. 가입은 비밀번호와 새 솔트를 Argon2id 로 해시해 저장 문자열을 만들고, 로그인은 저장된 솔트와 비용으로 같은 계산을 해 저장값과 견준다.
# 사실 출처: OWASP Password Storage Cheat Sheet(https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) 의 Argon2id 최소 설정 m=19456(19 MiB)·t=2·p=1, 솔트는 사용자마다 유일한 난수. 저장 문자열 형식은 RFC 9106 §3.1 의 Argon2id 와 argon2 참조 구현의 인코딩($argon2id$v=19$m,t,p$솔트$해시).
#   값은 이 노트가 만든 시연 값을 argon2-cffi 25.1.0 의 argon2.low_level.hash_secret(b"hunter2", 솔트 16바이트 a1b2c3d4e5f60718293a4b5c6d7e8f90, time_cost=2, memory_cost=19456, parallelism=1, hash_len=32, type=ID) 로 계산:
#   $argon2id$v=19$m=19456,t=2,p=1$obLD1OX2BxgpOktcbX6PkA$YMTXCurjWaDXqfW4Jia1wikDHHvv6U50PQ+rsTy/DQU. 재현 스크립트: scratchpad/sdi/demo-bbg0302.py. 추출본 v1.txt 418~470행(저장·검증 두 흐름).
# Layout conventions: §2 공식을 폭 12px 글자에 맞게 조정 — 레인 라벨 열 폭 96, 단계 슬롯 stride 204·노드 폭 176, 노드 높이 124, 레인 stride 168(첫 레인 y=148). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 520
d = D(W, H, "BYTEBYTEGO · 03-02 §6",
      "솔트와 비용이 저장 문자열 하나에 담겨 로그인이 같은 계산을 되풀이한다",
      "가입은 새 솔트로 한 번 계산해 저장하고 로그인은 저장된 솔트와 비용으로 다시 계산해 견줍니다",
      "Argon2id · m=19456 · t=2 · p=1")

LABW, X0, SLOT, NW, NH = 96, 108, 204, 176, 124
LANE_Y = [148, 316]
heads = ["입력", "솔트", "해시", "저장 · 비교"]
for k, nm in enumerate(heads):
    d.t(X0 + k * SLOT + NW / 2, 124, nm, 12, SOFT, KR, "middle", 600)

for ln, (name, sub) in enumerate([("가입", "alice"), ("로그인", "alice")]):
    y = LANE_Y[ln]
    d.box(12, y, LABW - 12, NH, PAPER2, RULE, 0.9, 6)
    d.t(12 + (LABW - 12) / 2, y + 56, name, 13, INK, KR, "middle", 600)
    d.t(12 + (LABW - 12) / 2, y + 76, sub, 12, MUTED, MONO)


def node(k, ln, title, lines, c=INFO, focal=False):
    x, y = X0 + k * SLOT, LANE_Y[ln]
    if focal:
        d.tone(x, y, NW, NH, ACC, 6, "14", 1.4)
        tc = ACC
    else:
        d.tone(x, y, NW, NH, c, 6, "0c", 0.9)
        tc = c
    d.t(x + NW / 2, y + 24, title, 12, tc, KR, "middle", 600)
    for i, ln_ in enumerate(lines):
        d.t(x + NW / 2, y + 48 + i * 20, ln_, 12, INK, MONO if not any("가" <= ch <= "힣" for ch in ln_) else KR, "middle")


# 가입 레인
node(0, 0, "비밀번호", ["hunter2"])
node(1, 0, "새 솔트 16바이트", ["obLD1OX2…"])
node(2, 0, "Argon2id", ["m=19456", "t=2 · p=1"])
node(3, 0, "저장 문자열", ["$argon2id$v=19", "$m=19456,t=2,p=1", "$obLD1OX2…", "$YMTXCurj…"], ACC, True)
# 로그인 레인
node(0, 1, "입력", ["hunter2"])
node(1, 1, "저장된 솔트", ["obLD1OX2…"])
node(2, 1, "Argon2id", ["m=19456", "t=2 · p=1"])
node(3, 1, "재계산 = 저장값", ["YMTXCurj…", "일치 → 통과"], OK)

for ln in range(2):
    y = LANE_Y[ln] + NH / 2
    for k in range(3):
        d.arrow([(X0 + k * SLOT + NW + 2, y), (X0 + (k + 1) * SLOT - 4, y)], MUTED, "ar", 1.4)
# 저장 문자열 → 로그인 솔트·비교 (DB 에서 읽기)
dbx = X0 + 3 * SLOT + NW / 2
d.arrow([(dbx, LANE_Y[0] + NH + 2), (dbx, LANE_Y[1] - 4)], ACC, "acc", 1.4, "4 3")
d.t(dbx + 12, LANE_Y[0] + NH + 24, "DB 에서 읽기", 12, ACC, KR, "start")

d.legend(H - 44, [("저장되는 값", ACC), ("일치해 통과", OK), ("계산 단계", INFO)])
d.save("03-02.password-process.svg")
