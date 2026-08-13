Output "15-02-rollingupdate-progress.gif"

Require kubectl

Set Shell "bash"
Set Width 1200
Set Height 420
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export KUBECONFIG=/tmp/18-job.kubeconfig"
Enter
Type "kubectl config set-context --current --namespace=deploy-lab"
Enter
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "kubectl set image deploy/kiada app=busybox:1.37"
Sleep 400ms
Enter
Wait+Screen /image updated/
Sleep 3s

Type "kubectl get deploy kiada"
Sleep 400ms
Enter
Sleep 4s

Type "kubectl get deploy kiada"
Sleep 400ms
Enter
Sleep 6s
