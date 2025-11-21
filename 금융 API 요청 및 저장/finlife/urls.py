from django.urls import path
from . import views

urlpatterns = [
    # F01: 데이터 수집 API
    path('save-products/', views.save_deposit_products), 
    
    # F02, F03: 상품 목록 조회 API 
    path('deposit-products/', views.deposit_products),

    # F04: 특정 상품 옵션 리스트 출력 API (방금 추가)
    # <str:fin_prdt_cd> 부분이 URL에서 상품 코드를 변수로 잡아줍니다.
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options),

    # F05: 최고 금리 상품 조회 API (방금 추가)
    path('top-rate/', views.top_rate_product),
]