## 🛠️ 환경 변수 (`API_KEY`) 로드 실패 트러블슈팅 보고서

| 구분 | 내용 |
| :--- | :--- |
| **프로젝트** | Django REST API 서버 (금융 상품 데이터 수집) |
| **대상 기능** | 외부 금융 API 데이터 수집 및 DB 저장 (`/finlife/save-products/`) |

-----

### 1\. 🔍 문제 상황: DB 저장 실패 (Data Flow Block)

API 호출 및 DB 저장을 담당하는 엔드포인트 (`/finlife/save-products/`)에 **GET 요청을 보냈으나**, 데이터 수집 로직이 실행되기 전에 서버가 **중단**되었습니다.

  * **발생 오류**: 서버 시작 또는 요청 시, 환경 변수를 설정하지 못했다는 오류 발생.
  * **구체적인 오류 메시지**: `django.core.exceptions.ImproperlyConfigured: Set the API_KEY environment variable`
  * **결과**: API Key가 시스템에 로드되지 않아, **API 요청을 보낼 수 없었으며** 데이터베이스에 데이터를 저장할 수 없었습니다.

-----

### 2\. 💡 원인 분석: 환경 설정 파일 경로 불일치

`django-environ` 라이브러리를 통해 환경 변수를 로드하려 했으나, **`.env` 파일의 경로를 잘못 인식**하여 발생한 문제입니다.

1.  **설정 파일 위치**: `config/settings.py` 파일이 실행될 때 `API_KEY` 로드를 시도합니다.
2.  **라이브러리 기본 동작**: `django-environ`은 `.env` 파일을 \*\*`settings.py`가 위치한 디렉토리(`config/`)\*\*에서 찾는 것이 기본 설정입니다.
3.  **경로 불일치**: 실제 **`.env` 파일은 프로젝트의 루트 디렉토리**(`/07-pjt/`)에 위치하고 있었습니다.

$\rightarrow$ **결론**: **파일 로드 시점에 `.env` 파일의 정확한 경로를 명시적으로 알려주지 않아** 환경 변수 로드가 실패했습니다.

-----

### 3\. 🚀 해결 방법: `BASE_DIR`을 활용한 경로 명시

Django의 내장 경로 변수인 `BASE_DIR`을 사용하여 `.env` 파일이 존재하는 **프로젝트 루트 경로를 명확하게 지정**함으로써 문제를 해결했습니다.

#### 🔨 조치 코드 (`config/settings.py` 수정)

```python
# config/settings.py (상단 환경 변수 로드 부분)

# BASE_DIR 변수 (프로젝트 루트 디렉토리)
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. env 객체 생성
env = environ.Env() 

# 2. FIX: BASE_DIR과 .env 파일명을 결합하여 정확한 경로를 지정
environ.Env.read_env(BASE_DIR / '.env') 

# 3. API_KEY 로드 (성공)
API_KEY = env('API_KEY')
```

#### ✅ 최종 결과

`environ.Env.read_env()`에 `BASE_DIR`을 인수로 전달하여 `.env` 파일의 **정확한 위치를 명시**했습니다. 이로 인해 `API_KEY`가 **성공적으로 시스템에 로드**되었으며, 서버가 정상적으로 시작되었습니다. 이후 `/finlife/save-products/` 요청 시 **API 호출 및 DB 저장이 모두 정상적으로 완료**되었습니다.