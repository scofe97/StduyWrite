# 타입 스펙: type-dp-security-matrix — 다섯 층(행) × 다섯 실행 방식(열)에서 누가 운영하는지를 가르는 격자(격자 문법을 비교 행렬로 사용). 초점 칸 하나는 서버리스 런타임 칸이 세 갈래로 갈리는 자리.
# 사실 출처: NIST SP 800-145(2011-09) 서비스 모델 정의 — SaaS: 소비자는 네트워크·서버·OS·스토리지·개별 애플리케이션 기능도 통제하지 않음 / PaaS: 소비자가 만든 애플리케이션을 제공자가 지원하는 언어·라이브러리·도구로 올리고 OS·스토리지는 통제하지 않음 / IaaS: OS·스토리지·배포한 애플리케이션을 통제
#   https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf
#   · AWS Lambda 보안 개요 백서 "The Shared Responsibility Model"·"Lambda functions and layers"(OS·애플리케이션 플랫폼은 AWS, 코드와 IAM 은 고객, 커스텀 런타임은 고객이 유지) https://docs.aws.amazon.com/pdfs/whitepapers/latest/security-overview-aws-lambda/security-overview-aws-lambda.pdf
#   · Lambda 런타임 문서 "Shared responsibility model"(관리형 런타임은 Lambda 가 보안 업데이트를 게시·기본 자동 적용, 컨테이너 이미지는 고객이 다시 빌드) https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html
#   · 내가 통제하는 층 수 = 행 다섯 중 "내가" 칸의 개수: 온프레미스 5, IaaS 4, PaaS 1, SaaS 0, 서버리스 1(+ 조건부 1).
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 168, role_col_w 128, role_col_gap 8, header_h 52, header_y 96, row_h 56 · stride 60. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, ROLE_W, ROLE_GAP, HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 12, 168, 12, 128, 8, 96, 52, 164, 56, 60
roles = [("온프레미스", "전부 직접"), ("IaaS", "서버를 빌림"), ("PaaS", "코드를 올림"), ("SaaS", "앱을 씀"), ("서버리스", "Lambda 함수")]
rows = ["애플리케이션 코드", "런타임 · 언어 환경", "운영체제", "스토리지", "서버 · 가상화"]
ME, PR, CD = "me", "pr", "cd"
cells = [
    [ME, ME, ME, PR, ME],
    [ME, ME, PR, PR, CD],
    [ME, ME, PR, PR, PR],
    [ME, ME, PR, PR, PR],
    [ME, PR, PR, PR, PR],
]
COUNTS = ["5 / 5", "4 / 5", "1 / 5", "0 / 5", "1 / 5 + 조건부"]
FOCAL = (1, 4)

W = LEFT + COMP_W + GAP0 + 5 * ROLE_W + 4 * ROLE_GAP + 28
H = ROW0 + 5 * STRIDE + 56 + 24 + 44
d = D(W, H, "BYTEBYTEGO · 06-01 §3",
      "맡기는 층이 높아질수록 내가 통제하는 행이 줄어든다",
      "다섯 층 중 내가 통제하는 행은 5 → 4 → 1 → 0 이고 서버리스 런타임 칸만 조건에 따라 주인이 바뀝니다",
      "각 칸은 그 층을 통제하는 쪽입니다")

d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 22, "층", 12, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HDR_Y + 40, "× 실행 방식", 12, MUTED, KR)


def rx(j):
    return LEFT + COMP_W + GAP0 + j * (ROLE_W + ROLE_GAP)


for j, (nm, sub) in enumerate(roles):
    d.box(rx(j), HDR_Y, ROLE_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    fam = KR if any("가" <= c <= "힣" for c in nm) else MONO
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 22, nm, 12, INK, fam, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 40, sub, 12, MUTED, KR)

for i, name in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT + 12, y + 33, name, 12, INK, KR, "start", 600)
    for j in range(5):
        x = rx(j)
        k = cells[i][j]
        if (i, j) == FOCAL:
            d.tone(x, y, ROLE_W, ROW_H, ACC, 4, "14", 1.4)
            d.t(x + ROLE_W / 2, y + 16, "조건부", 12, ACC, KR, "middle", 600)
            d.t(x + ROLE_W / 2, y + 33, "관리형: AWS", 12, MUTED, KR)
            d.t(x + ROLE_W / 2, y + 49, "그 밖: 내가", 12, MUTED, KR)
        elif k == ME:
            d.tone(x, y, ROLE_W, ROW_H, WARN, 4, "10", 0.9)
            d.t(x + ROLE_W / 2, y + 33, "내가", 12, WARN, KR, "middle", 600)
        else:
            d.tone(x, y, ROLE_W, ROW_H, OK, 4, "10", 0.9)
            d.t(x + ROLE_W / 2, y + 33, "제공자", 12, OK, KR, "middle", 600)

cy = ROW0 + 5 * STRIDE + 8
d.box(LEFT, cy, COMP_W, 44, PAPER2, RULE, 0.8, 4)
d.t(LEFT + 12, cy + 27, "내가 통제하는 층", 12, INK, KR, "start", 600)
for j, v in enumerate(COUNTS):
    d.tone(rx(j), cy, ROLE_W, 44, INFO, 4, "10", 0.9)
    d.t(rx(j) + ROLE_W / 2, cy + 27, v, 12, INFO, KR, "middle", 600)

d.legend(H - 44, [("제공자가 맡음", OK), ("내가 통제", WARN), ("개수", INFO), ("이 편의 초점", ACC)])
d.save("06-01.responsibility-grid.svg")
