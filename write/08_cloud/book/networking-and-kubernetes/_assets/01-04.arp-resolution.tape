Output "01-04.arp-resolution.gif"

Require tcpdump
Require ping

# ⛔ 이 테이프의 산출물은 공개 저장소에 커밋하지 않는다.
#    ARP 출력에는 이 랜의 게이트웨이 IP 와 양쪽 MAC 주소가 그대로 찍힌다.
#    5부 §11 민감정보 규약상 사설 대역 주소는 문서에 싣지 않는다.
#    굽더라도 로컬에서 확인만 하고 지우거나, private_dir 로 옮긴다.
#
# 굽기 전에:
#   1. sudo -v                                        # 자격 증명 캐시
#   2. GW=$(netstat -rn -f inet | awk '$1=="default"{print $2}')
#      아래 <GATEWAY_IP> 두 곳을 그 값으로 바꾼다. Type 은 변수 확장을 하지 않는다.

Set Shell "bash"
Set Width 1440
Set Height 420
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "sudo tcpdump -i en0 -e -n arp -c 4 &"
Sleep 400ms
Enter
Sleep 3s

Type "sudo arp -d <GATEWAY_IP>"
Sleep 400ms
Enter
Sleep 1500ms

Type "ping -c 1 <GATEWAY_IP>"
Sleep 400ms
Enter
Wait+Screen /ff:ff:ff:ff:ff:ff/
Sleep 7s
