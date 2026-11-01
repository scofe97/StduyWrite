# 05-01 §2 — 서비스 디스커버리의 해법은 간접을 한 겹씩 쌓으며 올라간다.
# 본문 근거: 이 노트 §2 93~131줄.
# 원서 근거: 01 명령줄 인자(원서 2쪽) → 02 hosts 파일 배포와 Docker 의 폐기된 link 옵션("This is the sort of
#            problem that host names were originally designed to solve", 원서 2쪽) → 03 중앙 DNS 도메인 이름
#            ("move to centralized distribution of names and IPs; that is, to use domain names stored in
#            DNS ... Using DNS provides a level of indirection as with hosts files, but allows the mapping
#            to change", 원서 2쪽) → 04 SRV 로 포트까지(원서 2~3쪽) → 05 전용 레지스트리(Consul 류, 원서 3쪽).
# 타입 스펙: type-layers — 아래 칸 위에 다음 칸이 얹히는 계층이고, 왼쪽 여백의 방향 표시가 논지다.
#           축약: 스펙의 폭 800~880 은 1000 viewBox 기준이라 880 캔버스에 비례로 줄여 740 을 쓴다.
# 2026-11-01 검증: 칸 오른쪽 라벨과 왼쪽 축 라벨이 "~한다·~없다" 문장이라 명사구로 줄였다.
#           05 칸은 본문 §3 161줄대로 "일반 DNS 질의" 경로에 푸시가 없다고 가렸다(RFC 8765 구독 경로와 구분).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING COREDNS · 05-01 §2",
      "간접을 한 겹씩 쌓아 올린 다섯 칸",
      "아래에서 위로 갈수록 클라이언트와 실제 주소 사이에 낀 층이 하나씩 늘어난다. "
      "층이 늘어난 만큼 주소를 바꿔도 클라이언트를 안 고치게 된다.",
      "세 번째 칸에서 간접이 처음 중앙으로 옮겨 갑니다")

LX, LW, LH, Y0 = 100, 740, 64, 112
layers = [
    ("05", "전용 레지스트리", "API 로 등록 · 일반 DNS 질의엔 여전히 푸시 없음", False),
    ("04", "SRV 레코드", "포트까지 조회 · 관례 포트에 안 묶임", False),
    ("03", "중앙 DNS", "매핑 변경 가능 · 클라이언트 재설정 불필요", True),
    ("02", "hosts 파일 배포", "같은 호스트에서만 · 경합 조건으로 실패", False),
    ("01", "명령줄 인자", "이동 시 의존 서비스 전부 재설정 · 재기동", False),
]

for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.tone(LX, y, LW, LH, ACC, 0, "12", 1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 0)
    d.t(LX + 16, y + 38, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(LX + 64, y + 38, name, 16, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 16, y + 38, sub, 12, MUTED, KR, "end")

d.path(f"M 60 {Y0 + 5 * LH - 12} L 60 {Y0 + 12}", SOFT, 1.4, m="soft")
d.t(20, Y0 + 5 * LH + 12, "간접", 12, SOFT, KR, "start")
d.t(20, Y0 + 5 * LH + 30, "한 겹씩", 12, SOFT, KR, "start")

BOT = Y0 + 5 * LH
d.t(LX, BOT + 40, "1→2칸 · 이름의 등장 · 2→3칸 · 이름의 중앙화", 13, MUTED, KR, "start")
d.t(LX, BOT + 64, "4칸 · 포트 추가 · 5칸 · API 등록 · 조회는 여전히 당겨 오기", 13, MUTED, KR, "start")

d.legend(BOT + 92, [("간접이 처음 중앙으로 간 칸", ACC)])
d.save("05-01.discovery-ladder.svg")
