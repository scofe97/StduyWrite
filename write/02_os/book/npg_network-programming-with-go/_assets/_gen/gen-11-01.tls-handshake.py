# 타입 스펙: type-sequence
# 사실 출처: RFC 8446 §2 (Handshake Protocol Overview), §4.4, NPG Ch.11
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO

W, H = 880, 576
s = Seq(W, H, "SEQUENCE · TLS 1.3 1-RTT HANDSHAKE",
        "TLS 1.3 핸드셰이크와 키 교환 및 세션 키 생성 순서",
        "클라이언트와 서버가 임시 ECDHE 키 공유를 교환해 세션 대칭 키를 유도하고 암호화 통신을 엽니다.",
        lead="TLS 1.3 은 단 1-RTT 만에 키 교환과 서버 인증 및 핸드셰이크 완료를 마칩니다.")

s.lanes([("클라이언트", "TLS Client"), ("서버", "TLS Server")], y0=104, lane_w=180)

# 메시지 1: ClientHello
s.msg("클라이언트", "서버", "ClientHello", 180, INFO, "info",
      sub="TLS 1.3 · TLS_AES_128_GCM_SHA256 · key_share")

# 메시지 2: ServerHello
s.msg("서버", "클라이언트", "ServerHello", 236, OK, "ok",
      sub="key_share · 스위트 확정 · ServerRandom(다운그레이드 표지)")

# 메시지 3: 암호화된 서버 핸드셰이크 메시지들
s.msg("서버", "클라이언트", "{EncryptedExtensions, Certificate, CertificateVerify, Finished}", 296, OK, "ok",
      sub="핸드셰이크 키로 암호화 · CertificateVerify: 서버 개인 키로 핸드셰이크 기록에 서명")

# 클라이언트 검증 및 키 파생
s.selfmsg("클라이언트", "서명 검증 & HKDF 키 유도", 356, ACC,
          sub="인증서 사슬 · CertificateVerify 서명 · Finished HMAC 확인")

# 메시지 4: 클라이언트 Finished
s.msg("클라이언트", "서버", "{Finished}", 416, INFO, "info",
      sub="클라이언트 핸드셰이크 완료 HMAC 전송")

# 메시지 5: 애플리케이션 데이터
# 양방향: 위 화살표는 클라이언트→서버, 아래 화살표는 서버→클라이언트
s.msg("클라이언트", "서버", "Application Data (양방향)", 466, OK, "ok")
xc, xs = s.LX["클라이언트"], s.LX["서버"]
s.path(f"M {xs - 10} 480 L {xc + 12} 480", OK, 1.5, m="ok")
s.t((xc + xs) / 2, 498, "AES-128-GCM 세션 키로 보호되는 데이터", 11, MUTED)

s.rails(508)
s.legend(526, [("클라이언트 전송", INFO), ("서버 응답 및 보호", OK), ("키 유도 및 검증", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.tls-handshake.svg"
s.save(str(svg_path))
print("ok 11-01 tls-handshake")
