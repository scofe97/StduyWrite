# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: Coding for SSDs 2부·3부(https://codecapsule.com/2014/02/12/coding-for-ssds-part-2-architecture-of-an-ssd-and-benchmarking/ — page 2~16 KB · block 128·256 page 는 일반값, program 250 µs 는 SLC 열)
#   · 추출본 v1.txt 2131~2170행(4+2 이레이저 코딩, 저장 오버헤드 50% 대 200%) · 1790~1830행(8 파트 × 200 MB 의 멀티파트 업로드)
#   · AWS S3 사용자 가이드 "Amazon S3 multipart upload limits"(파트 10,000개 · 5 MiB~5 GiB). 1.5× = 6 조각 / 4 조각, 3× = 복사본 세 벌.
# Layout conventions: 카드 폭 204·높이 212, 가로 stride 224(x=40+224k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 04-01",
      "큰 데이터를 싸고 안전하게 담는 네 장치",
      "플래시의 병렬 쓰기, 접근 단위가 다른 세 저장소, 조각과 패리티, 파트 업로드가 이어집니다.",
      "네 절이 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 204, 212, 224, 40, 112
cards = [
    ("§1", "SSD 가 빠른 이유", "page 2~16 KB", "block 128·256 page", "채널 4개 → 250 µs (SLC)", INFO),
    ("§2", "블록 · 파일 · 객체", "LBA · 경로 · 키", "객체는 통째로 교체", "접근 단위의 차이", INFO),
    ("§3", "이레이저 코딩", "4+2 → 1.5배", "3 복제 → 3배", "조각 둘을 잃어도 복원", ACC),
    ("§4", "분할 업로드", "8 파트 × 200 MB", "실패한 파트만 재전송", "uploadId · ETag 로 조립", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, KR, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("04-01.chapter-overview.svg")
