
## 💡 기술 블로그 포스팅용: Kakao Map API 로딩 문제 완벽 분석 및 해결

### 1\. 문제 정의 및 목표

저희 프로젝트의 목표는 **순수 바닐라 JS** 환경에서 Kakao Map API를 활용하는 것이었습니다. 이 과정에서 두 가지 상충되는 목표 때문에 핵심적인 기술 오류에 직면했습니다.

  * **보안 목표 :** API Key 값을 `index.html`에 직접 노출하지 않고, 별도의 파일(`js/apikey.js`)에 변수(`API_KEY`)로 보관하여 사용한다.
  * **구조 목표 (명세서 NF03):** 지도 초기화 로직은 `js/main.js` 파일에 분리하여 작성한다.

#### 🚨 발생한 주요 오류

1.  **`Uncaught ReferenceError: API_KEY is not defined`**: HTML `<script>` 태그에서 `API_KEY` 변수를 사용할 때, 변수가 정의된 `apikey.js` 파일 로딩 전에 해당 변수를 참조하여 발생.
2.  **`Uncaught ReferenceError: kakao is not defined`**: `main.js`에서 `kakao.maps.load()`를 호출할 때, 핵심 API 라이브러리(Kakao SDK) 로드가 완료되지 않아 `kakao` 전역 객체를 찾지 못해 발생.

-----

### 2\. 오류 원인 분석: 프론트엔드 비동기 로딩의 딜레마

HTML 파일 하단에 `<script src="..."></script>` 태그를 여러 개 넣으면, 브라우저는 위에서부터 아래로 순차적으로 스크립트를 요청합니다. 하지만 이 요청은 **비동기적으로 처리**되며, 외부 스크립트 파일의 **로딩 완료 시점**이 보장되지 않습니다.

| 파일 | 역할 | 로딩 이슈 |
| :--- | :--- | :--- |
| **`js/apikey.js`** | `API_KEY` 변수 정의 | 1번 스크립트에서 변수를 정의하기 전에 2번 스크립트 로더가 변수를 참조하여 `API_KEY is not defined` 발생. |
| **Kakao SDK** | `kakao` 객체 정의 | 3번 스크립트(`main.js`)가 실행될 때 2번 스크립트 로드가 완료되지 않아 `kakao is not defined` 발생. |
| **`js/main.js`** | 지도 초기화 로직 | 로딩 순서상 가장 먼저 실행되지만, 필수 전역 객체(`kakao`)가 준비되지 않아 오류 발생. |

**핵심:** HTML의 `<script src>`만으로는 **외부 라이브러리의 로드 완료 시점**을 정확하게 제어할 수 없습니다.

-----

### 3\. 해결 전략: 동적 로딩과 `onload` 이벤트 핸들링

이 문제를 해결하고 **보안/구조/안정성** 세 마리 토끼를 모두 잡는 방법은 **스크립트 태그를 동적으로 생성하고 `onload` 이벤트를 사용하여 실행 순서를 강제**하는 것입니다.

#### 🚀 단계별 해결 논리

1.  **`API_KEY` 변수 사용 보장:** 인라인 `<script>` 블록 안에서 `API_KEY` 변수를 사용하여 Kakao SDK URL을 동적으로 생성합니다. 이렇게 하면 `ReferenceError` 없이 변수 사용 원칙을 지킬 수 있습니다.
2.  **SDK 로드 완료 감지:** 동적으로 생성한 스크립트 태그에 **`onload` 이벤트 리스너**를 부착합니다. 이 리스너는 Kakao SDK 파일 다운로드 및 실행이 **완벽하게 끝난 시점**에만 호출됩니다.
3.  **`main.js` 실행 제어:** `onload` 이벤트 내부에서 `js/main.js` 파일을 **동적으로 로드**합니다. 이로써 `main.js`가 실행되는 시점은 `kakao` 객체가 정의된 후로 **강제**됩니다.

-----

### 4\. 최종 코드 구조

#### 🌐 `index.html` (로딩 및 순서 제어)

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>PJT08 - 은행 검색 애플리케이션</title>
    <link rel="stylesheet" href="css/style.css"> 
    
    <script src="js/apikey.js"></script>
</head>
<body>
    <div id="map" style="width:700px;height:500px;"></div>

    <script>
        // F02 핵심: API_KEY 변수를 사용하고 main.js 실행 시점을 제어합니다.
        if (typeof API_KEY !== 'undefined') {
            
            // 2. Kakao SDK 스크립트 태그 동적 생성 및 API_KEY 변수 사용
            const mapScript = document.createElement('script');
            mapScript.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&autoload=false`;
            
            // 3. SDK 로드가 완료된 후, main.js를 로드하여 실행합니다.
            mapScript.onload = () => {
                const mainScript = document.createElement('script');
                mainScript.src = 'js/main.js';
                document.body.appendChild(mainScript);
            };
            
            document.head.appendChild(mapScript);
        } else {
             // 디버깅 용도
             console.error('API_KEY 변수를 찾을 수 없습니다.');
        }
    </script>
    
    </body>
</html>
```

#### 🗺️ `js/main.js` (지도 초기화 로직)

```javascript
// js/main.js

// 이제 이 파일은 Kakao API 로드가 완료된 후에만 실행됨이 보장됩니다.
kakao.maps.load(() => {
    var container = document.getElementById('map');
    
    var options = {
        // 요구사항: 강남역 좌표
        center: new kakao.maps.LatLng(37.49818, 127.027386), 
        level: 3
    };

    // F02 완료
    const map = new kakao.maps.Map(container, options);
    window.mapInstance = map; // 이후 F04, F05를 위해 map 객체를 저장

    console.log("✅ F02 기능 구현 완료: 지도 정상 출력");
    
    // F03 로직 (검색 UI)을 여기에 추가합니다.
});
```

이 해결책은 **순수 바닐라 JS 환경**에서 API Key 보안과 코드 구조화 원칙을 모두 만족시키는 표준적이고 안정적인 방식입니다. 이제 다음 단계인 **F03 (은행 검색 UI 구성)** 개발을 진행해 주십시오.