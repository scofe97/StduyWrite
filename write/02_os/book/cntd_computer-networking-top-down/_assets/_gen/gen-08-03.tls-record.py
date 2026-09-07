# 타입 스펙: type-nested — 암호화되는 범위가 안쪽에 있고 그 밖에 평문으로 남는 필드가 있다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.6.1 Figure 8.25 (책 595쪽) —
#   다섯 필드와 앞 셋이 암호화되지 않는다는 것, 순서 번호를 레코드가 아닌 HMAC 계산에 넣는 것은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 612
d = D(W, H, "SECTION 8.6.1 · THE TLS RECORD",
      "암호화되는 범위 밖에 남는 것이 있습니다",
      "타입·버전·길이는 평문으로 남는다. 받는 쪽이 흐름에서 레코드를 잘라 내려면 길이를 먼저 읽어야 하기 때문이다.",
      "다섯 필드와 암호화 범위는 원문 Figure 8.25 의 것입니다")

OX, OY, OW, OH = 24, 148, 952, 152
d.box(OX, OY, OW, OH, PAPER2, RULE, 1.0, 8)
d.t(OX + 20, OY + 28, "TLS 레코드", 12, INK, KR, "start", 600)
FIELDS = [(64, 128, "타입", "record type", WARN),
          (208, 128, "버전", "version", WARN),
          (352, 128, "길이", "length", WARN),
          (512, 232, "데이터", "응용 바이트", OK),
          (768, 176, "HMAC", "무결성 검사", ACC)]
for x, w, name, sub, c in FIELDS:
    d.tone(x, OY + 52, w, 72, c, 6, "20" if c is ACC else "14", 1.4 if c is ACC else 1.2)
    d.t(x + w / 2, OY + 84, name, 12, c, KR, "middle", 600)
    d.t(x + w / 2, OY + 106, sub, 10, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)

IX = 512
# 채움은 "none" 을 인자로 넘긴다. replace 로 fill 을 덧붙이면 속성이 둘이 되어 앞의 값이 이긴다.
d.box(IX - 8, OY + 44, 952 - (IX - 8) - 16, 88, "none", ACC, 1.3, 6)
d.o[-1] = d.o[-1].replace('stroke-width="1.3"', 'stroke-width="1.3" stroke-dasharray="6 5"')
d.t(IX + 216, OY + 146, "이 안쪽만 암호화됩니다", 11, ACC, KR)
d.t(200, OY + 146, "앞의 셋은 평문으로 나갑니다", 11, WARN, KR)

PY = 336
d.box(24, PY, 470, 172, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "레코드마다 검사해도 남는 구멍", 12, INK, KR, "start", 600)
d.line(44, PY + 40, 474, PY + 40, RULE, 0.8)
for i, ln in enumerate([
    "트루디가 세그먼트 둘의 순서를 뒤집고",
    "암호화되지 않은 TCP 순서 번호를 맞춥니다.",
    "",
    "레코드 하나하나는 HMAC 검사를 통과하는데",
    "전체 바이트 흐름의 순서가 틀립니다.",
]):
    if ln:
        d.t(44, PY + 66 + i * 22, ln, 11, MUTED if i < 3 else BAD, KR, "start")

d.tone(514, PY, 462, 172, OK, 8, "14", 1.3)
d.t(534, PY + 28, "순서 번호를 레코드가 아니라 HMAC 에", 12, OK, KR, "start", 600)
d.line(534, PY + 40, 956, PY + 40, RULE, 0.8)
for i, ln in enumerate([
    "레코드 안에 담으면 공격자가 그것도 바꿉니다.",
    "그래서 HMAC 계산에만 넣습니다.",
    "",
    "HMAC = 해시(데이터 + M_B + 현재 순서 번호)",
    "어긋나면 검사에서 걸립니다.",
]):
    if ln:
        d.t(534, PY + 66 + i * 22, ln, 11, OK if i == 3 else MUTED,
            MONO if i == 3 else KR, "start")

d.t(24, 532, "연결 종료도 타입 필드로 알립니다. 종료 레코드보다 TCP FIN 이 먼저 오면 절단 공격을 의심할 수 있습니다.",
    11, SOFT, KR, "start")
d.legend(552, [("평문으로 남는 필드", WARN), ("응용 데이터", OK), ("무결성 검사", ACC), ("남는 구멍", BAD)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-03.tls-record.svg"
d.save(out); print("→", out.name)
