# 사실 출처: Spring Security 7.1.1 SessionRegistryImpl L103-L107·L149-L165·ConcurrentSessionFilter L140-L146 · 별도 JVM 관찰
# 타입 스펙: type-dp-security-matrix
# 고른 이유: 같은 두 세션이 비밀번호 변경 뒤 네 시점에서 장부와 Tomcat 맵에 남는 모습을 시점 x 저장소 격자로 보인다.
# 공식(§2) 변형: left_pad 12 · gap 12 · role_gap 12 · header_h 52 · 두 줄 셀이라 row_h 48 / stride 56
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

LEFT, COMP_W, GAP, ROLE_W, ROLE_GAP, RIGHT = 12, 176, 12, 128, 12, 24
HEADER_Y, HEADER_H = 100, 52
ROW0, ROW_H, STRIDE = 168, 48, 56

roles = [('1. 로그인', 'A, B 둘 다'), ('2. expireAll', '표시만'), ('3. A 무효화', '①장부 ②Tomcat'), ('4. B 다음 요청', 'B 무효화 뒤')]
rows = [('principals[1]', '사용자 1의 ID 집합'), ('sessionIds[A]', 'A 의 장부 항목'), ('sessionIds[B]', 'B 의 장부 항목'), ('Tomcat sessions', '세션 맵')]
# (줄1, 줄2, 색)  색: OK / INFO / WARN / BAD / None(중립) / ACC(focal)
cells = [
    [('{A, B}', '등록', OK), ('{A, B}', '그대로', INFO), ('{B}', 'A 빠짐', BAD), ('(없음)', '항목 삭제', BAD)],
    [('expired=false', '등록', OK), ('expired=true', '표시', WARN), ('삭제', '① 장부 먼저', ACC), ('(없음)', '', None)],
    [('expired=false', '등록', OK), ('expired=true', '표시', WARN), ('expired=true', '그대로', WARN), ('삭제', '이벤트로', BAD)],
    [('{A, B}', '세션 둘', OK), ('{A, B}', '그대로', INFO), ('{B}', '② 맵에서 제거', BAD), ('{ }', 'B 제거', BAD)],
]

W = LEFT + COMP_W + GAP + len(roles) * ROLE_W + (len(roles) - 1) * ROLE_GAP + RIGHT
n_rows = len(rows)
rows_bottom = ROW0 + (n_rows - 1) * STRIDE + ROW_H
LEG_Y = rows_bottom + 28
H = LEG_Y + 56

d = D(W, H, 'MATRIX · REGISTRY LIFE AFTER PASSWORD CHANGE', '비밀번호 변경 뒤 장부와 Tomcat 맵이 바뀌는 순서', 'A 는 invalidate() 한 번 안에서 ① 장부 A 제거 ② Tomcat 맵 A 제거 순으로 빠지고 B 는 다음 요청까지 만료 표시 상태로 남는다', '사용자 1의 세션 A(변경 요청)와 B(다른 브라우저)')


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

d.legend(LEG_Y, [('① 장부 먼저 제거 (핵심)', ACC), ('등록', OK), ('그대로', INFO), ('표시', WARN), ('삭제', BAD)])

out_path = Path(__file__).parent.parent / '01-02.registry-life.svg'
d.save(str(out_path))
print(f"생성 완료: {out_path}")
