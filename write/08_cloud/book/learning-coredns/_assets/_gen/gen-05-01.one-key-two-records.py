# 05-01 §5 — SkyDNS 메시지 한 줄의 필드가 A 응답과 SRV 응답의 어느 칸으로 가는가.
# 본문 근거: 이 노트 §5 의 put 값과 두 dig 응답(원서 Example 5-3·5-7 의 값).
# 소스 근거: plugin/etcd/etcd.go 의 defaultTTL=300·defaultPriority=10, plugin/backend_lookup.go 의 가중치 재계산.
# 타입 스펙: type-dp-security-matrix — 필드(행) × 응답 종류(열) 격자에서 어느 칸이 그대로이고 어느 칸이 바뀌는가가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING COREDNS · 05-01 §5",
      "메시지 한 줄의 필드가 응답 두 종류로 갈라진다",
      "host 는 A 응답의 주소가 되고, port·priority·weight 는 SRV 응답의 칸이 된다. "
      "넣지 않은 ttl 은 기본값 300 으로 채워지고, weight 20 은 같은 우선순위 합 대비 백분율인 100 으로 바뀐다.",
      "주황 칸이 등록값과 다르게 나오는 자리입니다")

COLS = [(20, 130, "필드"), (160, 210, "메시지에 넣은 값"), (380, 220, "A 응답"), (610, 250, "SRV 응답")]
NA = ("—", "", SOFT)
rows = [
    ("host", ('"192.0.2.10"', "", INK), ("192.0.2.10", "주소 그대로", INK), ("ADDITIONAL 의 A", "대상 이름을 풀어 줌", INK)),
    ("port", ("20020", "", INK), NA, ("20020", "포트 칸", INK)),
    ("priority", ("10", "", INK), NA, ("10", "적은 값 그대로", INK)),
    ("weight", ("20", "", INK), NA, ("100", "같은 우선순위 합 대비 %", ACC)),
    ("ttl", ("없음", "", MUTED), ("300", "기본값 defaultTTL", INK), ("300", "기본값 defaultTTL", INK)),
]

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (field, *cells) in enumerate(rows):
    y = 132 + i * 60
    x0, w0, _ = COLS[0]
    d.box(x0, y, w0, 52, PAPER2, RULE, 1.0, 6)
    d.t(x0 + 12, y + 31, field, 14, INK, MONO, "start", 600)
    for k, (main, sub, c) in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        if c == ACC:
            d.tone(x, y, w, 52, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 52, PAPER2, RULE, 1.0, 6)
        fam = KR if any("가" <= ch <= "힣" for ch in main) else MONO
        if sub:
            d.t(x + 12, y + 22, main, 14, c, fam, "start", 600)
            d.t(x + 12, y + 42, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 31, main, 14, c, fam, "start", 600)

d.t(20, 460, "키 /skydns/com/example/services/users 하나 · 응답 두 종류 · TTL 300 은 두 응답 모두", 13, MUTED, KR, "start")

d.legend(476, [("등록값과 다른 응답값", ACC)])
d.save("05-01.one-key-two-records.svg")
