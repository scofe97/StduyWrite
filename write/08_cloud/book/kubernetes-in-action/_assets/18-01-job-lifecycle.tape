Output "18-01-job-lifecycle.gif"

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
Type "kubectl config set-context --current --namespace=job-lab"
Enter
Type "kubectl delete job quiz-init --ignore-not-found"
Enter
Type "cd /tmp && cp job-demo.yaml job.quiz-init.yaml"
Enter
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "kubectl apply -f job.quiz-init.yaml"
Sleep 400ms
Enter
Wait+Screen /created/
Sleep 1s

Type "kubectl get jobs"
Sleep 400ms
Enter
Wait+Screen /Running/
Sleep 3s

Type "kubectl wait --for=condition=complete job/quiz-init --timeout=60s"
Sleep 400ms
Enter
Wait+Screen /condition met/
Sleep 1s

Type "kubectl get jobs"
Sleep 400ms
Enter
Wait+Screen /1\/1/
Sleep 6s
