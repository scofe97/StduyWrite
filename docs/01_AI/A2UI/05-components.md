# A2UI 컴포넌트 레퍼런스 (Components Reference)

> **학습 목표**: A2UI 표준 컴포넌트의 종류와 사용법을 마스터한다.

---

## 1. 컴포넌트 카테고리

A2UI는 목적별로 조직된 표준 컴포넌트를 제공합니다:

| 카테고리 | 컴포넌트 | 용도 |
|----------|---------|------|
| **레이아웃** | Row, Column, List | 컴포넌트 배치 |
| **표시** | Text, Image, Icon, Divider | 콘텐츠 표시 |
| **입력** | TextField, Button, Checkbox, DateTimeInput, Slider | 사용자 입력 |
| **컨테이너** | Card, Modal, Tabs | 콘텐츠 그룹화 |

---

## 2. 레이아웃 컴포넌트

### 2.1 Row (가로 레이아웃)

자식을 **가로로** 배치합니다 (왼쪽 → 오른쪽).

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `children` | Children | 자식 컴포넌트 |
| `distribution` | String | 수평 분배 |
| `alignment` | String | 수직 정렬 |

**distribution 옵션**:
- `start`: 시작점 정렬
- `center`: 중앙 정렬
- `end`: 끝점 정렬
- `spaceBetween`: 균등 분배 (양 끝 붙음)
- `spaceAround`: 균등 분배 (양 끝 여백 절반)
- `spaceEvenly`: 균등 분배 (동일 간격)

**예시**:
```json
{
  "id": "header-row",
  "component": {
    "Row": {
      "children": {"explicitList": ["logo", "nav", "profile"]},
      "distribution": "spaceBetween",
      "alignment": "center"
    }
  }
}
```

### 2.2 Column (세로 레이아웃)

자식을 **세로로** 배치합니다 (위 → 아래).

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `children` | Children | 자식 컴포넌트 |
| `distribution` | String | 수직 분배 |
| `alignment` | String | 수평 정렬 |

**예시**:
```json
{
  "id": "form-column",
  "component": {
    "Column": {
      "children": {"explicitList": ["title", "input1", "input2", "submit"]},
      "distribution": "start",
      "alignment": "stretch"
    }
  }
}
```

### 2.3 List (스크롤 리스트)

스크롤 가능한 리스트를 생성합니다. 동적 데이터에 적합합니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `children` | Children | 템플릿 기반 데이터 바인딩 지원 |

**예시** (동적 리스트):
```json
{
  "id": "product-list",
  "component": {
    "List": {
      "children": {
        "template": {
          "dataBinding": "/products",
          "componentId": "product-item"
        }
      }
    }
  }
}
```

---

## 3. 표시 컴포넌트

### 3.1 Text (텍스트)

텍스트 콘텐츠를 표시합니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `text` | BoundValue | 표시할 텍스트 |
| `usageHint` | String | 스타일 힌트 |

**usageHint 옵션**:
- `h1`, `h2`, `h3`, `h4`, `h5`: 제목 레벨
- `body`: 본문 텍스트
- `caption`: 작은 설명 텍스트

**예시**:
```json
{
  "id": "page-title",
  "component": {
    "Text": {
      "text": {"literalString": "환영합니다!"},
      "usageHint": "h1"
    }
  }
}
```

```json
{
  "id": "user-name",
  "component": {
    "Text": {
      "text": {"path": "/user/name"},
      "usageHint": "body"
    }
  }
}
```

### 3.2 Image (이미지)

URL에서 이미지를 표시합니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `url` | BoundValue | 이미지 URL |

**예시**:
```json
{
  "id": "profile-image",
  "component": {
    "Image": {
      "url": {"path": "/user/avatarUrl"}
    }
  }
}
```

### 3.3 Icon (아이콘)

Material Icons 또는 커스텀 아이콘을 표시합니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `name` | BoundValue | 아이콘 이름 |

**예시**:
```json
{
  "id": "settings-icon",
  "component": {
    "Icon": {
      "name": {"literalString": "settings"}
    }
  }
}
```

**자주 사용하는 아이콘**:
- `home`, `settings`, `person`, `search`
- `add`, `delete`, `edit`, `save`
- `check`, `close`, `arrow_back`, `arrow_forward`

### 3.4 Divider (구분선)

시각적 구분선을 표시합니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `axis` | String | `horizontal` 또는 `vertical` |

**예시**:
```json
{
  "id": "section-divider",
  "component": {
    "Divider": {
      "axis": "horizontal"
    }
  }
}
```

---

## 4. 입력 컴포넌트

### 4.1 Button (버튼)

클릭 가능한 버튼입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `child` | String | 버튼 내부 컴포넌트 ID |
| `primary` | Boolean | 주요 버튼 여부 |
| `action` | Action | 클릭 시 수행할 액션 |

**예시**:
```json
{
  "id": "submit-btn",
  "component": {
    "Button": {
      "child": "btn-label",
      "primary": true,
      "action": {"name": "submit_form"}
    }
  }
},
{
  "id": "btn-label",
  "component": {
    "Text": {"text": {"literalString": "제출하기"}}
  }
}
```

### 4.2 TextField (텍스트 입력)

텍스트 입력 필드입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `label` | BoundValue | 입력 필드 레이블 |
| `text` | BoundValue | 데이터 바인딩 경로 |
| `textFieldType` | String | 입력 타입 |

**textFieldType 옵션**:
- `shortText`: 짧은 텍스트 (한 줄)
- `longText`: 긴 텍스트 (여러 줄)
- `number`: 숫자 입력
- `date`: 날짜 입력
- `obscured`: 비밀번호 입력

**예시**:
```json
{
  "id": "email-input",
  "component": {
    "TextField": {
      "label": {"literalString": "이메일"},
      "text": {"path": "/form/email"},
      "textFieldType": "shortText"
    }
  }
}
```

```json
{
  "id": "password-input",
  "component": {
    "TextField": {
      "label": {"literalString": "비밀번호"},
      "text": {"path": "/form/password"},
      "textFieldType": "obscured"
    }
  }
}
```

### 4.3 Checkbox (체크박스)

불리언 토글입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `label` | BoundValue | 체크박스 레이블 |
| `value` | BoundValue | 데이터 바인딩 경로 |

**예시**:
```json
{
  "id": "agree-checkbox",
  "component": {
    "Checkbox": {
      "label": {"literalString": "약관에 동의합니다"},
      "value": {"path": "/form/agreed"}
    }
  }
}
```

### 4.4 DateTimeInput (날짜/시간 입력)

날짜 및 시간 선택기입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `label` | BoundValue | 입력 필드 레이블 |
| `value` | BoundValue | 데이터 바인딩 경로 (ISO 8601 형식) |

**예시**:
```json
{
  "id": "reservation-date",
  "component": {
    "DateTimeInput": {
      "label": {"literalString": "예약 날짜"},
      "value": {"path": "/reservation/datetime"}
    }
  }
}
```

**데이터 형식**: ISO 8601 (`2025-12-25T19:00:00Z`)

### 4.5 Slider (슬라이더)

범위 값 선택기입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `value` | BoundValue | 현재 값 |
| `min` | Number | 최소값 |
| `max` | Number | 최대값 |

**예시**:
```json
{
  "id": "volume-slider",
  "component": {
    "Slider": {
      "value": {"path": "/settings/volume"},
      "min": 0,
      "max": 100
    }
  }
}
```

---

## 5. 컨테이너 컴포넌트

### 5.1 Card (카드)

테두리/그림자와 패딩이 있는 컨테이너입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `child` | String | 카드 내부 컴포넌트 ID |

**예시**:
```json
{
  "id": "user-card",
  "component": {
    "Card": {
      "child": "card-content"
    }
  }
},
{
  "id": "card-content",
  "component": {
    "Column": {
      "children": {"explicitList": ["user-avatar", "user-name", "user-email"]}
    }
  }
}
```

### 5.2 Modal (모달)

오버레이 다이얼로그입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `entryPointChild` | String | 모달을 여는 요소 ID |
| `contentChild` | String | 모달 콘텐츠 ID |

**예시**:
```json
{
  "id": "settings-modal",
  "component": {
    "Modal": {
      "entryPointChild": "open-settings-btn",
      "contentChild": "settings-content"
    }
  }
},
{
  "id": "open-settings-btn",
  "component": {
    "Button": {
      "child": "btn-text",
      "action": {"name": "open_modal"}
    }
  }
}
```

### 5.3 Tabs (탭)

탭 인터페이스입니다.

**속성**:

| 속성 | 타입 | 설명 |
|------|------|------|
| `tabItems` | Array | 탭 항목 배열 |

**tabItems 구조**:
```json
{
  "title": "탭 제목",
  "child": "탭-콘텐츠-컴포넌트-ID"
}
```

**예시**:
```json
{
  "id": "main-tabs",
  "component": {
    "Tabs": {
      "tabItems": [
        {"title": "홈", "child": "home-content"},
        {"title": "프로필", "child": "profile-content"},
        {"title": "설정", "child": "settings-content"}
      ]
    }
  }
}
```

---

## 6. 공통 속성

### 6.1 weight (Flex 가중치)

부모가 Row/Column일 때 공간 비율을 지정합니다.

**예시**:
```json
{
  "id": "sidebar",
  "component": {
    "Column": {...},
    "weight": 1
  }
},
{
  "id": "main-content",
  "component": {
    "Column": {...},
    "weight": 3
  }
}
```

→ 사이드바 25%, 메인 콘텐츠 75%

---

## 7. 실습: 컴포넌트 조합

### 예제 1: 로그인 폼

```json
{
  "surfaceUpdate": {
    "surfaceId": "login-form",
    "components": [
      {
        "id": "form-container",
        "component": {
          "Card": {"child": "form-content"}
        }
      },
      {
        "id": "form-content",
        "component": {
          "Column": {
            "children": {"explicitList": ["title", "email", "password", "remember", "submit"]}
          }
        }
      },
      {
        "id": "title",
        "component": {
          "Text": {
            "text": {"literalString": "로그인"},
            "usageHint": "h1"
          }
        }
      },
      {
        "id": "email",
        "component": {
          "TextField": {
            "label": {"literalString": "이메일"},
            "text": {"path": "/login/email"},
            "textFieldType": "shortText"
          }
        }
      },
      {
        "id": "password",
        "component": {
          "TextField": {
            "label": {"literalString": "비밀번호"},
            "text": {"path": "/login/password"},
            "textFieldType": "obscured"
          }
        }
      },
      {
        "id": "remember",
        "component": {
          "Checkbox": {
            "label": {"literalString": "로그인 상태 유지"},
            "value": {"path": "/login/remember"}
          }
        }
      },
      {
        "id": "submit",
        "component": {
          "Button": {
            "child": "submit-text",
            "primary": true,
            "action": {"name": "login"}
          }
        }
      },
      {
        "id": "submit-text",
        "component": {
          "Text": {"text": {"literalString": "로그인"}}
        }
      }
    ]
  }
}
```

### 예제 2: 상품 카드 리스트

```json
{
  "surfaceUpdate": {
    "surfaceId": "product-list",
    "components": [
      {
        "id": "list-container",
        "component": {
          "List": {
            "children": {
              "template": {
                "dataBinding": "/products",
                "componentId": "product-card"
              }
            }
          }
        }
      },
      {
        "id": "product-card",
        "component": {
          "Card": {"child": "card-content"}
        }
      },
      {
        "id": "card-content",
        "component": {
          "Column": {
            "children": {"explicitList": ["product-image", "product-name", "product-price", "add-cart"]}
          }
        }
      },
      {
        "id": "product-image",
        "component": {
          "Image": {"url": {"path": "/imageUrl"}}
        }
      },
      {
        "id": "product-name",
        "component": {
          "Text": {
            "text": {"path": "/name"},
            "usageHint": "h3"
          }
        }
      },
      {
        "id": "product-price",
        "component": {
          "Text": {
            "text": {"path": "/price"},
            "usageHint": "body"
          }
        }
      },
      {
        "id": "add-cart",
        "component": {
          "Button": {
            "child": "cart-btn-text",
            "action": {"name": "add_to_cart"}
          }
        }
      },
      {
        "id": "cart-btn-text",
        "component": {
          "Text": {"text": {"literalString": "장바구니 추가"}}
        }
      }
    ]
  }
}
```

---

## 📝 실습 체크리스트

### 필수 과제

- [ ] Row와 Column의 distribution 옵션 비교
- [ ] TextField 타입별 차이 확인
- [ ] Button action 설정 및 userAction 확인
- [ ] Card와 Modal 구현

### 도전 과제

- [ ] 복잡한 폼 (5개 이상 입력 필드) 구현
- [ ] Tabs를 사용한 다중 페이지 UI
- [ ] 동적 리스트와 템플릿 활용

---

## 🔗 다음 단계

- [06. 실제 사용 시나리오](./06-practical-scenarios.md) → 프로덕션 적용 가이드

---

## 📚 참고 자료

- [A2UI Component Reference](https://a2ui.org/reference/components/)
- [Standard Catalog Definition](https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json)
- [Component Gallery Demo](https://a2ui.org/composer/)
