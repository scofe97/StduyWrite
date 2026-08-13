Output "16-01-statefulset-ordered.gif"

Require kubectl

Set Shell "bash"
Set Width 1200
Set Height 460
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
Type "kubectl config set-context --current --namespace=sts-lab"
Enter
Type "kubectl delete statefulset quiz --ignore-not-found"
Enter
Type "cd /tmp && cp sts-demo.yaml quiz.statefulset.yaml && sleep 3"
Enter
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "kubectl apply -f quiz.statefulset.yaml"
Sleep 400ms
Enter
Wait+Screen /created/
Sleep 1s

Type "kubectl get pods -w"
Sleep 400ms
Enter
Wait+Screen /quiz-2/
Sleep 5s
