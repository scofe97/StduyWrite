# 타입 스펙: type-process — 40 MB 파일이 4 MB 블록 1~10 으로 쪼개지고, 수정된 블록 2·5 만 해시가 바뀌어 압축·암호화를 거쳐 올라간다. 칸마다 블록 번호와 해시가 실제 값이다.
# 사실 출처: 추출본 v2.txt 4525~4530행(블록 최대 4 MB·블록마다 고유 해시를 메타데이터 DB 에 둔다)·4561~4577행(블록 분할 → 압축 → 암호화 → 업로드, 수정된 블록 2·5 만 전송).
#   해시는 `block-NN-v1`·`block-02-v2`·`block-05-v2` 문자열의 SHA-256 앞 6자리이며 설명용 값이다. Dropbox 콘텐츠 해시가 4 MB(4,194,304 B) 블록마다 SHA-256 을 구한다: https://docs.dropboxapi.com/dropbox-api/docs/technical-reference/content-hash
#   계산: 4 MB × 10 = 40 MB · 4 MB × 2 = 8 MB.
# Layout conventions: 블록 폭 84·높이 72, x stride 92(24부터), 줄 y=120·240, 업로드 상자 y=360 높이 64. 모든 좌표 4의 배수.
import hashlib
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, SOFT, KR, MONO

W, H = 1000, 504
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 15-01 §5",
      "블록 열 개 중 2 번과 5 번만 올라간다",
      "블록마다 해시가 있어 같은 해시는 건너뛰고, 달라진 블록만 압축하고 암호화해 올린다. 40 MB 가 8 MB 로 줄어든다.",
      "해시 6 자리는 설명용 값")

BW, BH, ST, X0 = 84, 72, 92, 24
CHANGED = (2, 5)


def h6(s):
    return hashlib.sha256(s.encode()).hexdigest()[:6]


def blk(x, y, n, hv, c, tone=True):
    if tone:
        d.tone(x, y, BW, BH, c, 6, "14", 1.2)
    else:
        d.box(x, y, BW, BH, "#161B22", "rgba(191,192,192,0.22)", 1.0)
    d.t(x + BW // 2, y + 30, f"블록 {n}", 14, INK, KR, "middle", 600)
    d.t(x + BW // 2, y + 54, hv, 13, MUTED, MONO)


d.t(24, 108, "버전 1 · 4 MB × 10 = 40 MB", 13, SOFT, KR, "start", 600)
d.t(24, 228, "버전 2 · 블록 2 와 5 수정", 13, SOFT, KR, "start", 600)
for n in range(1, 11):
    x = X0 + (n - 1) * ST
    h1 = h6(f"block-{n:02d}-v1")
    blk(x, 120, n, h1, INFO)
    if n in CHANGED:
        blk(x, 240, n, h6(f"block-{n:02d}-v2"), WARN)
    else:
        blk(x, 240, n, h1, OK)

UX, UW, UY, UH = 100, 420, 360, 64
for n in CHANGED:
    cx = X0 + (n - 1) * ST + BW // 2
    d.arrow([(cx, 240 + BH + 4), (cx, UY - 4)], WARN, "warn", 1.5)
d.tone(UX, UY, UW, UH, ACC, 6, "12", 1.4)
d.t(UX + UW // 2, UY + 28, "업로드 블록 2 · 5", 15, INK, KR, "middle", 600)
d.t(UX + UW // 2, UY + 50, "8 MB (건너뜀 블록 8 개)", 13, MUTED, KR)
d.arrow([(UX + UW + 4, UY + UH // 2), (572, UY + UH // 2)], MUTED, "ar", 1.5)
d.box(576, UY, 360, UH, "#161B22", "rgba(191,192,192,0.22)", 1.0)
d.t(756, UY + 28, "압축 → 암호화", 15, INK, KR, "middle", 600)
d.t(756, UY + 50, "클라우드 저장소", 13, MUTED, KR)

d.legend(H - 56, [("원 버전", INFO), ("해시 같음", OK), ("해시 달라짐", WARN), ("업로드 대상", ACC)])
d.save("15-01.block-delta.svg")
