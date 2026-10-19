# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.11 Listing 11-10~11-11, crypto/tls, crypto/x509
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480
d = D(W, H, "ARCHITECTURE · CERTIFICATE PINNING SCOPE",
      "기본 신뢰 저장소와 인증서 피닝의 신뢰 경계 비교",
      "기본 클라이언트(RootCAs: nil)와 피닝 클라이언트(RootCAs: certPool)의 신뢰 범위 차이를 대조합니다.",
      lead="인증서 피닝은 시스템에 등록된 수백 개 CA 를 배제하고 대상 서버 인증서 하나만 신뢰합니다.")

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

y1, y2 = 140, 276
NW1, NW2, NW3 = 220, 260, 250
NH = 84

# 행 1: 기본 신뢰 모델 (광범위)
d.chip(150, y1 - 14, "기본 신뢰 모델 (RootCAs: nil)", WARN,  11, 4)
d.tone(40, y1, NW1, NH, INFO, 6, "14", 1.0)
d.t(150, y1 + 32, "클라이언트 tls.Config", 13, INFO, KR, "middle", 600)
d.t(150, y1 + 54, "RootCAs: nil (기본값)", 11, MUTED, kr("RootCAs: nil (기본값)"), "middle")

d.tone(340, y1, NW2, NH, WARN, 6, "14", 1.0)
d.t(470, y1 + 32, "OS 시스템 신뢰 저장소", 13, WARN, KR, "middle", 600)
d.t(470, y1 + 54, "수백 개 공용 루트 CA 등록", 11, MUTED, KR, "middle")

d.tone(670, y1, NW3, NH, BAD, 6, "14", 1.1)
d.t(795, y1 + 32, "광범위한 신뢰 범위", 13, BAD, KR, "middle", 600)
d.t(795, y1 + 54, "어느 CA 든 서명 시 허용 (침해 위험)", 11, MUTED, KR, "middle")

d.arrow([(260, y1 + NH / 2), (336, y1 + NH / 2)], c=MUTED, m="ar")
d.t(298, y1 + NH / 2 - 8, "시스템 참조",  11, MUTED, KR, "middle")

d.arrow([(600, y1 + NH / 2), (666, y1 + NH / 2)], c=BAD, m="bad")
d.t(633, y1 + NH / 2 - 8, "전역 신뢰",  11, BAD, KR, "middle")

# 행 2: 인증서 피닝 모델 (단일 서버 격리)
d.chip(150, y2 - 14, "인증서 피닝 (RootCAs: certPool)", ACC,  11, 4)
d.tone(40, y2, NW1, NH, INFO, 6, "16", 1.1)
d.t(150, y2 + 32, "피닝 클라이언트 Config", 13, INFO, KR, "middle", 600)
d.t(150, y2 + 54, "RootCAs: certPool 지정", 11, MUTED, kr("RootCAs: certPool 지정"), "middle")

d.tone(340, y2, NW2, NH, OK, 6, "16", 1.1)
d.t(470, y2 + 32, "단일 서버 인증서 풀", 13, OK, KR, "middle", 600)
d.t(470, y2 + 54, "AppendCertsFromPEM(cert.pem)", 11, MUTED, MONO, "middle")

d.tone(670, y2, NW3, NH, ACC, 6, "18", 1.2)
d.t(795, y2 + 32, "단일 대상 신뢰 격리", 13, ACC, KR, "middle", 600)
d.t(795, y2 + 54, "cert.pem 이 서명하지 않은 인증서 거부", 11, MUTED, KR, "middle")

d.arrow([(260, y2 + NH / 2), (336, y2 + NH / 2)], c=OK, m="ok")
d.t(298, y2 + NH / 2 - 8, "cert.pem 주입",  11, OK, KR, "middle")

d.arrow([(600, y2 + NH / 2), (666, y2 + NH / 2)], c=ACC, m="acc")
d.t(633, y2 + NH / 2 - 8, "단일 격리",  11, ACC, KR, "middle")

d.legend(410, [("설정 객체", INFO), ("안전한 피닝 풀", OK), ("격리 신뢰 경계", ACC), ("광범위 신뢰 위험", BAD), ("시스템 저장소", WARN)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.certificate-pinning-scope.svg"
d.save(str(svg_path))
print("ok 11-01 certificate-pinning-scope")
