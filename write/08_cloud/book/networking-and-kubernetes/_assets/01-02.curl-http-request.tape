Output "01-02.curl-http-request.gif"

Require curl

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

# 사전 조건: 같은 호스트에서 01-01 §5 의 Go 웹 서버가 8080 으로 떠 있어야 한다.
#   go run main.go &
Hide
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "curl localhost:8080 -vvv"
Sleep 500ms
Enter
Wait+Screen /Hello/
Sleep 6s
