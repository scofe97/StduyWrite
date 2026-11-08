# 44-01 「키를 둘로 나누면 방향마다 얻는 성질이 갈린다」 — 개인 키로 만든 서명은 공개 키로 확인하고, 공개 키로 만든 암호문은 개인 키로 푼다.
# 본문 근거: 이 노트 「2. 개인 키로 서명하고 공개 키로 암호화한다」.
# 검증 근거: openssl 3.6.4 로 RSA 2048 키 쌍을 만들어, 개인 키 서명은 공개 키로 Verified OK, 문장을 바꾸면 Verification failure.
#   공개 키로 암호화한 평문은 개인 키로만 복호된다.
# 공식 근거: SP 800-131A Rev. 2 — RSA 서명 생성은 키 길이 2048비트 이상을 허용(Acceptable).
# 타입 스펙: type-sequence — 키 쌍의 주인과 상대 두 참여자, 시간은 위에서 아래로만 흐른다.
#
# 상태 칩(state)은 ASCII 만 담는다. dd.py 의 폭 계산이 문자당 7px 이라 한글을 넣으면 칩이 글자보다 좁아진다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, RULE, KR, MONO

W, H = 920, 704

d = Seq(W, H, "OSTEP · 44-01 PUBLIC KEY",
        "개인 키로 만들면 서명이고 공개 키로 만들면 비밀이다",
        "위쪽은 키 쌍의 주인이 개인 키로 서명을 만들고 상대가 공개 키로 확인하는 흐름이다. 서명은 맞으면 Verified OK 이고 문장이 바뀌면 Verification failure 이다. "
        "아래쪽은 상대가 공개 키로 암호문을 만들고 주인이 개인 키로 푸는 흐름이다. 서명은 내용을 숨기지 못하고 암호문은 보낸 사람을 확인하지 못한다.",
        lead="RSA 2048 키 쌍 하나로 해 본 실험의 결과이다.")

d.lanes([("키 쌍의 주인", "private key"),
         ("상대", "public key")], lane_w=200)
d.rails(640)

# 개인 키로 만든 방향
d.t(148, 176, "개인 키로 만든 결과 — 작성자 확인", 13, MUTED, KR, "start", 600)
d.selfmsg("키 쌍의 주인", "sign(msg, private)", 220, INFO, sub="개인 키는 주인만 가짐")
d.msg("키 쌍의 주인", "상대", "msg + signature", 280, ACC, mk="acc", sub="내용은 그대로 보임")
d.state("상대", "Verified OK", 328, OK)
d.msg("키 쌍의 주인", "상대", "msg' + same signature", 392, MUTED, sub="전송 중 문장 한 글자가 바뀜")
d.state("상대", "Verification failure", 440, BAD)

d.line(24, 480, W - 48, 480, RULE, 0.8, "4 4")

# 공개 키로 만든 방향
d.t(148, 508, "공개 키로 만든 결과 — 내용 숨김", 13, MUTED, KR, "start", 600)
d.msg("상대", "키 쌍의 주인", "ciphertext", 564, ACC, mk="acc", sub="누구나 공개 키로 만들 수 있음")
d.selfmsg("키 쌍의 주인", "decrypt(private)", 612, INFO, sub="개인 키를 가진 쪽만 읽음")

d.legend(H - 40, [("키를 쓰는 연산", INFO), ("보내는 값", ACC), ("확인 성공", OK), ("확인 실패", BAD)])
d.save("44-01.public-key-directions.svg")
