# 07-01 §5 metadata — 공급자가 값을 발행하고 소비자가 그 값을 쓰는 길을 실제 키 이름으로 잇는다.
# 근거: metadata README "any plugin that implements metadata.Provider interface will be called for each DNS query",
#       metadata_edns0 README 예제의 client_id 0xffed address, kubernetes README 의 kubernetes/client-namespace,
#       trace README 의 trace/traceid, template README 의 .Meta, dnstap README 의 EXTRA.
# 타입 스펙: type-data-flow — 공급자 → 발행된 키 → 소비자의 세 단계를 열로, 공급자 셋을 행으로 놓았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 07-01 §5",
      "metadata 는 값을 고치지 않고 넘겨 주기만 한다",
      "metadata.Provider 를 구현한 플러그인이 질의 초입에 값을 계산해 키 이름으로 발행하고, 뒤의 플러그인이 그 키를 읽는다. "
      "요청과 응답 자체는 그대로다.",
      "주황 열이 플러그인 사이를 오가는 값입니다")

COLS = [(20, 230, "공급자"), (270, 300, "발행된 키"), (590, 270, "소비자")]
rows = [
    (("metadata_edns0", "외부 · EDNS0 0xffed 를 address 로"), ("metadata_edns0/client_id", "엣지가 실어 보낸 주소"), ("log", "어느 사이트의 질의인지 남김")),
    (("kubernetes", "1.5.1 부터 공급자"), ("kubernetes/client-namespace", "질의한 파드의 네임스페이스"), ("template", ".Meta 로 답에 사용")),
    (("trace", "발행자로 등재"), ("trace/traceid", "추적 식별자"), ("dnstap", "EXTRA 필드에 실음")),
]

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 10, 118, head, 12, ACC if k == 1 else SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = 132 + i * 86
    for k, (a, b) in enumerate(cells):
        x, w, _ = COLS[k]
        if k == 1:
            d.tone(x, y, w, 70, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 70, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + 30, a, 13, ACC if k == 1 else INK, MONO, "start", 600)
        d.t(x + 12, y + 53, b, 12, MUTED, KR if any("가" <= c <= "힣" for c in b) else MONO, "start")
        if k < 2:
            nx = COLS[k + 1][0]
            d.path(f"M {x + w + 2} {y + 35} L {nx - 3} {y + 35}", MUTED, 1.2, m="ar")

d.t(20, 412, "원서가 기준으로 삼은 1.5.0 · 소비자는 log 와 rewrite 둘, 저장소 안 공급자는 없음", 13, MUTED, KR, "start")

d.legend(426, [("플러그인 사이를 오가는 값", ACC)])
d.save("07-01.metadata-flow.svg")
