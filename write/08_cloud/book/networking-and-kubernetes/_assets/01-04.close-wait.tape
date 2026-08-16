Output "01-04.close-wait.gif"

Require go
Require nc

Set Shell "bash"
Set Width 1440
Set Height 350
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

# 셋업: 닫지 않는 서버를 배경으로 띄운다. 학습 내용이 아니므로 Hide 로 감춘다.
Hide
Type "cd /private/tmp/claude-501/-Users-simbohyeon-claude/bd0a735e-d469-4873-bc70-abb5e9e7dd1b/scratchpad/lab"
Enter
Type "go run no-close-server.go > /dev/null 2>&1 &"
Enter
Sleep 4s
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "netstat -an -p tcp | grep 9090"
Sleep 400ms
Enter
Sleep 1500ms

Type "nc -w1 localhost 9090 < /dev/null"
Sleep 400ms
Enter
Sleep 2s

Type "netstat -an -p tcp | grep 9090"
Sleep 400ms
Enter
Wait+Screen /CLOSE_WAIT/
Sleep 6s
