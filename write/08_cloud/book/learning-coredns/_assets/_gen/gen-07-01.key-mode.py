# 07-01 §7 — dnssec 플러그인이 설정된 키의 SEP 비트 조합으로 서명 방식을 정하는 규칙.
# 근거: dnssec README(v1.5.0 와 master 같은 글) "If multiple keys are specified of which there is at least one key with the SEP bit set
#       and at least one key with the SEP bit unset, signing will happen in split ZSK/KSK mode. DNSKEY records will be signed with all keys
#       that have the SEP bit set. All other records will be signed with all keys that do not have the SEP bit set. In any other case,
#       each specified key will be treated as a CSK".
# 타입 스펙: type-dp-security-matrix — 키 구성(행) × 판정·서명 대상(열) 격자, 원서가 말하지 않은 행이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 07-01 §7",
      "SEP 비트가 켜진 키와 꺼진 키가 다 있어야 나뉜다",
      "KSK 는 SEP 비트를 켠 키다. 켠 키와 끈 키가 함께 있을 때만 DNSKEY 는 켠 키로, 나머지는 끈 키로 나눠 서명한다. "
      "그 밖의 조합은 모두 CSK 로 보고 각 키가 전부를 서명한다. v1.5.0 문서도 같은 규칙이다.",
      "주황 행이 원서가 다루지 않은 경우입니다")

COLS = [(20, 260, "설정한 키"), (290, 150, "판정"), (450, 200, "DNSKEY 서명"), (660, 200, "나머지 레코드 서명")]
rows = [
    (("KSK 하나 + ZSK 하나", "SEP 켬 · 끔"), "분리", "KSK", "ZSK"),
    (("ZSK 하나", "SEP 끔 · 원서가 든 경우"), "CSK", "그 키", "그 키"),
    (("KSK 하나", "SEP 켬"), "CSK", "그 키", "그 키"),
    (("ZSK 둘", "SEP 둘 다 끔"), "CSK", "두 키 모두", "두 키 모두"),
]
FOCAL = 2

for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (keys, mode, k1, k2) in enumerate(rows):
    y = 132 + i * 66
    foc = i == FOCAL
    if foc:
        d.tone(16, y - 3, 848, 64, ACC, 8, "12", 1.4)
    x, w, _ = COLS[0]
    if not foc:
        d.box(x, y, w, 58, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 25, keys[0], 13, ACC if foc else INK, KR, "start", 600)
    d.t(x + 12, y + 45, keys[1], 12, MUTED, KR, "start")
    for k, v in ((1, mode), (2, k1), (3, k2)):
        x, w, _ = COLS[k]
        if not foc:
            d.box(x, y, w, 58, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + 35, v, 14, ACC if (foc and k == 1) else INK, KR if any("가" <= c <= "힣" for c in v) else MONO, "start", 600)

d.t(20, 412, "원서 · KSK 플래그 없는 키 하나면 CSK · 같은 시절 README 를 줄여 옮긴 표현", 13, MUTED, KR, "start")

d.legend(426, [("원서가 다루지 않은 경우", ACC)])
d.save("07-01.key-mode.svg")
