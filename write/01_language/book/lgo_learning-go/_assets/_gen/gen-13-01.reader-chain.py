# 13-01.reader-chain — 문자열도 gzip 파일도 io.Reader 로 감싸 countLetters 하나가 읽는다
# 본문 요구(13-01 §2): strings.NewReader 로 만든 *strings.Reader 와, os.Open 한 *os.File 을 gzip.NewReader 로 감싼
#           *gzip.Reader 가 모두 io.Reader 라서 countLetters 가 코드 변경 없이 읽는다. 정리는 buildGZipReader 가 돌려준 클로저가 한다.
# 타입 스펙: type-architecture — 두 입력 줄(문자열 · 파일)이 오른쪽 countLetters 하나로 모인다. 직교 화살표만 쓴다.
#           열 x = 24 · 290 · 556 · 800, 노드 폭 150(마지막 170), 높이 64, 줄 y = 140 · 284. focal 은 gzip.NewReader 화살표 하나.
# 사실 출처: Learning Go 2판 13장 「io and Friends」, 원서 예제 저장소 ch13 sample_code/io_friends 를 go1.25.1 로 실행 —
#           같은 문장을 gzip 으로 압축한 파일을 만들어 문자열 판과 같은 map 이 나옴(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 992, 500
d = D(W, H, "ARCHITECTURE · 13-01 §2",
      "파일을 gzip 리더로 감싸도 countLetters 는 io.Reader 만 봅니다",
      "위 줄은 문자열 s 를 strings.NewReader 로 감싼 *strings.Reader, 아래 줄은 my_data.txt.gz 를 os.Open 한 *os.File 을 gzip.NewReader 로 다시 감싼 *gzip.Reader 다. "
      "둘 다 io.Reader 라서 countLetters(r io.Reader) 하나가 같은 코드로 영어 글자 수를 센다. 아래 줄의 정리는 buildGZipReader 가 돌려준 클로저가 gr 과 r 을 차례로 닫아 맡는다.",
      lead="상자 아래 글자는 그 값이 만족하는 인터페이스입니다.")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, w, title, sub, c=None, h=64):
    if c:
        d.tone(x, y, w, h, c, 6, "14", 1.1)
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + 28, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + w / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")


X = (24, 290, 556, 800)
NW = 150
Y1, Y2 = 140, 284

# 위 줄: 문자열 → strings.Reader
d.arrow([(X[0] + NW + 2, Y1 + 32), (X[2] - 4, Y1 + 32)], SOFT, "soft", 1.3)
d.t((X[0] + NW + X[2]) / 2, Y1 + 23, "strings.NewReader", 11, MUTED, MONO, "middle", 600)
# 아래 줄: 파일 → os.File → gzip.Reader
d.arrow([(X[0] + NW + 2, Y2 + 32), (X[1] - 4, Y2 + 32)], SOFT, "soft", 1.3)
d.t((X[0] + NW + X[1]) / 2, Y2 + 23, "os.Open", 11, MUTED, MONO, "middle", 600)
d.arrow([(X[1] + NW + 2, Y2 + 32), (X[2] - 4, Y2 + 32)], ACC, "acc", 1.6)
d.t((X[1] + NW + X[2]) / 2, Y2 + 23, "gzip.NewReader", 11, ACC, MONO, "middle", 600)
# 두 줄이 countLetters 로 모임
jx = X[2] + NW + 47
cy = (Y1 + Y2) / 2 + 32
d.line(X[2] + NW + 2, Y1 + 32, jx, Y1 + 32, SOFT, 1.3)
d.line(X[2] + NW + 2, Y2 + 32, jx, Y2 + 32, SOFT, 1.3)
d.line(jx, Y1 + 32, jx, Y2 + 32, SOFT, 1.3)
d.arrow([(jx, cy), (X[3] - 4, cy)], SOFT, "soft", 1.3)

node(X[0], Y1, NW, "문자열 s", "The quick brown…")
node(X[2], Y1, NW, "*strings.Reader", "io.Reader", INFO)
node(X[0], Y2, NW, "my_data.txt.gz", "디스크의 파일")
node(X[1], Y2, NW, "*os.File", "Reader · Closer", INFO)
node(X[2], Y2, NW, "*gzip.Reader", "Reader · Closer", INFO)
node(X[3], cy - 32, 170, "countLetters(r)", "r io.Reader 만 받음", OK)

d.path(f"M {X[1] + NW / 2} {Y2 + 66} L {X[1] + NW / 2} 392 L {X[2] + NW / 2} 392 L {X[2] + NW / 2} {Y2 + 70}", MUTED, 1.1, dash="4 4")
d.t((X[1] + X[2] + NW) / 2, 412, "defer closer() · gr.Close() 다음 r.Close()", 11, MUTED, MONO, "middle", 600)

d.legend(440, [("io.Reader 구현", INFO), ("감싸는 데코레이터", ACC), ("같은 코드로 읽는 함수", OK)])
d.save("13-01.reader-chain.svg")
print("ok 13-01 chain")
