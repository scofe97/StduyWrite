# 모듈 시스템 (Module Systems)

## 개요

**정의**: 모듈 시스템은 코드를 독립적인 단위로 분리하고, 의존성을 관리하며, 전역 네임스페이스 오염을 방지하는 구조화 방법이다.

**목적**: 코드 재사용성, 유지보수성, 캡슐화를 달성하고 대규모 애플리케이션의 복잡성을 관리한다.

---

## 핵심 개념

### 모듈 시스템 발전 역사

```
1995: JavaScript 탄생 (모듈 시스템 없음)
    │
2009: CommonJS 시작 (ServerJS)
    │
2010: AMD 제안 + RequireJS 등장
    │
2011: UMD 등장 (범용 호환)
    │
2015: ES2015 Modules (네이티브 표준)
    │
2020s: ESM 표준화, 대부분 전환
```

### 모듈 시스템 비교

| 특성 | AMD | CommonJS | UMD | ES Modules |
|------|-----|----------|-----|------------|
| **로딩** | 비동기 | 동기 | 환경 감지 | 비동기 |
| **환경** | 브라우저 | Node.js | 둘 다 | 둘 다 |
| **문법** | define/require | require/exports | IIFE 래퍼 | import/export |
| **현재 상태** | 레거시 | npm 생태계 | 라이브러리 배포 | **표준** |

---

## AMD (Asynchronous Module Definition)

### AMD 개념

AMD는 ES2015 이전에 브라우저에서 비동기적으로 모듈을 로드하기 위해 만들어진 포맷이다.

**핵심 특징**:
- define()으로 모듈 정의
- require()로 의존성 로드
- RequireJS, curl.js 등 스크립트 로더 필요
- jQuery, Dojo, Backbone.js 등에서 채택

### AMD 기본 문법

```javascript
// define(module_id, [dependencies], factory)
define("myModule",
    ["foo", "bar"],
    function(foo, bar) {
        var myModule = {
            doStuff: function() {
                foo.doSomething();
                bar.doSomethingElse();
            }
        };
        return myModule;
    }
);

// 익명 모듈 (권장)
define(["math", "graph"], function(math, graph) {
    return {
        plot: function(x, y) {
            return graph.drawPie(math.randomGrid(x, y));
        }
    };
});
```

### AMD 의존성 로드

```javascript
// require로 의존성 로드
require(["foo", "bar"], function(foo, bar) {
    foo.doSomething();
    bar.doSomethingElse();
});

// 플러그인으로 다양한 리소스 로드
define([
    "./templates",
    "text!./template.html",
    "css!./styles.css"
], function(templates, templateHtml) {
    // 템플릿으로 작업
});
```

### AMD 장단점

| 장점 | 단점 |
|------|------|
| 비동기 로딩 | define() 보일러플레이트 |
| 전역 오염 방지 | 스크립트 로더 필요 |
| 브라우저 네이티브 실행 | 복잡한 설정 |
| 지연 로딩 지원 | ES Modules로 대체됨 |

---

## CommonJS

### CommonJS 개념

CommonJS는 Node.js에서 사용하는 동기적 모듈 시스템이다.

**핵심 특징**:
- require()로 모듈 가져오기
- exports/module.exports로 내보내기
- 동기적 로딩 (파일 시스템 기반)
- 한 번 로드된 모듈은 캐시됨

### CommonJS 기본 문법

```javascript
// math.js - exports 객체 사용
exports.add = function(a, b) {
    return a + b;
};

exports.subtract = function(a, b) {
    return a - b;
};

// main.js
var math = require('./math');
console.log(math.add(2, 3)); // 5
```

```javascript
// calculator.js - module.exports 사용
function Calculator() {
    this.value = 0;
}

Calculator.prototype.add = function(num) {
    this.value += num;
    return this;
};

module.exports = Calculator;

// main.js
var Calculator = require('./calculator');
var calc = new Calculator();
console.log(calc.add(10).value); // 10
```

### exports vs module.exports

**핵심 규칙**:
- `exports`는 `module.exports`의 참조(alias)
- `require()`가 반환하는 것은 항상 `module.exports`
- `exports`에 직접 할당하면 참조가 끊어짐

```javascript
// ❌ 잘못된 사용 - exports 참조 끊어짐
exports = function() {
    console.log("This won't work!");
};

// ✅ 올바른 사용
module.exports = function() {
    console.log("This works!");
};

// ✅ 올바른 사용
exports.myFunction = function() {
    console.log("This also works!");
};
```

### CommonJS vs AMD

| 특성 | AMD | CommonJS |
|------|-----|----------|
| 로딩 방식 | 비동기 | 동기 |
| 주요 환경 | 브라우저 | Node.js (서버) |
| 문법 복잡도 | 복잡 (define 래퍼) | 단순 (require/exports) |
| 로더 필요 | 필수 (RequireJS 등) | 불필요 (Node 내장) |

---

## UMD (Universal Module Definition)

### UMD 개념

UMD는 AMD, CommonJS, 전역 변수 모두를 지원하는 범용 패턴이다.

**사용 시기**:
- 다양한 환경에서 동작하는 라이브러리 배포
- CDN 배포가 필요한 경우
- 레거시 환경 지원

### UMD 기본 패턴

```javascript
(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD 환경
        define(['dependency'], factory);
    } else if (typeof exports === 'object') {
        // CommonJS 환경
        module.exports = factory(require('dependency'));
    } else {
        // 전역 변수 (브라우저)
        root.myModule = factory(root.dependency);
    }
}(typeof self !== 'undefined' ? self : this, function(dependency) {
    return {
        doSomething: function() {
            return dependency.someMethod();
        }
    };
}));
```

### UMD jQuery 플러그인

```javascript
(function(factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = function(root, jQuery) {
            if (jQuery === undefined) {
                jQuery = require('jquery');
            }
            factory(jQuery);
            return jQuery;
        };
    } else {
        factory(jQuery);
    }
}(function($) {
    'use strict';

    $.fn.highlight = function(options) {
        var settings = $.extend({
            color: 'yellow',
            duration: 1000
        }, options);

        return this.each(function() {
            $(this).css('background-color', settings.color);
        });
    };
}));
```

---

## 네임스페이스 패턴

### 네임스페이스 필요성

JavaScript는 네이티브 네임스페이스를 지원하지 않아 전역 충돌 문제가 발생한다. 객체와 클로저를 사용해 유사한 효과를 얻을 수 있다.

### 1. 단일 전역 변수 패턴

```javascript
const myUniqueApplication = (() => {
    function myMethod() {
        console.log("Private method");
    }

    function anotherMethod() {
        console.log("Another method");
    }

    return {
        myMethod,
        anotherMethod
    };
})();

myUniqueApplication.myMethod();
```

### 2. 객체 리터럴 네임스페이싱

```javascript
const myApplication = {
    getInfo() {
        return "Application Info";
    },

    models: {},
    views: { pages: {} },

    config: {
        language: "english",
        debug: false
    }
};

// 네임스페이스 존재 확인
const myApplication = myApplication || {};
```

### 3. 중첩 네임스페이싱

```javascript
const myApp = myApp || {};

myApp.routers = myApp.routers || {};
myApp.model = myApp.model || {};
myApp.model.special = myApp.model.special || {};

// 로컬 참조로 성능 최적화
const canvas2d = myApp.utilities.drawing.canvas['2d'];
canvas2d.drawCircle(x, y, r);
canvas2d.drawRect(x, y, w, h);
```

### 4. IIFE 네임스페이스 확장

```javascript
;((namespace, undefined) => {
    const foo = "foo";

    namespace.foobar = "foobar";

    namespace.sayHello = () => {
        speak("hello world");
    };

    function speak(msg) {
        console.log(`You said: ${msg}`);
    }

})(window.namespace = window.namespace || {});
```

### 5. 네임스페이스 주입

```javascript
const myApp = myApp || {};
myApp.utils = {};

(function() {
    let val = 5;

    this.getValue = () => val;
    this.setValue = newVal => { val = newVal; };

}).apply(myApp.utils);

console.log(myApp.utils.getValue()); // 5
```

### 6. 자동 중첩 네임스페이싱

```javascript
function extend(ns, ns_string) {
    const parts = ns_string.split(".");
    let parent = ns;

    for (let i = 0; i < parts.length; i++) {
        if (typeof parent[parts[i]] === "undefined") {
            parent[parts[i]] = {};
        }
        parent = parent[parts[i]];
    }

    return parent;
}

const myApp = {};
extend(myApp, "modules.module2");
extend(myApp, "moduleA.moduleB.moduleC");

// myApp.modules.module2, myApp.moduleA.moduleB.moduleC 자동 생성
```

### 7. 딥 객체 확장

```javascript
function extendObjects(dest, src) {
    for (const prop in src) {
        if (src[prop] && typeof src[prop] === "object" && !Array.isArray(src[prop])) {
            dest[prop] = dest[prop] || {};
            extendObjects(dest[prop], src[prop]);
        } else {
            dest[prop] = src[prop];
        }
    }
    return dest;
}

const myNamespace = {};
extendObjects(myNamespace, {
    utils: {},
    hello: { world: { wave: {} } }
});
```

---

## ES Modules (현대 표준)

### ES Modules 문법

```javascript
// ES Modules
import fs from 'fs';
import { readFile } from 'fs';
export { myFunction };
export function anotherFunction() {}
export default mainFunction;

// CommonJS 대응
const fs = require('fs');
const { readFile } = require('fs');
module.exports = { myFunction };
module.exports.anotherFunction = function() {};
```

### ES Modules vs CommonJS

| 특성 | CommonJS | ES Modules |
|------|----------|------------|
| 문법 | require/exports | import/export |
| 로딩 | 동기 (런타임) | 비동기 (정적 분석) |
| Tree Shaking | 어려움 | 네이티브 지원 |
| Top-level await | 불가능 | 가능 (ES2022) |
| 순환 참조 | 값 복사 | 라이브 바인딩 |

### Node.js 듀얼 패키지

```json
{
  "name": "my-package",
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.mjs",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    }
  }
}
```

---

## 트레이드오프

### 네임스페이스 패턴 비교

| 패턴 | 전역 오염 | 충돌 방지 | 구조화 | 권장 규모 |
|------|----------|----------|--------|----------|
| 단일 전역 변수 | 최소 | 낮음 | 기본 | 소규모 |
| 접두사 | 높음 | 중간 | 없음 | 비권장 |
| 객체 리터럴 | 최소 | 높음 | 좋음 | 중규모 |
| 중첩 | 최소 | 매우 높음 | 매우 좋음 | 대규모 |

### 모듈 시스템 선택

```yaml
CommonJS:
  - 기존 Node.js 프로젝트 유지보수
  - npm 패키지 호환성 필요
  - 동적 require() 필요한 경우

UMD:
  - 브라우저/Node.js 모두 지원하는 라이브러리
  - CDN 배포가 필요한 경우
  - 레거시 환경 지원 필요

ES_Modules:
  - 새 프로젝트 (권장)
  - Tree Shaking 필요
  - 브라우저 네이티브 지원
```

---

## 실무 적용

### 마이그레이션 전략

```yaml
AMD_to_ESM:
  1단계:
    - 기존 AMD 모듈 구조 파악
    - 의존성 그래프 분석

  2단계:
    - Webpack/Rollup 도입
    - AMD → ES Modules 변환

  도구:
    - amd-to-es6: 자동 변환 도구
    - Webpack: AMD 모듈 번들링 지원

CommonJS_to_ESM:
  변환_규칙:
    - require() → import
    - module.exports → export default
    - exports.x → export { x }
    - __dirname → import.meta.url

  도구:
    - cjs-to-esm: 자동 변환 도구
    - esbuild: 빠른 번들링
```

### 네임스페이스 유틸리티

```javascript
const NamespaceManager = {
    create(root, path) {
        const parts = path.split('.');
        let current = root;

        for (const part of parts) {
            current[part] = current[part] || {};
            current = current[part];
        }

        return current;
    },

    extend(target, source) {
        for (const key in source) {
            if (source[key] && typeof source[key] === 'object') {
                target[key] = target[key] || {};
                this.extend(target[key], source[key]);
            } else {
                target[key] = source[key];
            }
        }
        return target;
    },

    exists(root, path) {
        const parts = path.split('.');
        let current = root;

        for (const part of parts) {
            if (!current[part]) return false;
            current = current[part];
        }

        return true;
    }
};
```

---

## 면접 포인트

**Q**: CommonJS와 ES Modules의 차이는?

**A**: CommonJS는 Node.js의 동기적 모듈 시스템으로 require/exports를 사용하고 런타임에 모듈을 로드한다. ES Modules는 JavaScript 표준으로 import/export를 사용하고 정적 분석이 가능하여 Tree Shaking을 지원한다. 순환 참조 시 CommonJS는 값 복사, ES Modules는 라이브 바인딩을 사용한다.

**Q**: UMD 패턴은 언제 사용하는가?

**A**: UMD는 AMD, CommonJS, 전역 변수를 모두 지원하는 범용 패턴이다. 다양한 환경(브라우저, Node.js, RequireJS)에서 동작해야 하는 라이브러리를 배포할 때 사용한다. 환경을 감지하여 적절한 방식으로 모듈을 노출한다.

**Q**: 네임스페이스 패턴의 목적은?

**A**: JavaScript는 네이티브 네임스페이스를 지원하지 않아 전역 변수 충돌 문제가 발생한다. 네임스페이스 패턴은 객체와 클로저를 사용해 코드를 논리적으로 그룹화하고 전역 오염을 방지한다. ES Modules가 표준이 된 현재는 필요성이 줄었지만, 레거시 환경이나 CDN 배포 시 여전히 유용하다.

---

## 참고 자료

- [Node.js Modules 문서](https://nodejs.org/api/modules.html)
- [RequireJS 공식 문서](https://requirejs.org/)
- [UMD 저장소](https://github.com/umdjs/umd)
- [MDN: ES Modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
- [Stoyan Stefanov - JavaScript Patterns](http://www.jspatterns.com/)
