# 08-01 §4 — 로그 하나가 무엇으로 이루어지는가.
# 원문("Logging"): "From a structural perspective, overall, a log comprises the following:
#       A collection of log items, messages, or lines — Captures information about a discrete event.
#       Metadata or context — Can be present on a per-message basis as well as on a global scope (the
#       entire log file, for example).
#       A format for how an individual log message is to be interpreted — Defines the log's parts and
#       meanings. Examples are line-oriented, space-separated messages or a JSON schema."
#       또 "while every log has some structure ... you will often hear the term structured logging. When
#       people say that, they actually mean that the log is structured using JSON."
# 타입 스펙: type-nested — 포함 관계로 드러나는 계층. 로그 파일이 항목들을 담고 항목이 다시 부분을
#           담으며, 형식은 그 부분들에 뜻을 부여하는 규칙이라 바깥에서 안쪽 전부에 걸린다.
#           축약: 형식 다섯 종류는 본문 표가 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §4",
      "로그는 항목과 문맥과 형식 셋으로 이루어진다",
      "저자가 로그를 구조 관점에서 셋으로 쪼갠 것을 포함 관계로 세운 것. 바깥 테두리가 형식인 이유는 "
      "형식이 안쪽의 각 부분에 뜻을 부여하는 규칙이기 때문이다.",
      "구조화 로깅이라고 말할 때 사람들이 실제로 뜻하는 것은 JSON 입니다")

OX, OY, OW, OH = 24, 108, 832, 300
d.o.append(f'<rect x="{OX}" y="{OY}" width="{OW}" height="{OH}" rx="10" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 5"/>')
d.t(OX + 20, OY + 26, "형식 — 개별 메시지를 어떻게 해석할지 정한다", 14, ACC, KR, "start", 600)
d.t(OX + 20, OY + 46, "줄 단위 공백 구분 · JSON 스키마 · Syslog", 11.5, ACC, MONO, "start")

MX, MY, MW, MH = OX + 20, OY + 62, OW - 40, 60
d.box(MX, MY, MW, MH, PAPER2, INFO, 1.2, 8)
d.t(MX + 18, MY + 24, "전역 메타데이터 · 문맥", 13, INFO, KR, "start", 600)
d.t(MX + 18, MY + 44, "파일 전체에 걸리는 정보. 저자는 메시지마다 붙을 수도, 파일 전체 범위로 붙을 수도 있다고 적는다.",
    11.5, MUTED, KR, "start")

IX, IY, IW, IH = MX, MY + MH + 14, MW, 148
d.box(IX, IY, IW, IH, PAPER, RULE, 1.1, 8)
d.t(IX + 18, IY + 26, "로그 항목의 모음 — 메시지 · 줄", 13, INK, KR, "start", 600)
d.t(IX + 18, IY + 46, "항목 하나가 개별 사건 하나를 담는다", 11.5, MUTED, KR, "start")

EW, EH = (IW - 56) / 3, 60
items = [("타임스탬프", "대개 붙는다", MUTED),
         ("텍스트 페이로드", "사람이 읽는다", OK),
         ("항목별 메타데이터", "요청 ID 같은 것", MUTED)]
for k, (nm, sub, col) in enumerate(items):
    x = IX + 18 + k * (EW + 10)
    d.box(x, IY + 62, EW, EH, PAPER2, col, 1.1, 6)
    d.t(x + 12, IY + 84, nm, 12.5, col if col is OK else INK, KR, "start", 600)
    d.t(x + 12, IY + 104, sub, 11, MUTED, KR, "start")

NY = OY + OH + 26
d.t(24, NY + 4, "저자가 로그를 정의하는 문장은 한 줄입니다 — 텍스트 페이로드를 가진 개별 사건들이고, "
                "사람이 소비하라고 있는 것입니다.", 12, MUTED, KR, "start")
d.t(24, NY + 26, "그래서 로그 메시지의 범위를 작고 구체적으로 두라고 적습니다. 읽는 사람이 코드의 "
                 "해당 위치를 찾기 쉬워야 하기 때문입니다.", 12, MUTED, KR, "start")
d.t(24, NY + 48, "형식이 스키마로 표현되면 검증을 자동으로 돌릴 수 있다는 것이 형식을 바깥에 그린 이유입니다.",
    12, SOFT, KR, "start")

d.legend(H - 56, [("바깥에서 전부에 걸리는 규칙", ACC), ("파일 전체 범위의 문맥", INFO),
                  ("사람이 읽는 자리", OK), ("항목과 그 부분들", MUTED)])
d.save("08-01.log-anatomy.svg")
print("ok 08-01.log-anatomy")
