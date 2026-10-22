# 타입 스펙: type-line — 슬로프그래프(2017년판 순위 → 2025년판 순위). 순위는 크게 흔들렸지만 책의 열 절 가운데 일곱은 이름이 이어지고 셋은 다른 범주에 흡수됐다(XXE → 보안 설정 오류, XSS → 인젝션, 역직렬화 → 무결성 실패). focal 은 알려진 취약점 컴포넌트 → A03 공급망(9위에서 3위로).
# 사실 출처: 노트 L172~L203(2025 목록·개명·신규·빠짐·흡수) + 책 밖 OWASP 1차 자료: 2017 순위 A1~A10 owasp.org/www-project-top-ten/2017/Top_10, 민감정보 → 암호화 실패 개명 owasp.org/Top10/2021/A02_2021-Cryptographic_Failures/, XSS(CWE-79) 인젝션 포함 owasp.org/Top10/2025/A05_2025-Injection/, XXE(CWE-611) 보안 설정 오류 포함 owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/ (모두 2026-10-22 조회)
# Layout conventions: 두 축 x=296·664, 순위 stride 40(y=140+40(r-1)), 왼쪽 이름은 x=256 오른쪽 정렬·순위 x=284, 오른쪽 순위 x=676·이름 x=712. 두 축은 같은 순위 눈금(1~10)을 공유한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 584
d = D(W, H, "CONTAINER SECURITY · 14-01 ADDENDUM",
      "책이 기준한 2017년판 열 가지는 2025년판에서 순위가 흔들리고 일부는 흡수됐다",
      "접근 통제는 1위로, 알려진 취약점 컴포넌트는 3위 공급망 실패로 올라왔고 XML 외부 엔티티는 보안 설정 오류에 흡수됐다.",
      "2017년판 순위에서 2025년판 순위로 잇는 슬로프그래프")

AX1, AX2 = 296, 664
Y0, STRIDE = 140, 40
def y(rank): return Y0 + (rank - 1) * STRIDE

# 왼쪽(2017): 순위, 책의 절 이름
LEFT = {1: "인젝션", 2: "인증 취약", 3: "민감정보 노출", 4: "XML 외부 엔티티", 5: "접근 통제 취약",
        6: "보안 설정 오류", 7: "크로스 사이트 스크립팅", 8: "안전하지 않은 역직렬화",
        9: "알려진 취약점 컴포넌트", 10: "로깅·모니터링 부족"}
# 오른쪽(2025): 순위, 이름, 꼬리표
RIGHT = {1: ("접근 통제 취약", ""), 2: ("보안 설정 오류", "XXE 흡수"), 3: ("소프트웨어 공급망 실패", "컴포넌트 범주 확장"),
         4: ("암호화 실패", "민감정보 노출에서 개명"), 5: ("인젝션", "XSS 포함"),
         6: ("안전하지 않은 설계", "책에 대응 절 없음"), 7: ("인증 실패", "식별·인증 실패에서 개명"),
         8: ("소프트웨어·데이터 무결성 실패", "역직렬화 흡수"), 9: ("보안 로깅·경보 실패", "로깅·모니터링에서 개명"),
         10: ("예외 상황 오처리", "완전 신규")}
# (왼쪽 순위, 오른쪽 순위, 색, focal) — 색: ok 이름 유지 · warn 개명 · info 흡수·확장
LINKS = [(1, 5, OK, False), (2, 7, WARN, False), (3, 4, WARN, False), (5, 1, OK, False), (6, 2, OK, False), (4, 2, INFO, False),
         (7, 5, INFO, False), (8, 8, INFO, False), (9, 3, ACC, True), (10, 9, WARN, False)]
RIGHT_COLOR = {r: c for _, r, c, _ in LINKS}
RIGHT_COLOR.update({6: MUTED, 10: MUTED})

# 축과 상태 캡션
for x, cap in ((AX1, "2017년판 · 책이 기준한 판"), (AX2, "2025년판 · 현재 최신")):
    d.line(x, 116, x, y(10) + 20, RULE, 1.0)
    d.t(x, 108, cap, 13, MUTED, KR, "middle", 600)

# 선과 끝점
for l, r, c, focal in LINKS:
    d.line(AX1, y(l), AX2, y(r), c, 2.4 if focal else 1.6)
for l, r, c, focal in LINKS:
    rad = 4 if focal else 3
    d.o.append(f'<circle cx="{AX1}" cy="{y(l)}" r="{rad}" fill="{c}"/>')
    d.o.append(f'<circle cx="{AX2}" cy="{y(r)}" r="{rad}" fill="{c}"/>')

# 왼쪽 라벨: 이름 + 순위
link_color_left = {l: c for l, _, c, _ in LINKS}
for rk, name in LEFT.items():
    c = link_color_left[rk]
    d.t(256, y(rk) + 5, name, 13, INK, KR, "end", 600 if c == ACC else 500)
    d.t(284, y(rk) + 4, f"A{rk}", 12, MUTED, MONO, "end")

# 오른쪽 라벨: 순위 + 이름 + 꼬리표
for rk, (name, tag) in RIGHT.items():
    c = RIGHT_COLOR[rk]
    d.t(676, y(rk) + 4, f"A{rk:02d}", 12, MUTED, MONO, "start")
    if tag:
        d.t(712, y(rk) - 1, name, 13, INK, KR, "start", 600 if c == ACC else 500)
        d.t(712, y(rk) + 15, tag, 13, c if c != MUTED else MUTED, KR, "start")
    else:
        d.t(712, y(rk) + 5, name, 13, INK, KR, "start", 500)

d.legend(H - 56, [("이름 유지", OK), ("개명", WARN), ("흡수·확장", INFO), ("가장 큰 상승", ACC)])
d.save("14-01.owasp-2017-vs-2025.svg")
