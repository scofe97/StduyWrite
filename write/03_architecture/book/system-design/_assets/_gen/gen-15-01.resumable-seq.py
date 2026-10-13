# 타입 스펙: type-sequence — 클라이언트와 Drive API 두 레인. 세션 시작 → 첫 청크 → 연결 끊김 → 상태 조회 → 이어 보내기. 메시지마다 실제 헤더 값이 나온다.
# 사실 출처: Google Drive API v3 "Manage file uploads"(https://developers.google.com/workspace/drive/api/guides/manage-uploads)의 재개 가능 업로드 절:
#   POST https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable → 200 OK + Location(…&upload_id=xa298sd_sdlkj2),
#   청크는 256 KB(256 x 1024 bytes)의 배수, `Content-Range: bytes 0-524287/2000000`(2,000,000 바이트 파일의 첫 524,288 바이트),
#   중단 뒤 빈 PUT 에 `Content-Range: bytes */<전체 크기>` → 308 Resume Incomplete 와 Range 헤더(예 bytes=0-42 는 43 바이트 수신).
#   계산: 524,288 = 256 × 1,024 × 2 · 다음 청크 524,288 + 524,288 − 1 = 1,048,575.
# Layout conventions: 레인 폭 200·중심 x=200·680, 메시지 stride 56(y=192부터), 상태 칩 y=412·640, 레일 하단 H-80. 모든 좌표 4의 배수.
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
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="20" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 13, MUTED, _kr(sub))

    def chip(s, a, txt, y, c):
        x = s.LX[a]; w = _w(txt, 13) + 12
        s.o.append(f'<rect x="{x - w/2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w/2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 13, c, _kr(txt))


W, H = 880, 720
d = SeqKR(W, H, "SYSTEM DESIGN INTERVIEW · 15-01 §2",
          "끊긴 업로드는 상태를 물어 받은 바이트 다음부터 이어 보낸다",
          "세션 URI 하나에 청크를 PUT 하고, 끊기면 빈 PUT 으로 Range 를 받아 524,288 바이트 다음부터 다시 보낸다.",
          "2,000,000 바이트 파일 · 청크 524,288 바이트")

C, S = "클라이언트", "Drive API"
d.LX = {C: 200, S: 680}
for nm, sub, x in ((C, "2,000,000 바이트 파일", 200), (S, "upload/drive/v3/files", 680)):
    d.box(x - 100, 100, 200, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 13, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.msg(C, S, "POST ?uploadType=resumable", 192, INFO, "info")
d.msg(S, C, "200 · Location …upload_id=xa298sd_sdlkj2", 248, INFO, "info", dash="5 4")
d.msg(C, S, "PUT Content-Range: bytes 0-524287/2000000", 304, MUTED, sub="청크 = 256 KB × 2")
d.msg(S, C, "308 Resume Incomplete", 360, MUTED, dash="5 4")
d.chip(C, "연결 끊김", 412, BAD)
d.msg(C, S, "PUT Content-Range: bytes */2000000", 468, WARN, "warn", sub="본문 없음")
d.msg(S, C, "308 · Range: bytes=0-524287", 524, WARN, "warn", dash="5 4")
d.msg(C, S, "PUT Content-Range: bytes 524288-1048575/2000000", 580, ACC, "acc", sub="받은 바이트 다음부터")
d.chip(S, "마지막 청크 뒤 200 OK · 201 Created", 640, OK)

d.legend(H - 56, [("세션 시작", INFO), ("청크 전송", MUTED), ("상태 조회", WARN), ("이어 보내기", ACC), ("완료", OK), ("연결 끊김", BAD)])
d.save("15-01.resumable-seq.svg")
