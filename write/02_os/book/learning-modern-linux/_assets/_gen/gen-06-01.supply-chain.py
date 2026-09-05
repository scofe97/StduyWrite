# 06-01 §7 — 소프트웨어가 내 기계에 닿기까지의 세 자리.
# 원문("Linux Application Supply Chains"): "a system of organizations and individuals supplying a
#       product to a consumer. ... the products are applications made up of software artifacts, and you
#       can think of the consumer as either yourself as the person using an app or as a tool that manages
#       the apps for you."
#   Software maintainers: "These include individual developers, open source projects, and companies, such
#       as independent software vendors (ISVs), that produce software artifacts and publish them, for
#       example, as packages to a repository (repo)."
#   Repository: "This lists the package that contains all or part of an app together with metadata. The
#       package usually captures the dependencies of an app. ... Keeping these dependencies up to date is
#       hard."
#   Tooling (a package manager): "On the target-system side, this can look up packages in the repository
#       and install, update, and remove apps as instructed by the human user."
#   실측 근거 — 저자의 `yum install golang` 출력 "Install 1 Package (+101 Dependent packages)",
#              "Total download size: 183 M", "Installed size: 624 M".
# 타입 스펙: type-data-flow — 무엇이 어느 방향으로 흐르는가. accent 는 저자가 어렵다고 못 박은 자리,
#           곧 의존성을 최신으로 유지하는 일. 축약: 서명·검증 경로는 원문이 한 줄로만 다뤄 그리지 않았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 596
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §7",
      "만드는 쪽과 쌓아 두는 쪽과 날라 오는 쪽",
      "apt install 한 줄 뒤에 서 있는 세 자리. 배포판마다 세부가 다르고 서버냐 데스크톱이냐에 "
      "따라서도 달라지지만, 이 셋은 어느 공급망에나 공통이다.",
      "저자는 의존성을 최신으로 유지하는 일이 어렵다고 못 박습니다")

BW, BH, Y = 244, 148, 168
GAP = (W - 48 - BW * 3) / 2
stages = [
    ("소프트웨어 관리자", "개별 개발자 · 오픈소스 프로젝트",
     "회사와 독립 소프트웨어 벤더", "산출물을 만들어 패키지로 발행한다", INFO),
    ("저장소", "패키지와 메타데이터를 목록에 올린다",
     "패키지가 앱의 의존성을 담는다", "앱 하나를 여러 패키지가 나타낼 수 있다", OK),
    ("도구 — 패키지 관리자", "대상 시스템 쪽에 있다",
     "저장소에서 찾고 설치 · 갱신 · 제거", "사람이 지시한 대로 움직인다", WARN),
]
for i, (name, l1, l2, l3, col) in enumerate(stages):
    x = 24 + i * (BW + GAP)
    d.box(x, Y, BW, BH, PAPER2, col, 1.2, 8)
    d.t(x + 16, Y + 30, name, 14.5, col, KR, "start", 600)
    d.line(x + 14, Y + 44, x + BW - 14, Y + 44, RULE, 1)
    d.t(x + 16, Y + 70, l1, 11.5, INK, KR, "start")
    d.t(x + 16, Y + 92, l2, 11.5, MUTED, KR, "start")
    d.t(x + 16, Y + 118, l3, 11.5, MUTED, KR, "start")
    if i < 2:
        d.arrow([(x + BW, Y + BH / 2), (x + BW + GAP - 2, Y + BH / 2)], MUTED, "ar", 1.5)
        mid = x + BW + GAP / 2
        d.t(mid, Y + BH / 2 - 14, ["발행", "조회"][i], 11.5, MUTED, KR, "middle", 600)

d.t(24, Y + BH + 34, "소비자", 12.5, SOFT, KR, "start", 600)
d.t(24 + 2 * (BW + GAP) + BW / 2, Y + BH + 34, "앱을 쓰는 사람이거나 그를 대신하는 도구",
    11.5, MUTED, KR, "middle")

AY = 372
d.o.append(f'<rect x="24" y="{AY}" width="{W - 48}" height="96" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(44, AY + 30, "저자가 어렵다고 적은 자리 — 의존성을 최신으로 유지하는 일", 14, ACC, KR, "start", 600)
d.t(44, AY + 56, "yum install golang 한 줄의 출력이 그 어려움을 숫자로 보입니다.", 12, ACC, KR, "start")
for i, (k, v) in enumerate([("딸려 오는 의존 패키지", "101 개"),
                            ("내려받는 양", "183 M"),
                            ("설치 뒤 차지하는 양", "624 M")]):
    x = 60 + i * 268
    d.t(x, AY + 82, k, 11.5, MUTED, KR, "start")
    d.t(x + 150, AY + 82, v, 12.5, INK, MONO, "start", 600)

d.legend(504, [("만드는 쪽", INFO), ("쌓아 두는 쪽", OK), ("날라 오는 쪽", WARN),
               ("어려운 자리", ACC)])
d.save("06-01.supply-chain.svg")
print("ok 06-01.supply-chain")
