# 타입 스펙: type-data-flow — 파이프라인 단계마다 누가 무엇을 하는지. 데이터 상자(분석 로그·집계 데이터·Trie DB·Trie 캐시)와 일하는 상자(집계기·작업자)가 번갈아 서고, 상자 안에 실제 행을 싣는다. focal 은 작업자.
# 사실 출처: 추출본 v2.txt 3730~3760행(분석 로그 · 집계기 · 집계 데이터 · 작업자 · Trie 캐시 · Trie DB 의 문서 저장소와 키-값 저장소 두 안) · PDF 211~213쪽 그림 13-9·13-10과 표 13-3·13-4.
#   로그 여섯 행(tree 10-01 22:01:01 · try 10-01 22:01:05 · tree 10-01 22:01:30 · toy 10-01 22:02:22 · tree 10-02 22:02:42 · try 10-03 22:03:03)은 표 13-3 이다.
#   집계 결과 tree 3 · try 2 · toy 1 은 위 여섯 행을 2019-10-01 로 시작하는 한 주(10-01~10-07)로 센 값이고 표 13-4 의 12000 같은 값과는 별개 예시다(본문도 그 표를 별개 예시라고 밝힌다). 칸 이름 query · time · frequency 는 표 13-4 와 같다.
#   Trie DB 행은 집계 결과 셋으로 만든 접두사 키 → 상위 목록이며 키-값 안의 대응(접두사 → 목록)은 PDF 213쪽 그림 13-10 을 따른다.
# Layout conventions: 상자 x = 24·224·368·600·744, y = 116(로그)·140(데이터·DB)·174(집계기·작업자). 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, SOFT, KR, MONO

W, H = 1000, 480
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §5",
      "로그 여섯 줄이 주 단위 집계 세 줄이 되고 작업자가 트라이로 다시 만든다",
      "분석 로그를 한 주 단위로 합산해 작업자가 트라이를 세우고 Trie DB 에 쓰며, Trie 캐시는 그 DB 를 주 1회 스냅샷으로 읽는다.",
      "2019-10-01 로 시작하는 한 주 · 질의 tree · try · toy")


def data_box(x, y, w, h, title, sub, rows, c, size=13):
    d.tone(x, y, w, h, c, 6, "10", 1.1)
    d.t(x + 14, y + 26, title, 14, INK, KR, "start", 600)
    if sub:
        d.t(x + 14, y + 46, sub, 12, SOFT, MONO, "start")
    y0 = y + (70 if sub else 54)
    for i, r in enumerate(rows):
        d.t(x + 14, y0 + i * 24, r, size, MUTED, MONO, "start")


def work_box(x, y, w, h, title, chip, c, focal=False):
    d.tone(x, y, w, h, ACC if focal else c, 6, "12", 1.4 if focal else 1.0)
    d.t(x + w / 2, y + 30, title, 14, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 54, chip, 13, MUTED, KR, "middle")


LOG = ("tree · 10-01", "try · 10-01", "tree · 10-01", "toy · 10-01", "tree · 10-02", "try · 10-03")
data_box(24, 116, 168, 188, "분석 로그", None, LOG, INFO)
work_box(224, 174, 112, 72, "집계기", "주 단위 합산", OK)
data_box(368, 140, 200, 136, "집계 데이터", "query · time · frequency",
         ("tree · 10-01 · 3", "try · 10-01 · 2", "toy · 10-01 · 1"), INFO)
work_box(600, 174, 112, 72, "작업자", "트라이 재구축", OK, focal=True)
data_box(744, 140, 232, 136, "Trie DB", "key → value",
         ("t → tree 3 · try 2 · toy 1", "tr → tree 3 · try 2", "to → toy 1"), INFO, 12)
data_box(744, 332, 232, 84, "Trie 캐시", None, ("tr → tree 3 · try 2",), INFO, 12)

for a, b in ((192, 224), (336, 368), (568, 600), (712, 744)):
    d.arrow([(a + 2, 208), (b - 6, 208)], MUTED, "ar", 1.5)
d.arrow([(860, 280), (860, 328)], MUTED, "ar", 1.5)
d.t(876, 308, "주 1회 스냅샷", 13, MUTED, KR, "start")

d.legend(H - 56, [("저장된 데이터", INFO), ("일하는 서버", OK), ("주기마다 도는 서버", ACC)])
d.save("13-01.collection-pipeline.svg")
