Output "01-04.tls-plaintext.gif"

Require tcpdump
Require curl

# 사용자가 직접 굽는 테이프다. 라이브 캡처는 sudo 가 필요하다.
#
# 굽기 전에 sudo -v 로 자격 증명을 캐시한다.
#
# 캡처 대상이 en0 이므로 다른 트래픽이 섞일 수 있다. host example.com 으로 좁혀
# 우리가 만든 요청만 남긴다. 목적지가 공개 도메인이라 화면에 사설 주소는 찍히지 않는다.

Set Shell "bash"
Set Width 1440
Set Height 560
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

Type "sudo tcpdump -i en0 -n -A host example.com and port 443 -c 6 &"
Sleep 400ms
Enter
Sleep 3s

Type "curl -s https://example.com > /dev/null"
Sleep 400ms
Enter
Wait+Screen /example.com/
Sleep 7s
