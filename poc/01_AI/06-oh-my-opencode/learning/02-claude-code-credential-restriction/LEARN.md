# 02. Claude Code 자격 증명 제한 이슈

## 목표

OpenCode 또는 OMO 환경에서 Claude Code 자격 증명을 섞어 쓰려 할 때 발생할 수 있는 제한과 운영 리스크를 이해한다.

## 참고 글 요약

참고 글: `https://ios-development.tistory.com/1839`

글의 핵심 주장은 단순하다.

- Claude Code 자격 증명을 OpenCode 같은 다른 환경에서 재사용하려 하면 제한될 수 있다
- 실제 에러 메시지와 커뮤니티 사례가 존재한다
- OpenCode 이슈만 보고 무조건 해결될 것이라 기대하면 안 된다
- 명확한 해결책이 없으면 Claude Code는 네이티브 환경에서 쓰는 편이 안전하다

## 대표 에러 메시지

글에서 제시한 핵심 에러는 아래다.

```text
This credential is only authorized for use with Claude Code and cannot be used for other API requests.
```

의미:

- 이 인증 정보는 Claude Code 전용으로 승인되었다
- 따라서 OpenCode나 다른 third-party harness에서 같은 자격 증명을 직접 재사용하는 방식은 막힐 수 있다

## 글에서 정리한 근거

글은 아래 근거를 제시한다.

1. Claude Code를 OpenCode와 같은 다른 환경에서 사용하다가 계정 정지 또는 사용 중지 사례가 있었다고 소개
2. OpenCode 이슈에서 관련 문의를 해도 GitHub Action이나 특정 케이스 확인 수준의 안내가 있었다고 설명
3. OpenCode 저장소 쪽에 Claude Code 관련 설정을 제거한 커밋이 존재한다고 언급
4. Anthropic 관련 설명 파일에도 제한 취지의 내용이 있다고 정리
5. Reddit 등 커뮤니티에서도 비슷한 제보를 언급

이 글은 "우회가 기술적으로 가능한가"보다 "운영적으로 안전한가"에 초점을 둔다.

## 이 이슈가 중요한 이유

OMO/OpenCode 문맥에서 이 문제는 꽤 중요하다.

### 1. 설치 성공과 운영 가능은 다르다

어떤 설정은 당장 동작할 수 있어도, provider 약관이나 인증 정책과 충돌하면 나중에 막힐 수 있다.

### 2. 문서보다 정책이 더 빨리 바뀔 수 있다

특히 인증/자격 증명/계정 제한은 매우 시점 민감하다. 어제 되던 방식이 오늘 막힐 수 있다.

### 3. "third-party harness"는 항상 리스크를 본다

Claude Code 네이티브 환경이 아닌 곳에서 Claude 전용 인증을 재활용하려는 시도는 정책 리스크가 크다.

## 실무적으로 어떻게 판단할까

### 권장 원칙

1. Claude Code 전용 credential은 Claude Code 안에서만 쓴다고 가정한다
2. OpenCode에서는 OpenCode가 공식적으로 지원하는 provider 인증 경로를 우선 사용한다
3. OMO를 쓰더라도 provider 인증은 `opencode auth login` 기준의 공식 흐름으로 맞춘다
4. Claude 계정 연결이 막히거나 위 에러가 뜨면 우회 설정부터 늘리지 말고 네이티브 Claude Code 사용 여부를 먼저 판단한다

### 피해야 할 태도

- "지금 우연히 되니까 계속 써도 된다"는 판단
- 커뮤니티 우회 팁을 곧바로 장기 운영 방식으로 채택하는 것
- 토큰 비용이나 편의성만 보고 계정 정책 리스크를 무시하는 것

## OMO 문서 관점에서의 정리

이 프로젝트 문맥에서는 아래처럼 이해하면 된다.

- OMO는 강력한 OpenCode 하네스다
- 하지만 Claude Code 전용 인증을 OpenCode에서 그대로 우회 사용하려는 것은 별개 문제다
- OMO의 품질과 credential 정책 리스크는 분리해서 봐야 한다

즉:

- **OMO 자체**는 유용한 학습/생산성 도구다
- **Claude Code 전용 credential 재사용**은 별도의 운영 리스크다

## 추천 대응 전략

| 상황 | 권장 대응 |
|------|----------|
| OpenCode에서 Claude provider를 정상적으로 공식 인증 가능 | 공식 인증 경로 사용 |
| Claude Code credential 재사용 중 위 에러 발생 | 우회보다 네이티브 Claude Code 사용 검토 |
| 커뮤니티 우회 설정만 존재하고 공식 해결책이 없음 | 장기 운영에 사용하지 않음 |
| 학습/실험 목적의 단기 확인 | 계정 리스크를 명확히 인지하고 제한적으로만 시도 |

## 결론

이 글의 메시지는 공격적 우회 팁이 아니라 보수적 운영 가이드에 가깝다.

- OpenCode/OMO를 쓴다고 해서 Claude Code 전용 자격 증명을 마음대로 재활용할 수 있다고 보면 안 된다
- 인증 정책과 계정 제한은 설치 편의보다 우선한다
- 에러가 발생하면 억지 우회보다 네이티브 Claude Code 사용으로 돌아가는 것이 더 안전하다

## 참고 링크

- 원문: https://ios-development.tistory.com/1839
- OpenCode 이슈 예시: https://github.com/anomalyco/opencode/issues/10956
- OpenCode 이슈 예시: https://github.com/anomalyco/opencode/issues/7410
- 커밋 언급: https://github.com/anomalyco/opencode/commit/973715f3da1839ef2eba62d4140fe7441d539411#diff-23c1b48647ee5935d7825f0f38195a8e018b726e1e331bcc0fcc8f8ce85e4c71L335
