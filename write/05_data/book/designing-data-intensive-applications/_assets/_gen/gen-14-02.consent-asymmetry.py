# 14-02 §3 도식 — GDPR 이 요구하는 동의와 본문 §3 이 짚은 추적 서비스 현실을, 본문이 직접 GDPR 에 묶은 세 쟁점으로 대조한 격자.
# 사실 출처: 14-02 §3(L57~L71)·자주 받는 오해 1(L89), 원서 Ch.14 "Consent and Freedom of Choice" (PDF p.8~10, GDPR 인용 p.9)
# 10-31 검증(cc-ddia-dverify14): agy 판은 GDPR 네 형용사에 본문 문제를 1:1 로 짝지었으나 본문·원서에 없는 짝(일방적 약관↔Unambiguous)과
#   GDPR 해설(기본 서비스 이용 보장·단일 목적 한정·보관 기간 공개)을 지어 넣었다. 본문이 GDPR 에 직접 묶은 세 쟁점만 남긴다.
#   첫째(추적 필요성)는 본문이 GDPR 요건에 묶지 않아 뺐다. WARN/BAD 등급 범례도 본문 근거가 없어 뺐다.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W = 880
ROW_H = 60
ROW_STEP = 68
Y0 = 144

rows = [
    ("거부·철회", "without detriment",
     "불이익 없이 거부·철회", "아니면 자유로운 동의 아님",
     "거부는 소수 특권층의 선택지", "사회 참여 필수 · 네트워크 효과 비용"),
    ("이해", "informed",
     "정보에 입각한 동의", "명료하고 쉬운 언어로 요청",
     "밝히기보다 가리는 정책", "동의 안 한 비이용자 데이터까지"),
    ("상호성", "freely given",
     "자유롭게 주어진 동의", "협상 여지 없는 관계면 불성립",
     "협상 없는 일방향 추출", "약관은 서비스가 정함"),
]

LEG = Y0 + (len(rows) - 1) * ROW_STEP + ROW_H + 16
H = LEG + 56

d = D(W, H, "14-02 · SECTION 3", "GDPR 동의 요건과 온라인 추적 현실의 비교",
      "EU GDPR 이 요구하는 동의와 본문 §3 이 짚은 추적 서비스 현실을 본문이 GDPR 에 묶은 세 쟁점으로 대조.",
      "불이익 없는 거부 · 정보에 입각한 동의 · 자유롭게 주어진 동의 대 추적 서비스 현실")

# 열 헤더
d.box(24, 100, 150, 36, PAPER2, RULE, 0.8)
d.t(99, 122, "쟁점", 12, MUTED, KR, "middle", 600)

d.box(182, 100, 328, 36, PAPER2, OK, 1.0)
d.t(346, 122, "EU GDPR 요구", 12, OK, KR, "middle", 600)

d.tone(518, 100, 338, 36, ACC, 6, "14", 1.4)
d.t(687, 122, "온라인 추적 서비스 현실", 12, ACC, KR, "middle", 600)

for i, (axis_kr, axis_en, ok_title, ok_desc, bad_title, bad_desc) in enumerate(rows):
    y = Y0 + i * ROW_STEP

    # 쟁점 셀
    d.box(24, y, 150, ROW_H, PAPER2, RULE, 0.6, r=4)
    d.t(99, y + 26, axis_kr, 12, INK, KR, "middle", 600)
    d.t(99, y + 44, axis_en, 11, SOFT, MONO, "middle")

    # GDPR 요구 (OK)
    d.box(182, y, 328, ROW_H, PAPER, OK, 0.8, r=4)
    d.t(346, y + 26, ok_title, 12, INK, KR, "middle", 600)
    d.t(346, y + 44, ok_desc, 11, MUTED, KR, "middle")

    # 추적 서비스 현실 (focal 열)
    d.tone(518, y, 338, ROW_H, ACC, 4, "10", 1.1)
    d.t(687, y + 26, bad_title, 12, ACC, KR, "middle", 600)
    d.t(687, y + 44, bad_desc, 11, MUTED, KR, "middle")

# 범례
d.legend(LEG, [
    ("GDPR 요구", OK),
    ("추적 서비스 현실 (focal)", ACC)
])

d.save("14-02.consent-asymmetry.svg")
