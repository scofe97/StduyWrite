# 01-01 §3 — CKS 출제 도메인 여섯의 비중(%)과 책 장 대응.
# 본문 근거: 이 노트 §3 「출제 도메인 여섯과 책의 장 대응」.
# 공식 근거: CNCF CKS_Curriculum v1.37.pdf (15%, 15%, 10%, 20%, 20%, 20%).
# 타입 스펙: type-bar — 긴 영문 도메인 이름 6개를 가로 막대로 비교하고 막대 끝에 책 장 번호를 붙인다.
# 축약: 스펙의 8px 눈금·값 라벨을 스타일 계약의 최소 11px/한글 12px 규칙에 맞춰 키웠다.
import sys
sys.path.insert(0, ".")
from dd import D, MUTED, SOFT, INK, RULE, OK, INFO, KR, MONO

W, H = 920, 444
d = D(W, H, "CKS STUDY GUIDE · 01-01 §3",
      "CKS v1.37 출제 도메인 비중과 책 장 대응",
      "CNCF CKS v1.37 커리큘럼 여섯 도메인의 출제 비중(%)을 가로 막대 길이로, 막대 끝에 대응하는 책의 장 번호를 나타낸 차트다.",
      "앞 세 도메인은 클러스터·호스트 설정(40%), 뒤 세 도메인은 워크로드·공급망·런타임 방어(60%)를 맡습니다")

X0 = 332          # 0% 축
PX_PER_PCT = 20   # 0~25% -> 500px (X=332..832)
TOP_Y = 104
ROW_H = 36
STRIDE = 44

domains = [
    ("Cluster Setup", 15, "2장", INFO),
    ("Cluster Hardening", 15, "3장", INFO),
    ("System Hardening", 10, "4장", INFO),
    ("Minimize Microservice Vulnerabilities", 20, "5장", OK),
    ("Supply Chain Security", 20, "6장", OK),
    ("Monitoring, Logging and Runtime Security", 20, "7장", OK),
]

BOT_Y = TOP_Y + len(domains) * STRIDE - 4

# 세로 눈금선 (0% 축은 강조, 5~25%는 희미하게)
for pct in range(0, 26, 5):
    gx = X0 + pct * PX_PER_PCT
    if pct == 0:
        d.line(gx, TOP_Y - 8, gx, BOT_Y, SOFT, 1.0)
    else:
        d.line(gx, TOP_Y - 8, gx, BOT_Y, RULE, 0.8)
    d.t(gx, BOT_Y + 18, f"{pct}%", 11, MUTED, MONO, "middle")

# 막대와 라벨
for i, (name, pct, ch, c) in enumerate(domains):
    y = TOP_Y + i * STRIDE
    bw = pct * PX_PER_PCT
    d.t(X0 - 12, y + 22, name, 12, INK, KR, "end", 600)
    d.tone(X0, y + 4, bw, ROW_H - 8, c, 4, "24", 1.2)
    d.t(X0 + bw + 12, y + 22, f"{pct}% · {ch}", 12, c, KR, "start", 600)

d.legend(400, [("클러스터·호스트 설정 (40%)", INFO), ("워크로드·공급망·런타임 방어 (60%)", OK)])
d.save("01-01.domain-weights.svg")
