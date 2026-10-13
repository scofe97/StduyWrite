# 타입 스펙: type-dp-security-matrix — HTTP 4개 버전 × 연결·다중화·막힘 범위·헤더 압축의 비교 격자(격자 문법을 비교 행렬로 사용). 초점 칸 하나는 HTTP/2 가 풀지 못한 TCP 계층의 막힘.
# 사실 출처: RFC 1945 §1.3(요청마다 연결 설정·응답 뒤 서버가 닫음, 1996-05), RFC 9112 §9.3(지속 연결 기본)·§9.4(연결 수 상한은 숫자 없음), RFC 9113 §1(HTTP/1.1 파이프라인의 응용 계층 HOL·HTTP/2 의 TCP HOL 미해결)·§3.2(ALPN h2),
#   RFC 9112 §9.3.2(파이프라인 응답은 요청 순서대로)·RFC 9113 §4.3.1(필드 압축은 상태를 가짐)·RFC 9114 §2(QUIC 스트림 독립·QPACK 이 HPACK 대체)·§3.1, RFC 9000 §13(한 패킷에 여러 스트림이 실리면 함께 막힘), RFC 2068(1997-01)·RFC 7540(2015-05) 머리 날짜.
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 164, role_col_w 152, role_col_gap 8, header_h 52, header_y 96, row_h 52 · stride 56(셀이 두 줄이라 44→52). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, ROLE_W, ROLE_GAP, HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 12, 164, 12, 152, 8, 96, 52, 164, 52, 56
roles = [("전송", "아래 계층"), ("연결 사용", "요청을 싣는 법"), ("요청 다중화", "한 연결 안에서"), ("막힘이 남는 곳", "HOL 범위"), ("헤더 표현", "필드 압축")]
rows = [
    ("HTTP/1.0", "RFC 1945 · 1996-05"),
    ("HTTP/1.1", "RFC 9112 (최초 2068)"),
    ("HTTP/2", "RFC 9113 (최초 7540)"),
    ("HTTP/3", "RFC 9114 · 2022-06"),
]
# 셀: (첫 줄, 둘째 줄, 상태색) — 상태색은 막힘이 남는 열에만 둔다.
cells = [
    [("TCP", "", None), ("요청마다 새 연결", "응답 뒤 서버가 닫음", None), ("없음", "요청 하나씩", None), ("연결당 요청 하나", "다음 요청은 새 연결", BAD), ("텍스트", "", None)],
    [("TCP", "", None), ("지속 연결이 기본", "여러 요청이 연결 재사용", None), ("파이프라인 일부", "응답은 요청 순서대로", None), ("응용 계층", "앞 응답이 뒤를 막음", WARN), ("텍스트", "", None)],
    [("TCP", "", None), ("연결 하나로 충분", "ALPN h2 로 협상", None), ("스트림 인터리빙", "응답 순서 무관", None), ("TCP 계층", "손실 하나가 전체를 막음", ACC), ("HPACK", "상태 있는 압축", None)],
    [("QUIC · UDP", "TLS 1.3 포함", None), ("QUIC 연결 하나", "Alt-Svc 로 발견", None), ("QUIC 스트림", "스트림마다 독립", None), ("같은 패킷의 스트림", "다른 스트림은 진행", OK), ("QPACK", "순서 의존을 없앰", None)],
]
FOCAL = (2, 3)

W = LEFT + COMP_W + GAP0 + 5 * ROLE_W + 4 * ROLE_GAP + 20
H = ROW0 + 3 * STRIDE + ROW_H + 24 + 44
d = D(W, H, "BYTEBYTEGO · 03-01 §4",
      "HTTP 버전마다 연결 하나에서 막히는 범위가 좁아진다",
      "아래로 갈수록 한 연결에 실리는 요청이 서로를 막는 범위가 줄고 HTTP/2 에서 TCP 계층이 남습니다",
      "RFC 1945 · 9112 · 9113 · 9114 · 9000")

d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 22, "버전", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HDR_Y + 40, "× 속성", 13, MUTED, KR)


def rx(j):
    return LEFT + COMP_W + GAP0 + j * (ROLE_W + ROLE_GAP)


for j, (nm, sub) in enumerate(roles):
    d.box(rx(j), HDR_Y, ROLE_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 22, nm, 13, INK, KR, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 40, sub, 13, MUTED, KR)

for i, (name, hint) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT + 12, y + 22, name, 13, INK, MONO, "start", 600)
    d.t(LEFT + 12, y + 40, hint, 13, MUTED, KR, "start")
    for j in range(5):
        l1, l2, c = cells[i][j]
        x = rx(j)
        fam1 = KR if any("가" <= ch <= "힣" for ch in l1) else MONO
        if (i, j) == FOCAL:
            d.tone(x, y, ROLE_W, ROW_H, ACC, 4, "14", 1.4)
            col = ACC
        elif c:
            d.tone(x, y, ROLE_W, ROW_H, c, 4, "10", 0.9)
            col = c
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.8, 4)
            col = INK
        if l2:
            d.t(x + ROLE_W / 2, y + 22, l1, 13, col, fam1, "middle", 600)
            d.t(x + ROLE_W / 2, y + 40, l2, 13, MUTED if col == INK else col, KR, "middle")
        else:
            d.t(x + ROLE_W / 2, y + 31, l1, 13, col, fam1, "middle", 600)

d.legend(H - 44, [("막힘 범위가 넓음", BAD), ("부분적", WARN), ("좁음", OK), ("HTTP/2 가 남긴 막힘", ACC)])
d.save("03-01.http-matrix.svg")
