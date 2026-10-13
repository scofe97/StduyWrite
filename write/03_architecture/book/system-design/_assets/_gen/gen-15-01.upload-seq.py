# 타입 스펙: type-sequence — 참여자 여섯(클라이언트 1 · API 서버 · 메타데이터 DB · 블록 서버 · 클라우드 저장소 · 알림 서비스). 메타데이터 갈래가 pending 을 기록하고 내용 갈래가 끝나면 uploaded 로 바뀐다. focal 은 uploaded 전환.
# 사실 출처: 추출본 v2.txt 4605~4627행(두 요청 병렬: 메타데이터 추가 → pending → 알림 → 클라이언트 2 통지 / 내용 → 블록 서버 분할·압축·암호화·업로드 → 완료 콜백 → uploaded → 알림).
#   12 MB 파일 = 4 MB × 3 블록은 설명용 값이다.
#   이벤트 발신 주체는 개략 설계 그림(API 서버 → 알림 서비스) 기준이다. 업로드 순서 그림은 두 notify change 화살표를 메타데이터 DB 에서 알림 서비스로 그려 서로 어긋나며, 발신 주체를 API 서버로 둔 것은 이 도식의 선택이다.
# Layout conventions: 레인 폭 132·중심 x=90·254·418·582·746·910, 메시지 stride 48(y=192부터), 상태 칩 y=264·620, 레일 하단 H-80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 13)/2}" y="{y - 23}" width="{_w(label, 13)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)

    def chip(s, a, txt, y, c):
        x = s.LX[a]; w = _w(txt, 13) + 12
        s.o.append(f'<rect x="{x - w/2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w/2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 13, c, _kr(txt))


W, H = 1000, 744
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 15-01 §7",
          "메타데이터가 pending 으로 먼저 적히고 내용이 닿으면 uploaded 가 된다",
          "클라이언트 1 이 메타데이터와 내용을 병렬로 보내고, 클라우드 저장소의 완료 콜백이 상태를 바꾼 뒤에야 알림이 uploaded 를 알린다.",
          "12 MB 파일 = 4 MB × 3 블록")

NAMES = (("클라이언트 1", "12 MB 파일"), ("API 서버", "메타데이터"), ("메타데이터 DB", "file · block"),
         ("블록 서버", "4 MB × 3"), ("클라우드 저장소", "S3"), ("알림 서비스", "→ 클라이언트 2"))
XS = (90, 254, 418, 582, 746, 910)
d.LX = {}
for (nm, sub), x in zip(NAMES, XS):
    d.LX[nm] = x
    d.box(x - 66, 100, 132, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 13, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

C1, API, DB, BLK, CLD, NTF = (n for n, _ in NAMES)
d.msg(C1, API, "파일 메타데이터 추가", 192, INFO, "info")
d.msg(API, DB, "INSERT file", 240, INFO, "info")
d.chip(DB, "pending", 272, WARN)
d.msg(API, NTF, "새 파일 이벤트", 312, INFO, "info")
d.msg(C1, BLK, "파일 내용 전송", 360, MUTED)
d.chip(BLK, "분할 · 압축 · 암호화", 396, MUTED)
d.msg(BLK, CLD, "블록 3 개 PUT", 440, MUTED)
d.msg(CLD, API, "완료 콜백", 488, WARN, "warn")
d.msg(API, DB, "status = uploaded", 536, ACC, "acc")
d.chip(DB, "uploaded", 568, OK)
d.msg(API, NTF, "상태 변경 이벤트", 608, OK, "ok")
d.chip(NTF, "클라이언트 2 에 통지", 644, OK)

d.legend(H - 56, [("메타데이터 갈래", INFO), ("내용 갈래", MUTED), ("완료 콜백", WARN), ("상태 전환", ACC), ("uploaded", OK)])
d.save("15-01.upload-seq.svg")
