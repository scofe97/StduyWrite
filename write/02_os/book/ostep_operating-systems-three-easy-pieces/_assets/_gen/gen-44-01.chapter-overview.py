# 44-01 개념도 — 앞 도구가 남긴 문제가 다음 도구를 부르는 사슬. 키의 비밀 → 대칭 암호 → 키 건네기 → 공개 키 암호 → 느림·키 주인 → 암호 해시 → 해시만 서명.
# 본문 근거: 이 노트 「핵심 요약」과 「1. 알고리즘은 공개하고 키만 숨기는 대칭 암호」·「2. 개인 키 서명과 공개 키 암호화」·「3. 해시만 서명하는 값싼 무결성 확인」.
# 타입 스펙: type-process — 고른 이유: 이 편의 줄기는 도구 하나가 풀고 남긴 문제가 다음 도구를 부르는 순서 있는 사슬이다.
#             단계마다 한 칸씩 내려가는 계단으로 놓으면 「남는 문제 → 다음 도구」 가 한눈에 보인다. 절마다 한 행인 옛 격자(열 x = 60 + j·340)는 쓰지 않는다.
#             스펙에 계단 전용 공식은 없어 좌표는 열 stride 258, 행 stride 112 로 직접 잡았다.
# 공식 근거: NIST FIPS 197(AES), SP 800-38D(GCM), SP 800-131A Rev. 2(SHA-1·RSA), NIST 해시 함수 정책.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, KR, MONO

W, H = 1000, 630
NW, NH = 154, 72
COLS = (24, 282, 540, 798)
ROWS = (132, 244, 356, 468)


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "OSTEP · 44-01 OVERVIEW",
      "보호는 키의 비밀에서 나오고, 도구가 남긴 문제가 다음 도구를 부른다",
      "44-01 의 키워드 개념도. 위에서 아래로 한 단씩 내려가며 읽는다. 출발점은 알고리즘을 공개하고 키 하나에만 비밀을 두는 것이다. "
      "대칭 암호는 빠르지만 키를 건네는 일이 남고, 공개 키 암호가 키를 둘로 나눠 그 문제를 푼다. "
      "공개 키 암호는 훨씬 느리고 공개 키가 정말 그 사람의 것인지가 남는다. 암호 해시는 지문만 서명해 서명 비용을 줄이고 변조를 알아챈다.",
      lead="초록이 쓰는 도구, 파랑이 남는 문제이고 화살표에 붙은 글자가 둘의 관계입니다. 점선은 뒤 편으로 넘기는 예고입니다.")


def node(col, row, title, sub, c, sec):
    x, y = COLS[col], ROWS[row]
    d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c if c != MUTED else MUTED, 11)
    d.t(x + NW / 2, y + 40, title, 14, c if c != INFO else INFO, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")


def harrow(col, row, label, c=INFO, m="info", dash=None):
    y = ROWS[row] + NH / 2
    x1, x2 = COLS[col] + NW, COLS[col + 1]
    d.arrow([(x1 + 3, y), (x2 - 4, y)], c, m, 1.4, dash)
    d.t((x1 + x2) / 2, y - 9, label, 13, MUTED, kr(label), "middle", 600)


def varrow(col, row, label, c=INFO, m="info"):
    x = COLS[col] + NW / 2
    y1 = ROWS[row] + NH
    y2 = ROWS[row + 1]
    d.arrow([(x, y1 + 3), (x, y2 - 4)], c, m, 1.4)
    d.t(x + 10, (y1 + y2) / 2 + 4, label, 13, MUTED, kr(label), "start", 600)


# 출발 — 이 편이 고르는 한 줄
node(0, 0, "비밀은 키 하나에만", "알고리즘은 공개 표준", ACC, "§1")
varrow(0, 0, "보호를 키에 걸고", ACC, "acc")

# 첫 단 — 대칭 암호
node(0, 1, "대칭 암호", "같은 키로 잠그고 연다", OK, "§1")
varrow(0, 1, "남는 문제", INFO, "info")
node(0, 2, "키를 건네는 일", "몰래 전달하고 관리", INFO, "§2")
harrow(0, 2, "키를 둘로 나눠", OK, "ok")

# 둘째 단 — 공개 키 암호
node(1, 2, "공개 키 암호", "공개 키 + 개인 키", OK, "§2")
varrow(1, 2, "남는 문제", INFO, "info")
node(1, 3, "훨씬 느리다", "대칭 암호보다 수백 배", INFO, "§2")
harrow(1, 2, "남는 문제", INFO, "info")
node(2, 2, "공개 키 확인", "정말 그 사람의 것인지", INFO, "§2")
harrow(2, 2, "뒤 편으로", SOFT, "soft", "4 3")
node(3, 2, "인증서 편", "서명을 확인하는 흐름", MUTED, "§2")

# 셋째 단 — 암호 해시
harrow(1, 3, "비용을 줄이려", OK, "ok")
node(2, 3, "암호 해시", "키 없는 고정 길이 지문", OK, "§3")
harrow(2, 3, "지문만 서명해", OK, "ok")
node(3, 3, "해시만 서명", "변조를 알아챌 수 있다", OK, "§3")

d.legend(H - 40, [("이 편이 고르는 한 줄", ACC), ("쓰는 도구", OK), ("남는 문제", INFO), ("뒤 편 예고", MUTED)])
d.save("44-01.chapter-overview.svg")
print("ok 44-01 overview")
