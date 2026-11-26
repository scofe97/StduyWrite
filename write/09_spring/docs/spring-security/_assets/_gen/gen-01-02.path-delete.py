# 사실 출처: 임시 서버와 curl 쿠키 저장소 관찰 · RFC 6265 5.1.4·5.3
# 타입 스펙: type-dp-security-matrix
# 고른 이유: 같은 삭제 시도가 경로에 따라 갈리는 세 단계와 두 관측값을 경우 x 단계 격자로 비교한다.
# 공식(§2) 변형: left_pad 12 · gap 12 · role_gap 12 · header_h 52 · 두 줄 셀이라 row_h 48 / stride 56
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

LEFT, COMP_W, GAP, ROLE_W, ROLE_GAP, RIGHT = 12, 216, 12, 216, 12, 24
HEADER_Y, HEADER_H = 100, 52
ROW0, ROW_H, STRIDE = 168, 48, 56

roles = [('쿠키 저장소', 'curl -c 로 저장한 파일'), ('다음 요청의 Cookie 헤더', '서버가 받은 값'), ('판정', '원래 쿠키')]
rows = [('1. 로그인', 'Path=/ 쿠키를 받음'), ('2. 삭제 쿠키 Path=/api', '경로가 다른 삭제'), ('3. 삭제 쿠키 Path=/', '경로가 같은 삭제')]
# (줄1, 줄2, 색)  색: OK / INFO / WARN / BAD / None(중립) / ACC(focal)
cells = [[('path=/', 'JSESSIONID=abc123', OK), ('JSESSIONID=abc123', '쿠키가 실림', INFO), ('저장됨', '세션 유지', OK)], [('path=/', 'JSESSIONID=abc123', ACC), ('JSESSIONID=abc123', '그대로 실림', BAD), ('안 지워짐', '다른 쿠키로 봄', BAD)], [('(없음)', '항목 삭제', OK), ('(없음)', '쿠키 안 실림', OK), ('지워짐', '이름·도메인·경로 같음', OK)]]

W = LEFT + COMP_W + GAP + len(roles) * ROLE_W + (len(roles) - 1) * ROLE_GAP + RIGHT
n_rows = len(rows)
rows_bottom = ROW0 + (n_rows - 1) * STRIDE + ROW_H
LEG_Y = rows_bottom + 28
H = LEG_Y + 56

d = D(W, H, 'MATRIX · COOKIE DELETE BY PATH', '삭제 쿠키의 경로에 따라 지워지거나 남는 쿠키', 'Path=/ 로 심은 세션 쿠키를 Path=/api 삭제 쿠키는 지우지 못하고 Path=/ 삭제 쿠키는 지운다', 'curl 의 쿠키 저장소로 관찰 · 브라우저도 RFC 6265 의 같은 식별 규칙을 따름')


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

d.legend(LEG_Y, [('경로 틀림: 안 지워짐 (핵심)', ACC), ('정상', OK), ('쿠키 실림', INFO), ('실패', BAD)])

out_path = Path(__file__).parent.parent / '01-02.path-delete.svg'
d.save(str(out_path))
print(f"생성 완료: {out_path}")
