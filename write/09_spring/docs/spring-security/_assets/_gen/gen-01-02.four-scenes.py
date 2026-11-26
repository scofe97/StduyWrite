# 사실 출처: Spring Security 7.1.1 SessionRegistryImpl·SecurityContextHolderFilter·SecurityContextLogoutHandler · Tomcat 11.0.24 StandardSession · 예제 앱 및 별도 JVM 관찰
# 타입 스펙: type-dp-security-matrix
# 공식(§2): left_pad 12 · comp_col_w 208 · gap 12 · role_col_w 148 · role_gap 16 · header_h 52. 셀이 두 줄이라 row_h 36→48, stride 40→56 으로 키웠다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

LEFT, COMP_W, GAP, ROLE_W, ROLE_GAP, RIGHT = 12, 208, 12, 148, 16, 48
HEADER_Y, HEADER_H = 100, 52
ROW0, ROW_H, STRIDE = 168, 48, 56
W = LEFT + COMP_W + GAP + 4 * ROLE_W + 3 * ROLE_GAP + RIGHT   # 920

roles = [
    ("1. 로그인", "…/auth/login"),
    ("2. 일반 요청", "/api/my/account"),
    ("3. 비밀번호 변경", "/api/my/password"),
    ("4. 로그아웃", "/api/my/logout"),
]
rows = [
    ("브라우저 쿠키", "JSESSIONID"),
    ("Tomcat 세션 맵", "sessions"),
    ("SessionRegistry", "장부"),
    ("SecurityContextHolder", "스레드"),
]
# (줄1, 줄2, 색)  색: OK 생성·기록 / INFO 읽기·갱신 / BAD 삭제·비움 / None 변화 없음 / ACC focal
cells = [
    [("새 ID 받음", "Set-Cookie", OK), ("ID 만 보냄", "Cookie 헤더", None), ("삭제 쿠키", "Expires 1970", BAD), ("삭제 쿠키", "Expires 1970", BAD)],
    [("세션 생성", "context 기록", OK), ("ID 로 찾기", "context 읽기", INFO), ("A 만 제거", "B 는 남음", BAD), ("세션 제거", "ID 키 삭제", BAD)],
    [("ID 등록", "expired=false", OK), ("시각 갱신", "lastRequest", INFO), ("전부 만료 표시", "expired=true", ACC), ("항목 삭제", "파기 이벤트", BAD)],
    [("직접 설정", "요청 끝에 비움", OK), ("세션에서 복원", "요청 끝에 비움", INFO), ("logout() 이 비움", "clearContext", BAD), ("logout() 이 비움", "clearContext", BAD)],
]

n_rows = len(rows)
rows_bottom = ROW0 + (n_rows - 1) * STRIDE + ROW_H
LEG_Y = rows_bottom + 28
H = LEG_Y + 56

d = D(
    W, H,
    "MATRIX · FOUR PLACES × FOUR SCENES",
    "네 장면에서 네 곳이 각각 하는 일",
    "비밀번호 변경에서 장부는 만료만 표시하고 Tomcat 은 지금 세션만 지운다",
    "로그인 · 일반 요청 · 비밀번호 변경 · 로그아웃"
)


def role_x(j):
    return LEFT + COMP_W + GAP + j * (ROLE_W + ROLE_GAP)


def row_y(k):
    return ROW0 + k * STRIDE


# 열 머리
for j, (nm, code) in enumerate(roles):
    x = role_x(j)
    d.box(x, HEADER_Y, ROLE_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(x + ROLE_W / 2, HEADER_Y + 22, nm, 12, INK, KR, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, code, 11, MUTED, MONO)

# 행 머리와 셀
for k, (nm, hint) in enumerate(rows):
    y = row_y(k)
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 1.0)
    d.t(LEFT + 12, y + 20, nm, 12, INK, KR if any("가" <= ch <= "힣" for ch in nm) else MONO, "start", 600)
    d.t(LEFT + 12, y + 38, hint, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in hint) else MONO, "start")
    for j, (l1, l2, c) in enumerate(cells[k]):
        x = role_x(j)
        if c == ACC:
            d.tone(x, y, ROLE_W, ROW_H, ACC, op="12", sw=1.4)
        elif c is None:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 1.0)
        else:
            d.tone(x, y, ROLE_W, ROW_H, c)
        d.t(x + ROLE_W / 2, y + 20, l1, 12, INK, KR if any("가" <= ch <= "힣" for ch in l1) else MONO, "middle", 600)
        d.t(x + ROLE_W / 2, y + 38, l2, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in l2) else MONO)

d.legend(LEG_Y, [
    ("만료 표시만 남김 (핵심)", ACC),
    ("생성 · 기록", OK),
    ("읽기 · 갱신", INFO),
    ("삭제 · 비움", BAD),
])

out_path = Path(__file__).parent.parent / "01-02.four-scenes.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
