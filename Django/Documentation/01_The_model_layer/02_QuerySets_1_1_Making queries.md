# Django_The model layer 정리

### QuerySets: Executing queries

<br>

*__Making queries__*

- **데이터 모델** 을 만들면 Django는 자동으로 객체를 생성, 검색, 업데이트 및 삭제할 수있는 **데이터베이스 추상화 API(!)**를 제공합니다. 이 문서는이 API를 사용하는 방법을 설명합니다.

<br>

*__Creating objects__*

- Django는 **Python 객체**에서 **데이터베이스 테이블 데이터**를 나타 내기 위해 **직관적인 시스템**을 사용합니다. **모델 클래스**는 **데이터베이스 테이블**을 나타내며 **클래스의 인스턴스**는 데이터베이스 테이블의 **특정 레코드**(한 행)를 나타냅니다.
- 오브젝트를 작성하기 위해서는 `모델 클래스`에 **키워드 인수**를 사용하여 오브젝트를 `인스턴스화` 한 후 호출 save()하여 데이터베이스에 저장하십시오.
	
	> 파이썬에서 클래스 만들고 인스턴스 생성하던 것과 같이
	
- `save()`
	- 객체를 데이터베이스에 저장
	- 사용에 따라 뒤에서 INSERT SQL문도 수행하고 UPDATE 문도 수행하고
	- Django는 명시적으로 `save()`를 호출 할 때까지 데이터베이스에 접근하지 않음 (저장(INSERT)하지 않음)
	- 반환값(return value) 없음
	- [save() 고급옵션](https://docs.djangoproject.com/en/1.11/ref/models/instances/#saving-objects)
	- 단일 단계(객체 생성 - `save()` 하지않고)로 하려면, `create()`

-

*__Saving changes to objects__*

- Saving ForeignKey and ManyToManyField fields

	- ForeignKey
		- 올바른 유형의 객체를 할당하기만 하면 됨
	- ManyToManyfield
		- `add()` 사용
		- `add(obj1, obj2, obj3, obj4)`(여러개 인자)로도 사용 가능

-

*__Retrieving objects__*

- 데이터베이스에서 객체를 검색하려면 모델 클래스의 Manager를 통해 QuerySet을 생성하십시오.

- QuerySet는 **데이터베이스의 객체 컬렉션**을 나타냅니다. 0 개, 하나 또는 여러 개의 필터를 가질 수 있습니다. 필터는 주어진 매개 변수를 기반으로 쿼리 결과의 범위를 좁 힙니다. SQL 용어에서 **QuerySet은 SELECT 문**과 같으며 **필터는 WHERE 또는 LIMIT와 같은 제한 절**입니다.
- 모델의 Manager를 사용하여 QuerySet을 얻습니다. 각 모델에는 최소한 하나의 Manager가 있으며 기본적으로 **objects**라고합니다. 다음과 같이 모델 클래스를 통해 직접 액세스하십시오.
- Manager는 **모델 인스턴스**가 아닌 **모델 클래스**를 통해서만 액세스 할 수 있으므로 "테이블 수준(!)"작업과 "레코드 수준(!)"작업을 구분할 수 있습니다.
- QuerySet...Query의 반환결과를 Set로 반환한다는 말 같은데...

-

*__Retrieving specific objects with filters__*

- `all()`에 의해 반환 된 QuerySet은 데이터베이스 테이블의 **모든 객체를 설명**합니다. 그러나 일반적으로 개체의 전체 집합 중 일부만 선택해야합니다.
	- `filter(**kwargs)`
		- 지정된 검색 매개 변수와 **일치하는(match)** 객체가 **포함된(containing)** 새 QuerySet을 반환합니다.
	- `exclude(**kwargs)`
		- 지정된 조회 매개 변수와 **일치하지 않는(not match)** 객체가 포함된 새 QuerySet을 반환합니다.

	- 위의 함수 정의에서 조회 매개 변수 (** kwargs)는 아래의 필드 조회에서 설명하는 형식이어야합니다.

	> [Field lookups_필드 조회 방식](https://docs.djangoproject.com/en/1.11/topics/db/queries/#field-lookups)
	
- Chaining filters

	- 필터를 연결해서 사용할수도 있다.(상세검색)

-

*__Filtered QuerySets are unique__*

- Chaining filteres 하더라도 각 filter(또는 exclude) QuerySet은 고유하다.(서로 영향을 주지 않는다. 검색값 안에서 또 검색값을 찾고, 그 검색값 안에서 또 검색 값을 찾고 하는 방식으로 움직인다.)

-

*__QuerySets are lazy__*

- QuerySet을 생성하는 행위는 어떤 **데이터베이스 활동**도 포함하지 않는다. QuerySet이 **평가 될 때** 까지 쿼리를 실행하지 않는다.
- [QuerySet 평가시기_When QuerySets are evaluated.](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#when-querysets-are-evaluated)

-

*__Retrieving a single object with get()__*

- `get()`
	- 단일 객체(single object) 반환
	- filter() 처럼 query expression 사용 가능
	- 없거나 하나 이상이면 오류

-

*__Other QuerySet methods__*

- 대부분 all(), get(), filter(), exclude()를 사용하지만, 또 많음. 
	- [QuerySet API Reference](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#queryset-api)

-

*__Limiting QuerySets__*

- python의 슬라이스를 이용해 LIMIT 와 OFFSET 같이 사용하기
	- (LIMIT 5)
	
		```
		>>> Entry.objects.all()[:5]
		```
		
	- (OFFSET 5 LIMIT 5)

		```
		>>> Entry.objects.all()[5:10]
		```
		
	- `Entry.objects.all()[-1]`은 지원 안함
	- 일반적으로 QuerySet을 슬라이스하면 새 QuerySet가 반환됩니다. **쿼리를 평가하지는 않습니다.** 예외는 파이썬 슬라이스 구문의 "step"매개 변수를 사용하는 경우입니다. 예를 들어 **첫 번째 10 번째 두 번째 객체 목록을 반환하기 위해 실제로 쿼리를 실행합니다.**

		```
		>>> Entry.objects.all()[:10:2]
		```
		
	- 목록이 아닌 단일 객체를 검색하려면 (예 : SELECT foo FROM bar LIMIT 1) 슬라이스 대신 간단한 색인을 사용하십시오. 예를 들어, 항목을 제목순으로 알파벳 순으로 정렬 한 후 데이터베이스의 첫 번째 항목을 반환합니다.

		```
		>>> Entry.objects.order_by('headline')[0]
		```
		```
		위와 동일...
		>>> Entry.objects.order_by('headline')[0:1].get()
		```
		
	- 그러나 첫 번째는 IndexError를 발생시키고 두 번째는 지정된 기준과 일치하는 객체가없는 경우 DoesNotExist를 발생시킵니다.

-

*__Field lookups__*

> 가장 관심있던...!!! 어떤 필드조회값이 SQL의 어떤 것과 같은지...
> 

- 기본 형태

	```
	field__lookuptype=value
	(double-underscore)
	```
	
	- `__lte`: <=

- [약 20개의 조회 유형을 지원](https://docs.djangoproject.com/en/1.11/ref/models/querysets/#field-lookups)하지만, 일반적으로 사용되는 것들

	- `exact`: = (정확한 일치)
	- `iexact`: 대소문자를 구분하지 않는 일치
	- `__contains=s`: `LIKE %s%` (대소문자 구분)
	- `icontains`: 대소문자를 구분하지 않는 LIKE
	- `startswith`,`endswith`
	- `istartswith`,`iendswith`

-

*__Lookups that span relationships__*

- Django는 백그라운드에서 자동으로 SQL JOIN을 처리하면서 조회에서 관계를 "따르는"강력하고 직관적 인 방법을 제공합니다. 관계를 확장하려면 원하는 필드를 찾을 때까지 **두 모델 모두에서 관련 필드의 필드 이름을 두 개의 밑줄로 구분하여 사용하십시오.**

	```
	>>> Entry.objects.filter(blog__name='Beatles Blog')
	```

- '역'관계는 소문자

	```
	>>> Blog.objects.filter(entry__headline__contains='Lennon')
	```
	
- 여러 관계를 거쳐 필터링하고 중간 모델 중 하나가 필터 조건을 만족하는 값을 가지지 않는다면 Django는 이것을 공백 (모든 값은 NULL 임)으로 처리하지만 유효합니다. 이 모든 것은 오류가 발생하지 않는다는 것을 의미합니다. 예를 들어이 필터에서 다음을 수행합니다.
- (관련 작성자 모델이있는 경우) 항목과 연관된 작성자가없는 경우 누락 된 작성자로 인해 오류가 발생하지 않고 이름이 첨부 된 것처럼 처리됩니다. 대개 이것은 정확히 당신이 원하는 것입니다. 혼란 스러울 수있는 유일한 경우는 isnull을 사용하는 경우입니다. 그러므로:

	```
	>>> Blog.objects.filter(entry__authors__name__isnull=True)
	```
	
-

*__Spanning multi-valued relationships__*

- 그냥... ManyToManyField 이건 역참조 ForeignKey던 위와 같던 방식으로 다 된다?는... 아닌거 같은데 일단 패스
- `filter()` 할때 (조건,조건) 이면 and / (조건).filter(조건) 는 말그대로 두번 필터링. 첫번째 실행 쿼리 결과 한번, 두번째 실행 쿼리 결과 한번
- (조건).filter(조건) 는 쿼리를 따로 실행하기 때문이다.
- `filter(조건, 조건)`와 `exclude(조건, 조건)` 의 작동 방식이 다르다.

-

*__Filters can reference fields on the model__*

- 지금까지는 필드와 상수, 하지만 모델 필드의 값을 같은 모델의 다른 필드와 비교하고 싶다면...?
	- F expressions, F()

- 예를 들어 pingback보다 많은 comment가있는 모든 블로그 항목의 목록을 찾으려면 핑백 수를 참조하는 F () 객체를 생성하고 쿼리에서 해당 F () 객체를 사용합니다.

	```
	>>> from django.db.models import F
	>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks'))
	```
	
- Django는 상수와 다른 F () 객체와 함께 F () 객체를 사용하여 덧셈, 뺄셈, 곱셈, 나눗셈, 모듈러스 및 지수 연산을 지원합니다. pingback보다 2 배 많은 주석이있는 모든 블로그 항목을 찾으려면 다음과 같이 쿼리를 수정하십시오.(연산식 사용 가능/비트연산도 가능)

	```
	>>> Entry.objects.filter(n_comments__gt=F('n_pingbacks') * 2)
	```
	
- 날짜 및 날짜 / 시간 필드의 경우 timedelta 객체를 더하거나 뺄 수 있습니다. 다음은 게시 된 후 3 일 이상 수정 된 모든 항목을 반환합니다.
	
	```
	>>> from datetime import timedelta
	>>> Entry.objects.filter(mod_date__gt=F('pub_date') + timedelta(days=3))
	```
	
-

*__The pk lookup shortcut__*

```
>>> Blog.objects.get(id__exact=14) # Explicit form
>>> Blog.objects.get(id=14) # __exact is implied
>>> Blog.objects.get(pk=14) # pk implies id__exact
```
```
# Get blogs entries with id 1, 4 and 7
>>> Blog.objects.filter(pk__in=[1,4,7])

# Get all blog entries with id > 14
>>> Blog.objects.filter(pk__gt=14)
```
```
>>> Entry.objects.filter(blog__id__exact=3) # Explicit form
>>> Entry.objects.filter(blog__id=3)        # __exact is implied
>>> Entry.objects.filter(blog__pk=3)        # __pk implies __id__exact
```

-

*__Escaping percent signs and underscores in LIKE statements__*

- LIKE 문 (iexact, contains, icontains, startswith, endswith 및 iendswith)과 같은 필드 조회는 LIKE 문에 사용 된 두 개의 특수 문자 (백분율 기호 및 밑줄)를 **자동으로 이스케이프**합니다. 

-

*__Caching and QuerySets__*

