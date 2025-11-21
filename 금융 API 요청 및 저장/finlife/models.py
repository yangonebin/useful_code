from django.db import models

# 1. 정기예금 상품 정보 모델 (DepositProducts)
# API로부터 수집된 상품의 기본 정보를 저장합니다.
class DepositProducts(models.Model):
    # 금융상품 코드 (Primary Key로 사용 가능)
    fin_prdt_cd = models.CharField(max_length=200, unique=True) 
    # 금융회사명
    kor_co_nm = models.CharField(max_length=100)
    # 금융상품명
    fin_prdt_nm = models.CharField(max_length=200)
    # 가입 방법
    join_way = models.TextField()
    # 가입 대상
    join_member = models.TextField()
    # 가입 제한 (1:제한없음, 2:서민전용, 3:일부제한)
    join_deny = models.IntegerField(default=1) 
    # 최고 한도 (만약 없다면 null=True, blank=True)
    max_limit = models.IntegerField(null=True, blank=True)
    # 기타 유의사항 (특이사항 등)
    etc_note = models.TextField()
    # 우대 조건
    spcl_cnd = models.TextField()

    def __str__(self):
        return f'[{self.kor_co_nm}] {self.fin_prdt_nm}'


# 2. 정기예금 옵션 정보 모델 (DepositOptions)
# 상품별 금리 옵션 정보를 저장하며, DepositProducts를 참조합니다.
class DepositOptions(models.Model):
    # 외래키 설정: DepositProducts 모델을 참조합니다. 
    # on_delete=models.CASCADE 설정으로, 상품이 삭제되면 옵션도 함께 삭제됩니다.
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options') 
    
    # 저축 기간 (6, 12, 24, 36개월 등)
    save_trm = models.IntegerField()
    # 저축 금리
    intr_rate = models.FloatField(default=-1) 
    # 최고 우대금리 (요구사항 F05의 기준)
    intr_rate2 = models.FloatField(default=-1)
    # 저축금리 유형 ('S':단리, 'M':월복리)
    intr_rate_type = models.CharField(max_length=1)
    # 저축금리 유형명
    intr_rate_type_nm = models.CharField(max_length=50)

    class Meta:
        # 두 필드를 조합하여 중복을 방지합니다. (같은 상품에 같은 기간 옵션이 중복되지 않도록)
        unique_together = ('product', 'save_trm')
    
    def __str__(self):
        return f'{self.product.fin_prdt_nm} - {self.save_trm}개월 옵션'