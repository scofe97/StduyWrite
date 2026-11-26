# 사실 출처: Spring Security 7.1.1 CookieCsrfTokenRepository · 예제 앱 로그인 POST 관찰 · 세션 저장소 쪽은 구조에서 따라 나온 추론
# 타입 스펙: type-dp-security-matrix
# 고른 이유: 저장소 두 종류가 세션 무효화 전후 시점에서 어떻게 다른지 경우 x 시점 격자로 비교한다.
# 공식(§2) 변형: left_pad 16 · gap 12 · role_gap 12 · header_h 52 · 두 줄 셀이라 row_h 48 / stride 56
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

LEFT, COMP_W, GAP, ROLE_W, ROLE_GAP, RIGHT = 16, 188, 12, 172, 12, 20
HEADER_Y, HEADER_H = 100, 52
ROW0, ROW_H, STRIDE = 168, 48, 56

roles = [
    ('로그인 전', '토큰 발급'),
    ('비밀번호 변경 뒤', '세션만 무효화'),
    ('로그아웃 뒤', '쿠키 삭제 후 재발급'),
    ('로그인 POST', '새 비밀번호로 로그인'),
]
rows = [('쿠키 저장소', '현재 설정 · XSRF-TOKEN'), ('세션 저장소', '가정 · 세션 속성')]
# (줄1, 줄2, 색)  색: OK / INFO / WARN / BAD / None(중립) / ACC(focal)
cells = [
    [
        ('쿠키에 토큰', '브라우저가 보관', INFO),
        ('쿠키 그대로', '세션 무효화만 수행', OK),
        ('쿠키도 삭제됨', '401 응답이 새 토큰 발급', OK),
        ('쿠키 = 헤더', '200 통과 (실측)', ACC),
    ],
    [
        ('세션 속성에 토큰', '서버 메모리', INFO),
        ('토큰도 사라짐', '세션과 함께 파기', BAD),
        ('토큰도 사라짐', '세션과 함께 파기', BAD),
        ('비교 대상 없음', '403 (추론)', BAD),
    ],
]

W = LEFT + COMP_W + GAP + len(roles) * ROLE_W + (len(roles) - 1) * ROLE_GAP + RIGHT
n_rows = len(rows)
rows_bottom = ROW0 + (n_rows - 1) * STRIDE + ROW_H
LEG_Y = rows_bottom + 28
H = LEG_Y + 56

d = D(
    W, H,
    'MATRIX · CSRF TOKEN STORE',
    'CSRF 토큰을 어디에 두느냐에 따른 세션 무효화 뒤의 차이',
    '토큰이 쿠키에 있으면 세션이 사라져도 첫 로그인 POST 가 통과하고 세션 속성에 있었다면 403 이 되었을 것이다',
    '세션 저장소 행의 결과는 소스 구조에서 따라 나온 추론'
)


def is_kr(t):
    return any("가" <= ch <= "힣" for ch in t)


def role_x(j):
    return LEFT + COMP_W + GAP + j * (ROLE_W + ROLE_GAP)


for j, (nm, code) in enumerate(roles):
    x = role_x(j)
    d.box(x, HEADER_Y, ROLE_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(x + ROLE_W / 2, HEADER_Y + 22, nm, 12, INK, KR if is_kr(nm) else MONO, "middle", 600)
    d.t(x + ROLE_W / 2, HEADER_Y + 40, code, 12, MUTED, KR if is_kr(code) else MONO)

for k, (nm, hint) in enumerate(rows):
    y = ROW0 + k * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 1.0)
    d.t(LEFT + 12, y + 20, nm, 12, INK, KR if is_kr(nm) else MONO, "start", 600)
    d.t(LEFT + 12, y + 38, hint, 12, MUTED, KR if is_kr(hint) else MONO, "start")
    for j, (l1, l2, c) in enumerate(cells[k]):
        x = role_x(j)
        if c == ACC:
            d.tone(x, y, ROLE_W, ROW_H, ACC, op="12", sw=1.4)
        elif c is None:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 1.0)
        else:
            d.tone(x, y, ROLE_W, ROW_H, c)
        d.t(x + ROLE_W / 2, y + 20, l1, 12, INK, KR if is_kr(l1) else MONO, "middle", 600)
        d.t(x + ROLE_W / 2, y + 38, l2, 12, MUTED, KR if is_kr(l2) else MONO)

d.legend(LEG_Y, [('현재 설정이 통과하는 지점 (핵심)', ACC), ('보관', INFO), ('유효 상태', OK), ('실패 (추론)', BAD)])

out_path = Path(__file__).parent.parent / '01-02.csrf-store.svg'
d.save(str(out_path))
print(f"생성 완료: {out_path}")
