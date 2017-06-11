# Django_The model layer 정리

### Models: Model field reference

<br>

*__Relationship fields__*

- Django는 관계를 나타내는 일련의 필드를 정의합니다.

*__ForeignKey__*

- **class ForeignKey(othermodel, on_delete, \*\*options)** [[source][ForeignKey source]]

- 다대일(many-to-one)관계. 위치 인수가 필요합니다. 모델이 관련 지을 수 있는 클래스입니다.

- 재귀 관계(recursive relationships, 자체와 다대일 관계가있는 객체)를 만들려면 `models.ForeignKey ('self', on_delete = models.CASCADE)`를 사용합니다.

- 아직 정의되지 않은 모델에서 관계를 작성해야하는 경우 모델 오브젝트 자체가 아닌 모델 이름을 사용할 수 있습니다.

	```
	from django.db import models
	
	class Car(models.Model):
	    manufacturer = models.ForeignKey(
	        'Manufacturer',
	        on_delete=models.CASCADE,
	    )
	    # ...
	
	class Manufacturer(models.Model):
	    # ...
	    pass
	
	```

- 이 방식으로 추상 모델에 정의된 관계는 모델이 구체적인 모델로 서브 클래싱되고 추상 모델의 app_label과 관련이없는 경우 해결됩니다.

	```
	products/models.py
	
	from django.db import models

	class AbstractCar(models.Model):
	    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
	
	    class Meta:
	        abstract = True
	```
	```
	production/models.py
	
	from django.db import models
	from products.models import AbstractCar
	
	class Manufacturer(models.Model):
	    pass
	
	class Car(AbstractCar):
	    pass
	
	# Car.manufacturer will point to `production.Manufacturer` here.
	```

- 다른 응용 프로그램에 정의 된 모델을 참조하려면 전체 응용 프로그램 레이블로 모델을 명시 적으로 지정할 수 있습니다. 예를 들어 위의 Manufacturer 모델이 production이라는 다른 애플리케이션에 정의되어있는 경우 다음을 사용해야합니다.

	```
	class Car(models.Model):
    manufacturer = models.ForeignKey(
        'production.Manufacturer',
        on_delete=models.CASCADE,
    )
	```

- 이러한 종류의 참조는 두 응용 프로그램 간의 순환 가져 오기 종속성을 해결할 때 유용 할 수 있습니다.

- 데이터베이스 인덱스는 ForeignKey에 자동으로 작성됩니다. db_index를 False로 설정하여이 기능을 비활성화 할 수 있습니다. 조인이 아닌 일관성을 위해 외부 키를 작성하거나 부분 또는 다중 컬럼 색인과 같은 대체 색인을 작성할 경우 색인의 오버 헤드를 피할 수 있습니다.

*__Database Representation__*

- 배후에서 Django는 `"_id"`를 필드 이름에 추가하여 **데이터베이스 열 이름을 만듭니다.** 위의 예에서 Car 모델의 데이터베이스 테이블에는 `manufacturer_id` 열이 있습니다. `db_column`을 지정하여 이를 명시적으로 변경할 수 있습니다. 그러나 사용자 정의 SQL을 작성하지 않으면 코드가 데이터베이스 열 이름을 처리하지 않아도됩니다. 모델 개체의 필드 이름은 항상 처리됩니다.

[ForeignKey source]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/fields/related/#ForeignKey

-

*__Arguments__*

- ForeignKey는 관계가 작동하는 방식에 대한 세부 정보를 정의하는 다른 인수를 허용합니다.

- **ForeignKey.on_delete**

	- ForeignKey가 참조하는 객체가 삭제되면 Django는 on_delete 인수로 지정된 SQL 제약 조건의 동작을 에뮬레이션합니다. 예를 들어 nullable ForeignKey가 있고 참조 된 객체가 삭제 될 때 null로 설정되기를 원할 경우 :

		```
		user = models.ForeignKey(
		    User,
		    models.SET_NULL,
		    blank=True,
		    null=True,
		)
		```
		
		> 버전 1.9에서 사용되지 않음 :  
		> on_delete는 Django 2.0에서 **필수 인수**가됩니다. 이전 버전에서는 기본적으로 CASCADE가 사용됩니다.
		
- `on_delete`에 가능한 값은 `django.db.models`에 있습니다.

	- **CASCADE**[[socure][cascade soucre]]
		- 계단식 삭제. Django는 ON DELETE CASCADE SQL 제약 조건의 동작을 에뮬레이션하고 ForeignKey가 포함 된 객체도 삭제합니다.

	- **PROTECT**[[socure][protect soucre]]
		- [`django.db.IntegrityError`][IntegrityError]의 하위 클래스 인 [`ProtectedError`][ProtectedError]를 발생시켜 **참조된 객체의 삭제를 방지**합니다.

	- **SET_NULL**[[socure][set_null soucre]]
		- [ForeignKey][Foreign] null을 설정하십시오. [null][null]이 True 인 경우에만 가능합니다.

	- **SET_DEFAULT**[[socure][set_default soucre]]
		- [ForeignKey][Foreign]를 기본값으로 설정하십시오. ForeignKey의 기본값을 설정해야합니다.

	- **SET()**[[socure][set soucre]]

		- [ForeignKey][Foreign]를 [SET()][set]에 전달 된 값으로 설정하거나 호출 가능 객체가 전달 된 경우 호출 한 결과. 대부분의 경우 `models.py`를 가져올 때 쿼리를 실행하지 않으려면 호출 가능을 전달해야합니다.

			```
			from django.conf import settings
			from django.contrib.auth import get_user_model
			from django.db import models
			
			def get_sentinel_user():
			    return get_user_model().objects.get_or_create(username='deleted')[0]
			
			class MyModel(models.Model):
			    user = models.ForeignKey(
			        settings.AUTH_USER_MODEL,
			        on_delete=models.SET(get_sentinel_user),
			    )
			```
			
	- **DO_NOTHING**[[socure][do_nothing soucre]]
		- 아무 조치도 취하지 않습니다. 데이터베이스 백엔드가 참조 무결성을 적용하면 데이터베이스 필드에 SQL ON DELETE 제약 조건을 수동으로 추가하지 않으면 [IntegrityError]가 발생합니다.
	
	

[Foreign]: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ForeignKey
	
[cascade soucre]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/deletion/#CASCADE

[protect soucre]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/deletion/#PROTECT

[IntegrityError]: https://docs.djangoproject.com/en/1.11/ref/exceptions/#django.db.IntegrityError

[ProtectedError]: https://docs.djangoproject.com/en/1.11/ref/exceptions/#django.db.models.ProtectedError

[set_null soucre]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/deletion/#SET_NULL

[null]: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.Field.null

[set_default soucre]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/deletion/#SET_DEFAULT

[set soucre]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/deletion/#SET

[set]: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.SET

[do_nothing soucre]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/deletion/#DO_NOTHING

[IntergrityError]: https://docs.djangoproject.com/en/1.11/ref/exceptions/#django.db.IntegrityError

- **ForeignKey.limit\_choices\_to**

	- `ModelForm` 또는 `admin`을 사용하여이 필드를 렌더링 할 때 이 필드에 사용할 수있는 선택 항목에 대한 제한을 설정합니다 (기본적으로 쿼리 세트의 모든 객체를 선택할 수 있음). 사전, [Q] 오브젝트 또는 호출 가능한 리턴 사전 또는 [Q] 오브젝트가 사용될 수 있습니다.
	- 예를 들면: 

		```
		staff_member = models.ForeignKey(
		    User,
		    on_delete=models.CASCADE,
		    limit_choices_to={'is_staff': True},
		)
		```
		
	- `ModelForm`의 해당 필드가 `is_staff = True `인 사용자 만 나열하도록합니다. 이것은 장고 관리자에게 도움이 될 수 있습니다.

	- 예를 들어 Python `datetime` 모듈과 함께 사용하여 날짜 범위에 따라 선택을 제한하는 경우 호출 가능 형식이 유용 할 수 있습니다. 예 :
		
		```
		def limit_pub_date_choices():
		    return {'pub_date__lte': datetime.date.utcnow()}
		
		limit_choices_to = limit_pub_date_choices
		```
		
	- `limit_choices_to`가 복잡한 쿼리에 유용한 [Q 객체][Q]를 반환하면 모델의 `ModelAdmin`에서 필드가 `raw_id_fields`에 나열되지 않은 경우에만 관리자가 사용할 수있는 선택 항목에 영향을 미칩니다.

	- 주의
		- `limit_choices_to`에 호출 된 호출이 사용되면 새 양식이 인스턴스화 될 때마다 호출됩니다. 또한 관리 명령이나 관리자와 같이 모델의 유효성을 검사 할 때 호출 될 수도 있습니다. 관리자는 다양한 엣지 경우에 폼 입력을 여러 번 검증하기 위해 쿼리 세트를 구성하므로 호출 가능 함수가 여러 번 호출 될 가능성이 있습니다.
	
[Q]: https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.Q

- *__ForeignKey.related_name__*

	- 관련 객체에서이 객체에 대한 관계에 사용할 이름입니다. 또한 `related_query_name` (대상 모델의 **역 필터 이름**에 사용할 이름)의 기본값입니다. 전체 설명과 예제는 [related objects documentation]를 참조하십시오. [abstract models]에 관계를 정의 할 때이 값을 설정해야합니다. 그렇게하면 [특별한 구문][special syntax]을 사용할 수 있습니다.

		> 역 참조 이름 !

	- Django가 뒤로 관계를 생성하지 않기를 원한다면, `related_name`을 `'+'`로 설정하거나 `'+'`로 끝내십시오. 예를 들어, 이렇게하면 User 모델이이 모델에 대한 역방향 관계를 갖지 않게됩니다.

		```
		user = models.ForeignKey(
		    User,
		    on_delete=models.CASCADE,
		    related_name='+',
		)
		```

[related objects documentation]: https://docs.djangoproject.com/en/1.11/topics/db/queries/#backwards-related-objects
	
[abstract models]: https://docs.djangoproject.com/en/1.11/topics/db/models/#abstract-base-classes	

[special syntax]: https://docs.djangoproject.com/en/1.11/topics/db/models/#abstract-related-name

- *__ForeignKey.related\_query\_name__*

	- 대상 모델에서 **역방향 필터 이름**에 사용할 이름입니다. 설정되어있는 경우 [`related_name`][related_name] 또는 [`default_related_name`][default_related_name]의 값이 기본값이며, 그렇지 않은 경우 기본값은 모델의 이름입니다.

		```
		# Declare the ForeignKey with related_query_name
		class Tag(models.Model):
		    article = models.ForeignKey(
		        Article,
		        on_delete=models.CASCADE,
		        related_name="tags",
		        related_query_name="tag",
		    )
		    name = models.CharField(max_length=255)
		
		# That's now the name of the reverse filter
		Article.objects.filter(tag__name="important")
		```
		
	- `related_name`과 마찬가지로 `related_query_name`은 [일부 특수 구문][special syntax]을 통해 앱 레이블 및 클래스 interpolation(보간법, 써넣음)을 지원합니다.

[related_name]: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ForeignKey.related_name

[default_related_name]: https://docs.djangoproject.com/en/1.11/ref/models/options/#default-related-name

- *__ForeignKey.to_field__*

	- 관계가있는 관련 객체의 필드입니다. 기본적으로 Django는 관련 객체의 기본 키를 사용합니다. 다른 필드를 참조하는 경우 해당 필드는 `unique = True`이어야합니다.

- *__ForeignKey.db_constraint__*

	- 이 외래 키에 대해 데이터베이스에 제약 조건을 만들지 여부를 제어합니다. 기본값은 True이며, 거의 확실하게 원하는 것입니다. 이것을 False로 설정하면 데이터 무결성이 매우 나쁠 수 있습니다. 즉, 다음과 같은 시나리오가 있습니다.

		- 유효하지 않은 기존 데이터가 있습니다.
		- 데이터베이스를 재구성하는 중입니다.

	- 이를 False로 설정하면 존재하지 않는 관련 개체에 액세스 할 수 없게 되므로 `DoesNotExist` 예외가 발생합니다.

- *__ForeignKey.swappable__*

	- 이 `ForeignKey`가 스왑 가능 모델을 가리키는 경우 마이그레이션 프레임 워크의 반응을 제어합니다. 이것이 True이면 - 기본값 - 그러면 `ForeignKey`가 `settings.AUTH_USER_MODEL` (또는 다른 스왑 가능 모델 설정)의 현재 값과 일치하는 모델을 가리키면 관계가 설정에 대한 참조를 사용하여 마이그레이션에 저장됩니다. 모델을 직접적으로.

	- 모델이 항상 스왑 된 모델 (예: 사용자 정의 사용자 모델 전용으로 설계된 프로파일 모델 인 경우)을 가리켜 야한다고 확신하는 경우에만 False로 바꾸십시오.

	- False로 설정한다고해서 스왑 가능 모델을 스왑 아웃해도 참조 할 수 있다는 의미는 아닙니다. False는이 ForeignKey로 수행 된 마이그레이션이 항상 사용자가 지정한 정확한 모델을 참조한다는 것을 의미합니다 (따라서 사용자가 실행하려고하면 실패합니다 예를 들어 사용자가 지원하지 않는 사용자 모델로).

	- 의심스러운 경우 기본값 인 True로 두십시오.

<br>
	
> `on_delete`(그 중에서도 CASCADE랑 PROTECT), `related_name`, `related_query_name`  
> 말고는 뭔지 모르겠음.

---

*__ManyToManyField__*

- *__class ManyToManyField(othermodel, \*\*options)__* [source][ManyToMany source]

- many-to-many(다대다) 관계. 위치 지정 인수가 필요합니다. 모형이 관련된 클래스이며, 재귀(recursive) 및 지연(lazy) 관계를 포함하여 ForeignKey에서와 똑같이 작동합니다.

	> ❓재귀는 자신과 관계를 가지는 것이고, 사용은 'self'로 하면 되는걸로 알겠는데, 지연관계 라는게 어떤 상황인지 감이오질 않는다.

- 관련 객체는 필드의 [RelatedManager]를 사용하여 추가, 제거 또는 생성 할 수 있습니다.

*__Database Representation__*

- 배후에서 Django는 다대다 관계를 나타 내기 위해 **중개 조인 테이블을 생성**합니다. 기본적으로이 테이블 이름은 **다대다 필드의 이름과 그 테이블을 포함하는 모델의 테이블 이름을 사용하여 생성**됩니다. 일부 데이터베이스는 특정 길이 이상의 테이블 이름을 지원하지 않으므로 이러한 테이블 이름은 자동으로 **64자**로 잘리고 고유성 해시가 사용됩니다. 즉, `author_books_9cdf4`와 같은 테이블 이름을 볼 수 있습니다. **이것은 정상입니다.** [db_table] 옵션을 사용하여 조인 테이블의 이름을 수동으로 제공 할 수 있습니다.

[ManyToMany source]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/fields/related/#ManyToManyField

[RelatedManager]: https://docs.djangoproject.com/en/1.11/topics/auth/default/

[db_table]: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.ManyToManyField.db_table

-

*__Arguments__*

- ManyToManyField는 **관계 함수가 제어되는 방식을 제어하는 ​​추가 인수 세트** (모두 선택 가능, all optional)를 허용합니다.

- *__ManyToManyField.related_name__*
	- Same as *__ForeignKey.related_name__*.

- *__ManyToManyField.related_query_name__*
	- Same as *__ForeignKey.related_query_name__*.

- *__ManyToManyField.limit_choices_to__*
	- Same as *__ForeignKey.limit_choices_to__*.

	- `limit_choices_to`는 **through** 매개 변수를 사용하여 지정된 사용자 지정 중간 테이블이있는 ManyToManyField에서 사용될 때 아무런 영향을주지 않습니다.

		> `limit_choices_to` 이해 못했는데...  
		> 아무튼 through 매개 변수에 아무런 영향을 주지 않는다.
		
- *__ManyToManyField.symmetrical__*

- 자체에 대한 ManyToManyFields의 정의에만 사용됩니다. 다음 모델을 고려하십시오.

	```
	from django.db import models
	
	class Person(models.Model):
	    friends = models.ManyToManyField("self")
	```
	
- Django는이 모델을 처리 할 때 ManyToManyField가 있음을 식별하므로 Person 클래스에 **person_set 속성을 추가**하지 않습니다. 대신, ManyToManyField는 대칭(symmetrical)이라고 가정합니다. 즉, 제가 당신의 친구라면, 당신은 내 친구입니다.

- 자기와의 many-to-many 관계에서 대칭(symmetrical)을 원하지 않는다면 대칭을 False로 설정하십시오. 이렇게하면 Django가 **역방향 관계에 대한 설명자를 추가하여 ManyToManyField 관계가 비대칭이되도록합니다.**


*__ManyToManyField.through__*

- Django는 다-대-다 관계를 관리하기위한 테이블을 자동으로 생성합니다. 그러나 **중개 테이블을 수동으로 지정**하려면 through 옵션을 사용하여 사용할 중간 테이블을 나타내는 Django 모델을 지정할 수 있습니다.

- 이 옵션의 가장 일반적인 용도는 추가 데이터를 다대다 관계와 연관시키려는 경우([extra data with a many-to-many relationship])입니다.

- 명시적 모델을 지정하지 않은 경우, 연관을 유지하기 위해 작성된 테이블에 직접 액세스하는 데 사용할 수있는 암시적 through 모델 클래스가 여전히 존재합니다. 모델을 연결하는 **세 개의 필드**가 있습니다.

- 원본 및 대상 모델이 다른 경우 다음 필드가 생성됩니다.

	- *__id__*
		- 관계의 주키(primary key)

	- *__\<containing\_model\>\_id__*
		- ManyToManyField를 선언한 모델의 ID입니다.

	- *__\<other\_model\>\_id__*
		- ManyToManyField가 가리키는 모델의 ID입니다.
	
- ManyToManyField가 동일한 모델에서 시작하여 동일한 모델을 가리키는 경우 다음 필드가 생성됩니다.

	- *__id__*
		- 관계의 주키(primary key)

	- *__from\_\<model\>\_id__*
		- 모델(즉, 소스 인스턴스)를 가리키는 인스턴스의 id.
	
	- *__to\_\<model\>\_id__*
		- 관계가 가리키는 인스턴스의 ID (즉, 타겟 모델 인스턴스)

*__ManyToManyField.through\_fields__*

- 사용자 지정 매개 모델(through)이 지정된 경우에만 사용됩니다. Django는 일반적으로 다대다 관계를 자동으로 설정하기 위해 사용할 중개 모델의 필드를 결정합니다. 그러나 다음 모델을 고려하십시오.

	```
	from django.db import models

	class Person(models.Model):
	    name = models.CharField(max_length=50)
	
	class Group(models.Model):
	    name = models.CharField(max_length=128)
	    members = models.ManyToManyField(
	        Person,
	        through='Membership',
	        through_fields=('group', 'person'),
	    )
	
	class Membership(models.Model):
	    group = models.ForeignKey(Group, on_delete=models.CASCADE)
	    person = models.ForeignKey(Person, on_delete=models.CASCADE)
	    inviter = models.ForeignKey(
	        Person,
	        on_delete=models.CASCADE,
	        related_name="membership_invites",
	    )
	    invite_reason = models.CharField(max_length=64)
	```

- 멤버십에는 Person(사람과 초청자, person and inviter)에 대한 **두 개의 외래키**가있어 관계가 모호 해지고 장고는 사용할 관계를 알 수 없습니다. 이 경우 위의 예제에서와 같이 장고가 through_fields를 사용하여 사용해야하는 외래키를 명시적으로 지정해야합니다.

- through_fields는 Two-tuple `( 'field1', 'field2')`을 허용합니다. 여기서 field1은 ManyToManyField가 정의 된 모델의 외래키 이름이고 (이 경우 그룹) field2는 외래키의 이름입니다. 목표 모델 (이 경우 사람).

- 다대다 관계에 참여하는 모델 중 하나 (또는 ​​두 모델 모두)의 중개 모델에 둘 이상의 외래 키가있는 경우에는 `through_fields`를 지정해야합니다. 이것은 중개 모델이 사용되고 **모델에 외래 키가 두 개 이상**이거나 Django가 사용할 두 개의 명시 적으로 지정하려는 경우 재귀 관계에도 적용됩니다.

- 중간 모델을 사용하는 재귀 관계는 항상 비대칭, 즉 `symmetrical = False`로 정의되므로 "원본(source)"과 "대상(target)"이라는 개념이 있습니다. 이 경우 'field1'은 관계의 '소스'로 취급되고 'target2'는 'field2'로 취급됩니다.

*__ManyToManyField.db_table__*

- 다대다 데이터를 저장하기 위해 작성할 테이블의 이름. 이것이 제공되지 않는다면, Django는 관계를 정의하는 모델의 테이블과 필드 자체의 이름을 기반으로 기본 이름을 사용합니다.

*__ManyToManyField.db_constraint__*

- 중개(intermediary) 테이블의 외래 키에 대해 데이터베이스에 제약 조건을 생성해야하는지 여부를 제어합니다. 기본값은 True이며, 거의 확실하게 원하는 것입니다. 이것을 False로 설정하면 데이터 무결성이 매우 나쁠 수 있습니다. 즉, 다음과 같은 시나리오가 있습니다.

	- 유효하지 않은 기존 데이터가 있습니다.
	- 데이터베이스를 재구성하는 중입니다.

- `db_constraint`와 `through`를 모두 전달하는 것은 오류입니다.

*__ManyToManyField.swappable__*

- 이 ManyToManyField가 스왑 가능 모델을 가리키는 경우 마이그레이션 프레임 워크의 반응을 제어합니다. 이것이 True이면 - 기본값 - ManyToManyField가 `settings.AUTH_USER_MODEL` (또는 다른 스왑 가능 모델 설정)의 현재 값과 일치하는 모델을 가리키는 경우 관계는 설정에 대한 참조를 사용하여 마이그레이션에 저장됩니다. 모델을 직접적으로.

- 모델이 항상 스왑 된 모델 (예 : 사용자 정의 사용자 모델 전용으로 설계된 프로파일 모델 인 경우)을 가리켜 야한다고 확신하는 경우에만 False로 바꾸십시오.

- ManyToManyField는 검사기([validators])를 지원하지 않습니다.

- 데이터베이스 레벨에서 관계를 요구할 방법이 없기 때문에 [null]은 아무 효과가 없습니다.

[extra data with a many-to-many relationship]: https://docs.djangoproject.com/en/1.11/topics/db/models/#intermediary-manytomany

[validators]: https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.Field.validators

---

*__OneToOneField__*

- *__class OneToOneField(othermodel, on_delete, parent_link=False, \*\*options)__* [source][OneToOne source]

- 일대일 관계. 개념적으로 이는 `unique = True` 인 [ForeignKey]와 유사하지만 관계의 "역"측은 하나의 객체를 직접 반환합니다.

- 이는 어떤 방법으로 다른 모델을 "확장"하는 모델의 기본 키로 가장 유용합니다. [다중 테이블 상속][Multi-table inheritance]은 하위 모델에서 상위 모델로 암시적 일대일 관계를 추가하여 구현됩니다.

- 모델이 관련 될 클래스인 하나의 위치 인수가 필요합니다. 이는 재귀 및 지연 관계와 관련된 모든 옵션을 포함하여 ForeignKey에서와 똑같이 작동합니다.

- OneToOneField에 `related_name` 인수를 지정하지 않으면 Django는 현재 모델의 소문자 이름을 기본값으로 사용합니다.

- 다음 예제를 참조하십시오.

	```
	from django.conf import settings
	from django.db import models
	
	class MySpecialUser(models.Model):
	    user = models.OneToOneField(
	        settings.AUTH_USER_MODEL,
	        on_delete=models.CASCADE,
	    )
	    supervisor = models.OneToOneField(
	        settings.AUTH_USER_MODEL,
	        on_delete=models.CASCADE,
	        related_name='supervisor_of',
	    )
	```
	
- 최종 사용자 모델에는 다음과 같은 속성이 있습니다.

	```
	>>> user = User.objects.get(pk=1)
	>>> hasattr(user, 'myspecialuser')
	True
	>>> hasattr(user, 'supervisor_of')
	True
	```
	
- 관련 테이블의 항목이없는 경우 역방향 관계에 액세스 할 때 DoesNotExist 예외가 발생합니다. 예를 들어 사용자에게 MySpecialUser가 지정한 관리자가없는 경우 :

	```
	>>> user.supervisor_of
	Traceback (most recent call last):
	    ...
	DoesNotExist: User matching query does not exist.
	```	
	
- 또한 OneToOneField는 ForeignKey에서 허용하는 모든 추가 인수와 하나의 추가 인수를 허용합니다.

- *__OneToOneField.parent_link__*

	- True이면 다른 모델을 상속한 모델에서 이 필드를 서브 클래싱하여 일반적으로 암시적으로 생성되는 여분의 OneToOneField가 아니라 부모 클래스에 대한 링크로 사용해야 함을 나타냅니다.

- OneToOneField의 사용 예제는 [일대일 관계][one_to_one]를 참조하십시오.


[OneToOne source]: https://docs.djangoproject.com/en/1.11/_modules/django/db/models/fields/related/#OneToOneField

[Multi-table inheritance]: https://docs.djangoproject.com/en/1.11/topics/db/models/#multi-table-inheritance

[one_to_one]:https://docs.djangoproject.com/en/1.11/topics/db/examples/one_to_one/