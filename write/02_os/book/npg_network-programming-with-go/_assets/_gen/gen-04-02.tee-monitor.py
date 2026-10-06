# 타입 스펙: type-data-flow
# 04-02 TeeReader 와 MultiWriter 트래픽 복제 파이프라인
# 사실 출처: NPG Ch.4 Listing 4-19·4-20 (io.TeeReader, io.MultiWriter)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 500
d = D(W, H, "LISTING 4-19 TEE-MONITOR",
      "트래픽 관측 파이프라인",
      "TeeReader 와 MultiWriter 의 투명한 바이트 복제 및 모니터링",
      "연결 변경 없는 입출력 스트림 복제")

# 1. 수신 파이프라인 (TeeReader)
d.t(36, 116, "수신 흐름", 11, INFO, KR, "start", 600)

# 소켓 Source
d.box(36, 130, 114, 40, fill=PAPER2, stroke=RULE)
d.t(93, 154, "소켓 (net.Conn)", 11, INK, KR, "middle")

# 소켓 -> TeeReader 사이 데이터 블록
d.line(150, 150, 164, 150, INFO, 1.4)
d.tone(164, 138, 56, 24, INFO, op="25", sw=1.0)
d.t(192, 154, "b[:n]", 10, INFO, MONO, "middle")
d.arrow([(220, 150), (236, 150)], INFO, "info", 1.4)

# io.TeeReader
d.box(236, 126, 138, 48, fill=PAPER2, stroke=INFO, sw=1.2)
d.t(305, 146, "io.TeeReader", 12, INFO, MONO, "middle", 600)
d.t(305, 163, "수신 스트림 분기", 11, MUTED, KR, "middle")

# 분기 1: Go 앱 Reader
d.line(374, 142, 392, 142, INFO, 1.4)
d.tone(392, 130, 56, 24, INFO, op="25", sw=1.0)
d.t(420, 146, "b[:n]", 10, INFO, MONO, "middle")
d.arrow([(448, 142), (480, 142)], INFO, "info", 1.4)
d.box(480, 124, 130, 36, fill=PAPER2, stroke=RULE)
d.t(545, 146, "Go 앱 (Reader)", 11, INK, KR, "middle")

# 분기 2: 모니터
d.path("M 305 174 L 305 206 L 360 206", ACC, 1.4)
d.tone(360, 194, 56, 24, ACC, op="25", sw=1.0)
d.t(388, 210, "b[:n]", 10, ACC, MONO, "middle")
d.arrow([(416, 206), (480, 206)], ACC, "acc", 1.4)
d.box(480, 188, 130, 36, fill=PAPER2, stroke=ACC, sw=1.0)
d.t(545, 210, "모니터 (Monitor)", 11, ACC, KR, "middle")

# 우측 안내 상자
d.box(646, 124, 200, 100, fill=PAPER2, stroke=RULE)
d.t(664, 164, "무침습 수신 관측", 12, INFO, KR, "start", 600)
d.t(664, 188, "소켓 읽기 동작 유지", 11, MUTED, KR, "start")


# 2. 송신 파이프라인 (MultiWriter)
d.t(36, 268, "송신 흐름", 11, OK, KR, "start", 600)

# Go 앱 Writer Source
d.box(36, 282, 114, 40, fill=PAPER2, stroke=RULE)
d.t(93, 306, "Go 앱 (Writer)", 11, INK, KR, "middle")

# Go 앱 -> MultiWriter 사이 데이터 블록
d.line(150, 302, 164, 302, OK, 1.4)
d.tone(164, 290, 56, 24, OK, op="25", sw=1.0)
d.t(192, 306, "b[:n]", 10, OK, MONO, "middle")
d.arrow([(220, 302), (236, 302)], OK, "ok", 1.4)

# io.MultiWriter
d.box(236, 278, 138, 48, fill=PAPER2, stroke=OK, sw=1.2)
d.t(305, 298, "io.MultiWriter", 12, OK, MONO, "middle", 600)
d.t(305, 315, "송신 데이터 복제", 11, MUTED, KR, "middle")

# 분기 1: 소켓 net.Conn
d.line(374, 294, 392, 294, OK, 1.4)
d.tone(392, 282, 56, 24, OK, op="25", sw=1.0)
d.t(420, 298, "b[:n]", 10, OK, MONO, "middle")
d.arrow([(448, 294), (480, 294)], OK, "ok", 1.4)
d.box(480, 276, 130, 36, fill=PAPER2, stroke=RULE)
d.t(545, 298, "소켓 (net.Conn)", 11, INK, KR, "middle")

# 분기 2: 모니터
d.path("M 305 326 L 305 358 L 360 358", ACC, 1.4)
d.tone(360, 346, 56, 24, ACC, op="25", sw=1.0)
d.t(388, 362, "b[:n]", 10, ACC, MONO, "middle")
d.arrow([(416, 358), (480, 358)], ACC, "acc", 1.4)
d.box(480, 340, 130, 36, fill=PAPER2, stroke=ACC, sw=1.0)
d.t(545, 362, "모니터 (Monitor)", 11, ACC, KR, "middle")

# 우측 안내 상자
d.box(646, 276, 200, 100, fill=PAPER2, stroke=RULE)
d.t(664, 316, "투명한 송신 복제", 12, OK, KR, "start", 600)
d.t(664, 340, "단일 쓰기 다중 전송", 11, MUTED, KR, "start")

d.legend(H - 46, [("수신 데이터", INFO), ("송신 데이터", OK), ("복제 데이터", ACC)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-02.tee-monitor.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
