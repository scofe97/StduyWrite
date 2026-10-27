# 타입 스펙: type-dp-security-matrix
# 사실 출처: NPG Ch.11 Listing 11-10~11-11, crypto/tls, crypto/x509 (사본 136, 146, 214, 451, 550, 552, 554줄)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, KR, MONO

W, H = 960, 548
d = D(W, H, "MATRIX · CERTIFICATE PINNING SCOPE",
      "기본 신뢰 저장소와 인증서 피닝의 신뢰 경계 비교",
      "자체 서명·공용 CA·오발급·저장소 변조·서버 침해·인증서 교체 시 동작 대조",
      lead="피닝은 자체 서명 검증과 CA 오발급·저장소 변조를 막지만, 공용 CA 접속이 막히고 서버 침해는 막지 못합니다.")

# 컬럼 X 좌표 및 폭 (모두 4의 배수)
# Comp (경우): x=24, w=256
# Col 1 (기본 클라이언트): x=296, w=312
# Col 2 (피닝 클라이언트): x=624, w=312
comp_x = 24
comp_w = 256
col1_x = 296
col1_w = 312
col2_x = 624
col2_w = 312

# 상단 헤더행 (y=96, h=52)
hdr_y = 96
hdr_h = 52

# 경우 헤더
d.box(comp_x, hdr_y, comp_w, hdr_h, fill="#161B22", stroke=RULE, sw=0.8)
d.t(comp_x + comp_w / 2, hdr_y + 22, "경우 (서버 및 공격 유형)", 13, INK, KR, "middle", 600)
d.t(comp_x + comp_w / 2, hdr_y + 40, "접속 대상 · 인증서 출처", 11, MUTED, KR, "middle")

# 기본 클라이언트 헤더
d.box(col1_x, hdr_y, col1_w, hdr_h, fill="#161B22", stroke=RULE, sw=0.8)
d.t(col1_x + col1_w / 2, hdr_y + 22, "기본 클라이언트", 14, INK, KR, "middle", 600)
d.t(col1_x + col1_w / 2, hdr_y + 40, "RootCAs: nil → 운영체제 루트 모음", 11, MUTED, MONO, "middle")

# 피닝 클라이언트 헤더
d.box(col2_x, hdr_y, col2_w, hdr_h, fill="#161B22", stroke=RULE, sw=0.8)
d.t(col2_x + col2_w / 2, hdr_y + 22, "피닝 클라이언트", 14, INK, KR, "middle", 600)
d.t(col2_x + col2_w / 2, hdr_y + 40, "RootCAs: certPool ← cert.pem", 11, MUTED, MONO, "middle")

# 행 정의: 6개 경우
# (경우명, 서브라벨, 기본결과, 기본서브, 기본색, 피닝결과, 피닝서브, 피닝색, is_focal)
rows = [
    # 행 0: 자체 서명 서버 (사본 146, 214, 550, 552줄)
    ("자체 서명 서버", "localhost, cert.pem",
     "거부", "unknown authority 오류", WARN,
     "통과", "cert.pem 직접 신뢰", OK, False),

    # 행 1: 공용 CA 서명 정상 서버 (사본 550줄)
    ("공용 CA 서명 정상 서버", "정상 발급 상용 웹 서버",
     "통과", "운영체제 루트 CA 사슬 검증", OK,
     "거부", "풀이 운영체제 모음 대체", WARN, False),

    # 행 2: CA 오발급 가짜 인증서 (사본 451, 552줄) - 피닝 열이 핵심 방어(FOCAL)
    ("CA 오발급 가짜 인증서", "TURKTRUST 중간 CA 오발급",
     "통과 → 속음", "진짜 CA 서명으로 사칭 수용", BAD,
     "거부 (핵심 방어)", "cert.pem 외 서명 차단", ACC, True),

    # 행 3: 신뢰 저장소 변조 (사본 451줄)
    ("신뢰 저장소 변조", "공격자 사설 루트 CA 등록",
     "통과 → 속음", "변조된 저장소 기준 수용", BAD,
     "거부", "운영체제 모음 안 씀", OK, False),

    # 행 4: 서버 호스트 침해 (사본 136줄)
    ("서버 호스트 침해", "서버 메모리 장악 · 세션 키 탈취",
     "못 막음", "호스트 침해 방어 한계", BAD,
     "못 막음", "진짜 서버 장악 시 무력", BAD, False),

    # 행 5: 서버 인증서 교체 (사본 554줄)
    ("서버 인증서 교체 (풀 그대로)", "만료 · 키 갱신 교체 시",
     "—", "해당 없음", RULE,
     "거부 (주의)", "옛·새 인증서 풀 동시 등록", WARN, False),
]

y_start = 160
row_h = 48
row_stride = 56

for idx, (c_name, c_sub, v1, s1, col1_c, v2, s2, col2_c, is_focal) in enumerate(rows):
    y = y_start + idx * row_stride

    # 경우 라벨 셀
    d.box(comp_x, y, comp_w, row_h, fill="#161B22", stroke=RULE, sw=0.8)
    d.t(comp_x + 14, y + 20, c_name, 12, INK, KR, "start", 600)
    fam_sub = MONO if "pem" in c_sub else KR
    d.t(comp_x + 14, y + 36, c_sub, 11, MUTED, fam_sub, "start")

    # 기본 클라이언트 셀
    if col1_c == RULE:
        d.box(col1_x, y, col1_w, row_h, fill="#161B22", stroke=RULE, sw=0.8)
        d.t(col1_x + col1_w / 2, y + 20, v1, 14, MUTED, MONO, "middle")
        d.t(col1_x + col1_w / 2, y + 36, s1, 11, MUTED, KR, "middle")
    else:
        d.tone(col1_x, y, col1_w, row_h, col1_c, 6, "14", 1.1)
        d.t(col1_x + col1_w / 2, y + 20, v1, 13, col1_c, KR, "middle", 600)
        d.t(col1_x + col1_w / 2, y + 36, s1, 11, MUTED, KR, "middle")

    # 피닝 클라이언트 셀
    if is_focal:
        # FOCAL 1곳: accent 테두리 1.8px + accent18 배경
        d.tone(col2_x, y, col2_w, row_h, ACC, 6, "18", 1.8)
        d.t(col2_x + col2_w / 2, y + 20, v2, 13, ACC, KR, "middle", 600)
        d.t(col2_x + col2_w / 2, y + 36, s2, 11, MUTED, KR, "middle")
    else:
        d.tone(col2_x, y, col2_w, row_h, col2_c, 6, "14", 1.1)
        d.t(col2_x + col2_w / 2, y + 20, v2, 13, col2_c, KR, "middle", 600)
        d.t(col2_x + col2_w / 2, y + 36, s2, 11, MUTED, KR, "middle")

# 범례
d.legend(508, [("통과 (안전) · 보호", OK), ("연결 거부 · 주의", WARN), ("속음 · 못 막음 (위험)", BAD), ("핵심 방어 (focal)", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.certificate-pinning-scope.svg"
d.save(str(svg_path))
print("ok 11-01 certificate-pinning-scope")
