# 01-01 §3 — 성능 활동 11단계가 수명주기의 어느 구간에 놓이고, 클라우드 지름길과 용량 계획이 어디에 걸치는가.
# 타입 스펙: type-process — 구간마다 같은 슬롯(번호 · 활동)이 반복되고 가로 위치가 수명주기의 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 행 stride 36 으로 고정한다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 1000, 584
Y0, HEAD, ROW, RH = 152, 40, 36, 28

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-01 §3 · SEC 1.3",
       "성능 활동 11단계와 수명주기",
       "원서 1.3 의 활동 열한 가지를 개발 · 타깃 환경 · 사후 구간으로 나눴다. 클라우드의 canary · blue-green 은 1~5 를 건너뛰고 6 으로 가게 하고, 용량 계획은 설계 단계와 배포 후 모니터링 두 자리에 걸친다.",
       "타깃 환경에서 드러난 이슈는 개발 단계에서 놓친 것입니다")

PHASES = [
    (24, 360, "개발 · 1~5", "제품이든 사내 서비스든", [
        ("1", "성능 목표 설정 · 모델링"), ("2", "프로토타입 성능 특성 파악"),
        ("3", "테스트 환경 성능 분석"), ("4", "새 버전 비회귀 테스트"), ("5", "릴리스 벤치마킹")]),
    (448, 300, "타깃 환경 · 6~9", "출시 뒤", [
        ("6", "타깃 환경 PoC 테스트"), ("7", "프로덕션 성능 튜닝"),
        ("8", "프로덕션 모니터링"), ("9", "프로덕션 이슈 분석")]),
    (780, 196, "사후 · 10~11", "SRE 함께", [
        ("10", "사후 검토"), ("11", "성능 도구 개발")]),
]

def row_y(i): return Y0 + HEAD + 4 + i * ROW

for x, w, name, sub, rows in PHASES:
    h = HEAD + len(rows) * ROW + 8
    d.box(x, Y0, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y0 + 26, name, 14, INK, KR, "start", 600)
    d.t(x + w - 16, Y0 + 26, sub, 12, MUTED, KR, "end")
    d.line(x + 12, Y0 + HEAD, x + w - 12, Y0 + HEAD, RULE, 0.8)
    for i, (n, label) in enumerate(rows):
        y = row_y(i)
        if n == "8": d.tone(x + 8, y, w - 16, RH, INFO, 4)
        d.t(x + 32, y + 19, n, 12, SOFT, MONO, "end", 600)
        d.t(x + 44, y + 19, label, 13, INFO if n == "8" else MUTED, KR, "start")

# 출시
XR = 416
d.line(XR, Y0, XR, Y0 + HEAD + 5 * ROW + 8, SOFT, 1.0, "4 4")
d.t(XR, Y0 - 8, "출시", 12, SOFT, KR, "middle", 600)

# 용량 계획 괄호 두 자리
YC = 116
for x, w, label in ((24, 360, "용량 계획 · 설계 중 자원 발자국 연구"), (448, 300, "용량 계획 · 배포 후 모니터링으로 예측")):
    d.line(x + 4, YC, x + w - 4, YC, INFO, 1.2)
    d.line(x + 4, YC, x + 4, YC + 8, INFO, 1.2)
    d.line(x + w - 4, YC, x + w - 4, YC + 8, INFO, 1.2)
    d.t(x + w / 2, YC - 8, label, 12, INFO, KR, "middle")

# 6~9 에서 드러나면
YD = Y0 + HEAD + 5 * ROW + 8          # 개발 상자 바닥 = 380
YT = Y0 + HEAD + 4 * ROW + 8          # 타깃 상자 바닥
d.t(448 + 150, YT + 24, "여기서 나온 이슈 = 개발 단계에서 놓친 것", 12, WARN, KR, "middle")

# 클라우드 지름길 — 1~5 를 건너뛰고 6 으로
YS = YD + 40
d.arrow([(56, YD), (56, YS), (432, YS), (432, row_y(0) + 14), (446, row_y(0) + 14)], ACC, "acc", 1.8)
d.t(244, YS + 22, "클라우드 지름길 · canary · blue-green · 1~5 건너뜀", 13, ACC, KR, "middle", 600)

# 늦을수록
YA = YS + 56
d.arrow([(24, YA), (976, YA)], SOFT, "soft", 1.2, "4 6")
d.t(500, YA + 22, "늦을수록 앞선 아키텍처 결정에서 생긴 성능 문제를 고치는 비용 증가", 12, MUTED, KR, "middle")

d.legend(YA + 40, [("클라우드 지름길", ACC), ("용량 계획", INFO), ("놓친 이슈가 드러나는 자리", WARN)])
d.save("01-01.activity-lifecycle.svg")
