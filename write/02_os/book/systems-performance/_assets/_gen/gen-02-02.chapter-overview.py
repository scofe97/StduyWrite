# 02-02 전체 지도 — 방법론 20종 × 원서 표 2.4 의 유형.
# 타입 스펙: type-dp-security-matrix — "어느 방법론이 어느 유형에 드는가"의 조합 격자.
#           원서 표 2.4(p.22–23) 그대로. 표의 2.5 밖 행(큐잉 이론·용량 계획·정량화·모니터링)은 02-03 몫이라 뺐다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER2, RULE, KR, MONO

TYPES = ["관측", "실험", "가설", "정보 수집", "생명주기", "튜닝", "용량 계획"]
ROWS = [  # (원서 절, 이름, 문서 §, 유형 인덱스들, 역할)
    ("2.5.1", "Streetlight", "§1", [0], "anti"), ("2.5.2", "Random change", "§1", [1], "anti"),
    ("2.5.3", "Blame-someone-else", "§1", [2], "anti"), ("2.5.4", "Ad hoc 체크리스트", "§2", [0, 1], ""),
    ("2.5.5", "문제 기술", "§2", [3], "start"), ("2.5.6", "과학적 방법", "§2", [0], ""),
    ("2.5.7", "진단 사이클", "§2", [4], ""), ("2.5.8", "도구 방법", "§2", [0], ""),
    ("2.5.9", "USE 방법", "§3", [0], "start"), ("2.5.10", "RED 방법", "§4", [0], ""),
    ("2.5.11", "워크로드 특성 파악", "§5", [0, 6], ""), ("2.5.12", "드릴다운 분석", "§6", [0], ""),
    ("2.5.13", "지연 분석", "§7", [0], ""), ("2.5.14", "Method R", "§7", [0], ""),
    ("2.5.15", "이벤트 추적", "§7", [0], ""), ("2.5.16", "기준선 통계", "§7", [0], ""),
    ("2.5.17", "정적 성능 튜닝", "§8", [0, 6], ""), ("2.5.18", "캐시 튜닝", "§8", [0, 5], ""),
    ("2.5.19", "마이크로벤치마킹", "§8", [1], ""), ("2.5.20", "성능 만트라", "§9", [5], ""),
]

W = 928
LX, CX, CW = 24, 336, 80
Y0, RH = 128, 26
H = Y0 + 40 + len(ROWS) * RH + 76

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-02",
       "방법론 20종은 대부분 관측이다",
       "원서 표 2.4 의 방법론 20종을 유형 일곱 칸에 놓았다. 한 방법론이 두 유형에 걸치면 두 칸이 켜진다. 행 끝의 § 는 이 문서의 절이다.",
       "원서 표 2.4 · 행 = 방법론, 열 = 유형")

for j, ty in enumerate(TYPES):
    x = CX + j * CW
    d.box(x + 2, Y0, CW - 4, 32, PAPER2, RULE, 1.0, 4)
    d.t(x + CW / 2, Y0 + 21, ty, 13, INK, KR, "middle", 600)

for i, (sec, name, ds, cols, role) in enumerate(ROWS):
    y = Y0 + 40 + i * RH
    c = BAD if role == "anti" else (ACC if role == "start" else INK)
    d.t(LX, y + 17, sec, 12, SOFT, MONO, "start")
    d.t(LX + 64, y + 17, name, 13, c, KR, "start", 600 if role else 400)
    d.t(CX - 12, y + 17, ds, 12, SOFT, MONO, "end")
    for j in range(len(TYPES)):
        x = CX + j * CW
        if j in cols: d.tone(x + 6, y + 3, CW - 12, RH - 6, INFO, 3)
        else: d.line(x + CW / 2 - 4, y + RH / 2, x + CW / 2 + 4, y + RH / 2, RULE, 1.0)

yl = Y0 + 40 + len(ROWS) * RH + 16
d.legend(yl, [("해당 유형", INFO), ("원서 권장 출발점", ACC), ("anti-method", BAD)])
d.save("02-02.chapter-overview.svg")
