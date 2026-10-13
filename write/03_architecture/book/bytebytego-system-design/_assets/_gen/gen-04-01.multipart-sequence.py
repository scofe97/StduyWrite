# 타입 스펙: type-sequence — 1.6 GB 를 200 MB 파트 8개로 올리는 멀티파트 업로드. 시작(uploadId) → 파트마다 ETag → part 2 가 끊겨 그 파트만 재전송 → 완료 요청에 파트 번호와 ETag 목록.
# 사실 출처: 추출본 v1.txt 1803~1827행과 쪽 74 그림(initiate · uploadID · 파트마다 ETag · complete 에 uploadID 와 파트 번호·ETag · success, 1.6 GB = 8 파트 × 200 MB)
#   · AWS S3 사용자 가이드 "Uploading and copying objects using multipart upload in Amazon S3"(https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html — 업로드 ID, 파트 번호 1~10,000, 파트마다 ETag 를 기록해 완료 요청에 포함, 실패한 파트만 다시 전송)
#   · API 이름 CreateMultipartUpload · UploadPart · CompleteMultipartUpload 는 같은 문서의 "Sample multipart upload calls". part 2 실패는 설명용 가정이다.
# Layout conventions: 레인 둘(폭 210), 메시지 stride 44(y=188 부터), 실패 메시지는 점선·BAD, 재전송은 ACC. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        s.t((x1 + x2) / 2, y - 9, label, 12, c, _kr(label), "middle", 600)


W, H = 920, 804
d = SeqKR(W, H, "BYTEBYTEGO · 04-01 §4",
          "1.6 GB 를 200 MB 파트 8개로 올리기",
          "파트마다 ETag 를 받아 두고, 끊긴 파트는 그 파트만 다시 보내며, 완료 요청이 번호와 ETag 목록으로 조립을 시킵니다",
          "uploadId · 파트 번호 · ETag")
C, S = "클라이언트", "객체 저장소"
d.lanes([(C, "1.6 GB 파일"), (S, "S3")], 100, 210)
d.rails(H - 80)

STR = 44
steps = [
    (C, S, "CreateMultipartUpload", MUTED, "ar", None),
    (S, C, "uploadId", MUTED, "ar", "5 4"),
    (C, S, "UploadPart 1 · 200 MB", MUTED, "ar", None),
    (S, C, "ETag 1", MUTED, "ar", "5 4"),
    (C, S, "UploadPart 2 · 200 MB", BAD, "bad", "5 4"),
    (C, S, "UploadPart 2 재전송 · 200 MB", ACC, "acc", None),
    (S, C, "ETag 2", MUTED, "ar", "5 4"),
    (C, S, "UploadPart 8 · 200 MB", MUTED, "ar", None),
    (S, C, "ETag 8", MUTED, "ar", "5 4"),
    (C, S, "CompleteMultipartUpload", INFO, "info", None),
    (S, C, "성공 · 객체 ETag", OK, "ok", "5 4"),
]
# 행 y: 기본 stride 44, 생략 표지(파트 3~7) 자리와 완료 요청 목록 자리에 간격을 더한다
ys, y = [], 196
for k in range(len(steps)):
    if k == 7:
        y += 44          # 생략 표지 한 칸
    if k == 10:
        y += 24          # 완료 요청이 싣는 목록 한 줄
    ys.append(y)
    y += STR
for (a, b, label, c, mk, dash), yy in zip(steps, ys):
    if mk == "bad":
        # 끊긴 요청은 상대 레인에 닿지 않고 도중에서 X 로 끝난다
        x1, x2 = d.LX[a], d.LX[b]
        xb = round((x1 + (x2 - x1) * 0.6) / 4) * 4
        d.path(f"M {x1 + 10} {yy} L {xb - 8} {yy}", c, 1.5, dash=dash)
        d.line(xb - 6, yy - 6, xb + 6, yy + 6, c, 1.8)
        d.line(xb - 6, yy + 6, xb + 6, yy - 6, c, 1.8)
        d.t((x1 + xb) / 2, yy - 9, label, 12, c, _kr(label), "middle", 600)
        continue
    d.msg(a, b, label, yy, c, mk, dash)

# 끊긴 메시지 위의 표지, 생략 표지, 완료 요청이 싣는 목록
cx = (d.LX[C] + d.LX[S]) / 2
d.chip(cx + 190, ys[4], "연결 끊김", BAD, 12)
d.t(cx, ys[6] + 40, "… 파트 3 ~ 7 도 같은 방식", 12, MUTED, KR, "middle")
d.t(cx, ys[9] + 22, "1→ETag 1 · 2→ETag 2 · … · 8→ETag 8", 12, INFO, MONO, "middle")

d.legend(H - 44, [("보냄", MUTED), ("끊김", BAD), ("재전송", ACC), ("완료 요청", INFO), ("성공 응답", OK)])
d.save("04-01.multipart-sequence.svg")
