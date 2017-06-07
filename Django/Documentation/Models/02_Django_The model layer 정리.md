# Django_The model layer 정리

### Models: Introduction to models

<br>

*__Models__*

- 모델은 **데이터**에 대한 **단일 정보 소스**이다. 여기에는 저장중인 데이터의 **필수 필드**와 **동작**이 포함됩니다.(class) 일반적으로 각 모델은 단일 데이터베이스 테이블에 매핑됩니다.
- 기본 사항
	- 각 모델은 `django.db.models.Model`을 하위 클래스로 묶는 Python 클래스입니다.(상속)
	- **모델의 각 속성**은 **데이터베이스 필드**를 나타냅니다.
	- 이 모든 것을 통해 Django는 자동으로 생성 된 **데이터베이스 액세스 API**를 제공합니다. [쿼리 만들기](https://docs.djangoproject.com/en/1.11/topics/db/queries/)를 참조하십시오.

<br>

*__Quick example__*

- 이 예제 모델은 first\_name과 last\_name이있는 Person을 정의합니다.

	```
	from django.db import models
	
	class Person(models.Model):
	    first_name = models.CharField(max_length=30)
	    last_name = models.CharField(max_length=30)
	```
	
	- first\_name과 last\_name은 **모델의 필드**입니다. 각 **필드**는 **클래스 속성**으로 지정되며 **각 속성**은 **데이터베이스 열**에 **매핑**됩니다.
	- 위의 Person 모델은 다음과 같은 데이터베이스 테이블을 생성합니다.

		```
		CREATE TABLE myapp_person (
		    "id" serial NOT NULL PRIMARY KEY,
		    "first_name" varchar(30) NOT NULL,
		    "last_name" varchar(30) NOT NULL
		);
		```
		> 이름이 myapp_person 인 점  
		> id 속성을 따로 정해주지 않았는데 추가 된 점
	- Some technical notes:
		
		- 테이블의 이름 인 myapp_person은 **일부 모델 메타 데이터에서 자동으로 파생**되지만 **재정의 될 수 있습니다.** [Model-Meta-options: Table names 참조](https://docs.djangoproject.com/en/1.11/ref/models/options/#table-names)
		- id 필드가 자동으로 추가되지만 이 동작은 무시 될 수 있습니다. [Automatic primary key fields 참고](https://docs.djangoproject.com/en/1.11/topics/db/models/#automatic-primary-key-fields)
		- 이 예제의 CREATE TABLE SQL은 PostgreSQL 구문을 사용하여 포맷되지만 Django는 설정 파일에 지정된 데이터베이스 백엔드에 맞게 SQL을 사용합니다. (사용자의 db세팅에 맞게 쿼리를 생성!!!) 

-

*__Using models__*

- 모델을 정의한 후에는 Django에게 해당 모델을 사용할 것이라고 알려야합니다. **setting.py** 파일을 편집하고 **INSTALLED_APPS 설정을 변경**하여 models.py가 포함 된 **모듈**의 이름을 추가하면됩니다.

	```
	INSTALLED_APPS = [
	    #...
	    'myapp',
	    #...
	]
	```
	- INSTALLED_APPS에 새 앱을 추가 할 때는 manage.py migrate를 실행하고, 선택적으로 manage.py makemigrations를 사용하여 마이그레이션을 수행하십시오.

-

*__Fields__*

- 모델의 가장 중요한 부분과 모델의 유일한 필수 부분은 **정의하는 데이터베이스 필드의 목록**입니다. **필드는 클래스 속성에 의해 지정됩니다.** 모델 API와 충돌하는 필드 이름을 정리, 저장 또는 삭제하지 않도록주의하십시오.

	```
	from django.db import models

	class Musician(models.Model):
	    first_name = models.CharField(max_length=50)
	    last_name = models.CharField(max_length=50)
	    instrument = models.CharField(max_length=100)
	
	class Album(models.Model):
	    artist = models.ForeignKey(
	    Musician, 
	    on_delete=models.CASCADE
	    )
	    name = models.CharField(max_length=100)
	    release_date = models.DateField()
	    num_stars = models.IntegerField()
	   ```
- Field types
	- 모델의 각 필드는 **적절한 Field 클래스의 인스턴스** 여야합니다. Django는 필드 클래스 유형을 사용하여 몇 가지를 결정합니다.
		- 데이터베이스에 어떤 종류의 데이터를 저장 할지를 알려주는 열 유형 (예 : INTEGER, VARCHAR, TEXT).
		- 양식 필드를 렌더링 할 때 사용할 기본 HTML 위젯 (예 : `<input type = "text">`, `<select>`).
		- 장고 관리자 및 자동 생성 양식에서 사용되는 최소한의 유효성 확인 요구 사항.
	- Django에는 수십 가지 내장 필드 유형이 있습니다. 
		- [모델필드전체목록](https://docs.djangoproject.com/en/1.11/ref/models/fields/#model-field-types)

-

*__Field options__*

각 필드는 필드 특정 인수 집합을 사용합니다.(argument) 예를 들어, CharField (및 해당 하위 클래스)에는 데이터를 저장하는 데 사용되는 VARCHAR 데이터베이스 필드의 크기를 지정하는 max_length 인수가 필요합니다.

```
models.CharField(max_length=30)
```

또한 모든 필드 유형에 사용할 수있는 일반적인 인수 집합이 있습니다. 모두 선택 사항입니다. 그것들은 참고 문헌에서 완전히 설명되어 있지만, 가장 자주 사용되는 것들에 대한 간단한 요약이 있습니다 :

- null
	- True이면 Django는 빈 값을 NULL로 데이터베이스에 저장합니다. 기본값은 False입니다.
- blank
	- True이면 필드를 비워 둘 수 있습니다. 기본값은 False입니다.
	- **이것은 null과 다릅니다.** null은 순전히 데이터베이스와 관련된 반면 blank는 유효성 검사와 관련이 있습니다. 필드에 blank = True가 있으면 양식 유효성 검사에서 빈 값을 입력 할 수 있습니다. 필드에 blank = False가 있으면 필드가 필요합니다.(require)
- choice
	- 이 필드의 선택 항목으로 사용할 2-튜플의 반복 가능한 (예 : 리스트 또는 튜플) 이것이 주어지면 기본 양식 위젯은 표준 텍스트 필드 대신 선택 상자가되어 주어진 선택 사항으로 선택을 제한합니다.

	```
	YEAR_IN_SCHOOL_CHOICES = (
	    ('FR', 'Freshman'),
	    ('SO', 'Sophomore'),
	    ('JR', 'Junior'),
	    ('SR', 'Senior'),
	    ('GR', 'Graduate'),
	)
	```
	- 각 튜플의 첫 번째 요소는 데이터베이스에 저장 될 값입니다.
	- 두 번째 요소는 기본 양식 위젯 또는 ModelChoiceField에 표시됩니다. 모델 인스턴스가 주어지면 선택 필드의 표시 값은 get\_FOO\_display () 메소드를 사용하여 액세스 할 수 있습니다. 예 :

	```
	from django.db import models

	class Person(models.Model):
	    SHIRT_SIZES = (
	        ('S', 'Small'),
	        ('M', 'Medium'),
	        ('L', 'Large'),
	    )
	    name = models.CharField(max_length=60)
	    shirt_size = models.CharField(
	    	max_length=1, 
	    	choices=SHIRT_SIZES
	    )
    ```
    ```
	>>> p = Person(name="Fred Flintstone", shirt_size="L")
	>>> p.save()
	>>> p.shirt_size
	'L'
	>>> p.get_shirt_size_display()
	'Large'
	```
	
- default
	- 필드의 기본값입니다. 값 또는 호출 가능 객체 일 수 있습니다. 호출 가능하면 새로운 객체가 생성 될 때마다 호출됩니다.
- help_text
	- 양식 위젯과 함께 표시되는 추가 "도움말"텍스트. 양식에서 필드를 사용하지 않아도 문서화에 유용합니다.
- primary_key
	- True이면이 필드는 모델의 기본 키입니다.
	- 모델의 모든 필드에 primary\_key = True를 지정하지 않으면, Django는 자동적으로 IntegerField를 추가하여 프라이 머리 키를 유지하고, 기본 기본 키 동작을 덮어 쓰지 않으려면 모든 필드에서 primary\_key = True를 설정할 필요가 없습니다. 
	- 기본 키 필드는 읽기 전용입니다. 기존 개체의 기본 키 값을 변경 한 다음 저장하면 이전 개체와 함께 새 개체가 만들어집니다. 예 :

	```
	from django.db import models

	class Fruit(models.Model):
	    name = models.CharField(
	    max_length=100, 
	    primary_key=True
	    )
	```
	```
	>>> fruit = Fruit.objects.create(name='Apple')
	>>> fruit.name = 'Pear'
	>>> fruit.save()
	>>> Fruit.objects.values_list('name', flat=True)
	['Apple', 'Pear']
	```

- unique
	- 참이면이 필드는 테이블 전체에서 고유해야합니다.

-
*__Automatic primary key fields__*

- 기본적으로 Django는 각 모델에 다음 필드를 제공합니다.

	```
	id = models.AutoField(primary_key=True)
	```

- 자동 **증가** 기본 키입니다.
- 사용자 정의 기본 키를 지정하려면 필드 중 하나에서 primary_key = True를 지정하면됩니다. Django가 Field.primary_key를 명시 적으로 설정했다고 판단하면 자동 ID 열을 추가하지 않습니다.
- 각 모델은 primary_key = True (명시 적으로 선언되거나 자동으로 추가됨)를 갖기 위해 정확히 하나의 필드가 필요합니다.

-

*__Verbose field names__*
> Verbose: 장황한

- ForeignKey, ManyToManyField 및 OneToOneField를 제외한 각 필드 유형은 선택적 첫 번째 위치 인수 - verbose name을 사용합니다. verbose name 인자가 주어지지 않으면 Django는 밑줄(_)을 공백으로 변환하여 **필드의 속성 이름을 사용하여 verbose name을 자동으로 만듭니다.**

> ForeignKey(외래키), ManyToManyField(다대다 필드) 및 OneToOneField(일대일 필드)의 경우엔 첫번째 인수가 참조 모델 클래스가 인자값임

- 이 예제에서 verbose name은 "person 's first name"입니다.

	```
	first_name = models.CharField("person's first name", max_length=30)
	```

- 이 예제에서 verbose name은 "first name"입니다. (변수명 언더스코어가 공백으로 바뀜)

	```
	first_name = models.CharField(max_length=30)
	```
	
- ForeignKey, ManyToManyField 및 OneToOneField는 첫 번째 인수가 모델 클래스 여야하므로 verbose_name 키워드 인수를 사용하십시오.

	```
	poll = models.ForeignKey(
		Polls,
		on_delete=models.CASCADE,
		verbose_name="the related poll",
	)
	sites = models.ManyToManyfield(Site, verbose_name="list of sites")
	place = models.OneToOnefield(
		Place,
		on_delete=models.CASCADE,
		verbose_name="related place",
	)
	```
	
- 규약은 verbose_name의 첫 문자를 대문자로 사용하지 않습니다. Django는 필요한 첫 문자를 자동으로 대문자로 만듭니다.

-

*__Relationships__*

- 분명히, 관계형 데이터베이스의 힘은 테이블을 서로 연관시키는 데 있습니다. Django는 다대일, 다대다 및 일대일 데이터베이스 관계의 세 가지 가장 일반적인 유형을 정의하는 방법을 제공합니다.

- *__다대일(Many-to-one relationships)__*
	- 다 대일 관계를 정의하려면 django.db.models.ForeignKey를 사용하십시오. 다른 필드 유형과 마찬가지로 모델의 클래스 속성으로 포함하여 사용합니다.
	- ForeignKey에는 위치 인수가 필요합니다. 모델이 관련된 클래스입니다.
	- 예를 들어 자동차 모델에 제조업체가있는 경우 - 즉, 제조업체가 여러 자동차를 생산하지만 각 자동차에만 하나의 제조업체가있는 경우 - 다음 정의를 사용하십시오.

```
from django.db import models

class Manufacturer(models.Model):
	# ...
	pass
	
class Car(models.Model):
	manufacturer = models.ForeignKey(
		Manufacturer,
		on_delete=models.CASCADE
	)
	# ...
```

- 재귀 관계 (자체와의 다 대일 관계가있는 객체)를 만들 수도 있습니다.
- ForeignKey 필드의 이름 (위의 예제에서 제조업체)은 소문자 인 모델의 이름이 될 것을 권장하지만 필수는 아닙니다. (manufacturer) 물론 원하는대로 필드를 호출 할 수 있습니다. 예 :

```
class Car(models.Model):
	campany_that_makes_it = models.ForeignKey(
		Manufacturer,
		on_delete=models.CASCADE,
	)
	# ...
```
-
- *__다대다(Many-to-many relationships)__*

	- many-to-many 관계를 정의하려면 ManyToManyField를 사용하십시오. 다른 필드 유형과 마찬가지로 모델의 클래스 속성으로 포함하여 사용합니다.
	- ManyToManyField에는 위치 인수가 필요합니다. 모델이 관련된 클래스입니다.
	- 예를 들어, 피자에 여러 토핑 개체가있는 경우 - 토핑이 여러 피자에있을 수 있으며 각 피자에 여러 토핑이있는 경우 - 여기에 그 피자를 나타내는 방법이 있습니다.

```
from django.db import models

class Topping(models.Model):
	# ...
	pass
	
class Pizza(models.Model):
	# ...
	toppings = models.ManyToManyField(Topping)
```
- ForeignKey와 마찬가지로 재귀 관계 (자체와의 다 대다 관계가있는 객체)를 만들 수도 있습니다.
- ManyToManyField (위의 예제에서 토핑)의 이름은 관련 모델 객체 세트를 설명하는 복수형으로 제안되지만 필수는 아닙니다. (tippings)
- ManyToManyField가있는 모델은 중요하지 않지만 **두 모델 중 하나에만 삽입해야합니다.**
- 일반적으로 ManyToManyField 인스턴스는 폼에서 편집 할 객체에 있어야합니다. 위의 예에서 토핑은 여러 개의 피자에 토핑을하는 것보다 **토핑을하는 피자에 대해 생각하는 것이 자연 스럽기 때문에** 피자 (피자 ManyToManyField가있는 토핑이 아닌)에 있습니다. 위에 설정된 방식대로 피자 양식을 사용하면 사용자가 토핑을 선택할 수 있습니다.

-

- *__Extra fields on many-to-many relationships__*
	- 피자와 토핑을 믹싱하고 매칭하는 것과 같은 단순한 다 대다 관계 만 처리 할 때는 표준 ManyToManyField 만 있으면됩니다. 그러나 때로는 두 모델 간의 관계에 데이터를 연결해야 할 수도 있습니다.
	- 예를 들어 음악가가 속한 음악 그룹을 추적하는 응용 프로그램의 경우를 생각해보십시오. 개인과 회원이 속해있는 그룹 간에는 다 대 다 관계가 있으므로이 관계를 나타 내기 위해 ManyToManyField를 사용할 수 있습니다. 그러나 그룹에 가입 한 날짜와 같이 수집하고자하는 멤버쉽에 대한 세부 정보가 많이 있습니다.
	- 이러한 상황에서 Django는 다 - 대 - 다 관계를 관리하는 데 사용될 모델을 지정할 수 있습니다. 그러면 중간 모델에 필드를 추가 할 수 있습니다. 중간 모델은 throughTo 인수를 사용하여 중개자 역할을하는 모델을 가리키는 ManyToManyField와 연결됩니다. 뮤지션의 경우, 코드는 다음과 같습니다.

	```
	from django.db import models


	class Person(models.Model):
	    name = models.CharField(max_length=128)
	
	    def __str__(self):
	        return self.name
	
	
	class Group(models.Model):
	    name = models.CharField(max_length=128)
	    members = models.ManyToManyField(
	        Person,
	        through="Membership"
	    )
	
	    def __str__(self):
	        return self.name
	
	
	class Membership(models.Model):
	    person = models.ForeignKey(
	        Person,
	        on_delete=models.CASCADE
	    )
	    group = models.ForeignKey(
	        Group,
	        on_delete=models.CASCADE
	    )
	    data_joined = models.DateField()
	    invite_reason = models.CharField(max_length=64)
	```

- 중개 모델을 설정할 때, 다 대 다 관계와 관련된 모델에 대한 외래 키를 명시 적으로 지정합니다. 이 명시 적 선언은 두 모델이 관련되는 방식을 정의합니다.
- 중간 모델에는 몇 가지 제한 사항이 있습니다.
	- **중간 모델**에는 원본 모델에 대한 외래 키가 하나만 포함되어야합니다 (이 예에서는 Group입니다). Django가 ManyToManyField.through\_fields를 사용하여 관계에 사용해야하는 외래 키를 명시적으로 지정해야합니다. 둘 이상의 외부 키가 있고 through\_fields가 지정되지 않은 경우. 유효성 검증 오류가 발생합니다. 비슷한 제한이 대상 모델에 대한 외래 키에도 적용됩니다 (이 예에서는 Person입니다).
	- 중간 모델을 통해 다대다 관계를 갖는 모델의 경우 동일한 모델에 대한 두 개의 외래 키가 허용됩니다. 그러나 그들은 다 - 대 - 다 관계의 두 가지 측면으로 취급 될 것이다. 두 개 이상의 외래 키가있는 경우 위와 같이 through_fields도 지정해야합니다. 그렇지 않으면 유효성 검사 오류가 발생합니다.
	- 중개 모델을 사용하여 모델에서 다 대다 관계를 정의 할 때는 symmetrical = False를 사용해야합니다.

- 이제 중개 모델 (이 경우 Membership)을 사용하도록 ManyToManyField를 설정 했으므로, 당신은 다 대 다 관계를 만들기 시작할 준비가되었습니다. 중간 모델의 인스턴스를 생성하여이를 수행합니다.

	```
	>>> ringo = Person.objects.create(name="Ringo Starr")
	>>> paul = Person.objects.create(name="Paul McCartney")
	>>> beatles = Group.objects.create(name="The Beatles")
	>>> m1 = Membership(person=ringo, group=beatles,
	...     date_joined=date(1962, 8, 16),
	...     invite_reason="Needed a new drummer.")
	>>> m1.save()
	>>> beatles.members.all()
	<QuerySet [<Person: Ringo Starr>]>
	>>> ringo.group_set.all()
	<QuerySet [<Group: The Beatles>]>
	>>> m2 = Membership.objects.create(person=paul, group=beatles,
	...     date_joined=date(1960, 8, 1),
	...     invite_reason="Wanted to form a band.")
	>>> beatles.members.all()
	<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
	``` 

- 일반적인 다 대다 필드와는 달리 add (), create () 또는 set ()을 사용하여 관계를 만들 수 없습니다.

	```
	>>> # The following statements will not work
	>>> beatles.members.add(john)
	>>> beatles.members.create(name="George Harrison")
	>>> beatles.members.set([john, paul, ringo, george])
	```
	
- 왜냐하면, 개인과 그룹 간의 관계 만 만들 수는 없습니다. 멤버십 모델에 필요한 관계에 대한 모든 세부 사항을 지정해야합니다. 간단한 추가, 생성 및 할당 호출은 이러한 추가 세부 사항을 지정하는 방법을 제공하지 않습니다. 결과적으로, 중간 모델을 사용하는 다 대 다 관계에 대해서는 비활성화됩니다. 이러한 유형의 관계를 작성하는 유일한 f}은 중간 모델의 인스턴스를 작성하는 것입니다.
- 유사한 이유로 remove () 메서드가 비활성화됩니다. 예를 들어, 중간 모델에 의해 정의 된 사용자 정의 테이블을 통해 (model1, model2) 쌍의 고유성을 적용하지 않으면 remove () 호출은 어떤 중간 모델 인스턴스를 삭제해야하는지에 대한 충분한 정보를 제공하지 않습니다.

	```
	>>> Membership.objects.create(person=ringo, group=beatles,
	...     date_joined=date(1968, 9, 4),
	...     invite_reason="You've been gone for a month and we miss you.")
	>>> beatles.members.all()
	<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>, <Person: Ringo Starr>]>
	>>> # This will not work because it cannot tell which membership to remove
	>>> beatles.members.remove(ringo)
	```
	
- 그러나 clear () 메서드는 인스턴스의 모든 다 대다 관계를 제거하는 데 사용할 수 있습니다.

	```
	>>> # Beatles have broken up
	>>> beatles.members.clear()
	>>> # Note that this deletes the intermediate model instances
	>>> Membership.objects.all()
	<QuerySet []>
	```
	
- 중간 모델의 인스턴스를 생성하여 다 대 다 관계를 설정하면, 쿼리를 실행할 수 있습니다. 일반적인 다 대다 관계와 마찬가지로 다 대 다 관련 모델의 특성을 사용하여 쿼리 할 수 ​​있습니다.

	```
	# Find all the groups with a member whose name starts with 'Paul'
	>>> Group.objects.filter(members__name__startswith='Paul')
	<QuerySet [<Group: The Beatles>]>
	```
	
- 중간 모델을 사용할 때 해당 속성에 대해서도 쿼리 할 수 ​​있습니다.

	```
	# Find all the members of the Beatles that joined after 1 Jan 1961
	>>> Person.objects.filter(
	...     group__name='The Beatles',
	...     membership__date_joined__gt=date(1961,1,1))
	<QuerySet [<Person: Ringo Starr]>
	```
	
- 회원 정보에 액세스해야하는 경우 멤버쉽 모델에 직접 문의하여 수행 할 수 있습니다.

	```
	>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
	>>> ringos_membership.date_joined
	datetime.date(1962, 8, 16)
	>>> ringos_membership.invite_reason
	'Needed a new drummer.'
	```
	
- 동일한 정보에 접근하는 또 다른 방법은 Person 객체에서 many-to-many 역방향 관계를 쿼리하는 것입니다.

	```
	>>> ringos_membership = ringo.membership_set.get(group=beatles)
	>>> ringos_membership.date_joined
	datetime.date(1962, 8, 16)
	>>> ringos_membership.invite_reason
	'Needed a new drummer.'
	```

> 솔직히 다대다도 헷갈리는데, extra도 이해하려고 하니깐 어렵다. 우선은 중간 모델이 있고, through(던져주는) 옵션으로 어떻게 처리한다는 것, 그래서 그에 따른 규약이 있다는 것 정도가 있다는 것만 알고 넘어가자.
	
-

- *__일대일(one-to-one)__*

- 일대일 관계를 정의하려면 OneToOneField를 사용하십시오. 다른 필드 유형과 마찬가지로 모델의 클래스 속성으로 포함하여 사용합니다.
- 이것은 객체의 기본 키에서 객체가 어떤 방식으로 다른 객체를 "확장"할 때 가장 유용합니다.
- OneToOneField에는 위치 인수 인 모델과 관련된 클래스가 필요합니다.
- 예를 들어, "places"의 데이터베이스를 구축하는 경우 데이터베이스에서 주소, 전화 번호 등과 같은 아주 표준적인 항목을 작성하게됩니다. 그런 다음, 레스토랑의 데이터베이스를 직접 만들고 레스토랑 모델에서 해당 필드를 복제하는 대신 장소 위에 레스토랑 데이터베이스를 구축하려는 경우, 당신은 Restaurant에 OneToOneField Place를 둘 수 있습니다 (왜냐하면 레스토랑은 "장소"이기 때문에 사실 이것을 처리하기 위해 암시 적 일대일 관계가 포함 된 상속을 사용합니다).
- OneToOneField 필드는 선택적 parent_link 인수도 허용합니다.
- OneToOneField 클래스는 모델에서 자동으로 기본 키가됩니다. 원하는 경우 primary_key 인수를 수동으로 전달할 수는 있지만 더 이상 사실이 아닙니다. 따라서 이제 단일 모델에 OneToOneField 유형의 여러 필드를 포함 할 수 있습니다.

-

- *__Models across files__*

- 모델을 다른 앱의 모델과 연결하는 것은 완벽합니다. 이렇게하려면 모델이 정의 된 파일의 맨 위에 관련 모델을 가져옵니다. 그런 다음 필요할 때마다 다른 모델 클래스를 참조하십시오. 예 :

	```
	from django.db import models
	from geography.models import ZipCode
	
	class Restaurant(models.Model):
	    # ...
	    zip_code = models.ForeignKey(
	        ZipCode,
	        on_delete=models.SET_NULL,
	        blank=True,
	        null=True,
	    )
	```
-

- *__Field name restrictions__*

- Django는 모델 필드이름에 2가지 제약을 두고 있습니다.
- 파이썬 예약어는 필드이름으로 사용할 수 없습니다. 이 경우 파이썬 문법에러가 발생됩니다.

	```
	class Example(models.Model):
		pass = models.IntegerField() # 'pass' is a reserved word!
	```
	
- 두번째로, 필드이름에 밑줄 두개를 연속으로 사용할 수 없습니다. 이는 Django에서 특별한 문법으로 사용되기 때문입니다. 

	```
	class Example(models.Model):
	foo__bar = models.IntegerField() # 'foo__bar' has two underscores!
	```
	
- 데이터베이스 컬럼이름에 밑줄을 두 개 넣어야 하는 상황이라면, db_column 옵션을 이용해서 이러한 제약을 우회할 수 있습니다.
- SQL 예약어의 경우(join, where, select 등)에는 필드이름으로 허용됩니다. Django가 쿼리문을 만들때, 모든 컬럼명과 테이블 명을 모두 이스케이프 처리하기 때문입니다. 실제 데이터베이스 엔진에 맞게 알아서 말이죠.

-

- *__Custom field types__*

- Django에서 제공하는 필드 타입들 중에 당신의 목적에 적합한 타입이 없거나 특정 데이터베이스에서만 제공하는 특별한 타입을 사용하고 싶다면, 필드를 직접 만들어 사용할 수도 있습니다. 이 부분에 대한 내용은 "Writing custom model fields" 문서를 참고하세요.

-

- *__Meta options__*

- 아래와같이 모델클래스 내부에 Meta 라는 이름의 클래스 선언해서 모델에 메타데이터를 추가할 수 있습니다.

	```
	from django.db import models
	
	class Ox(models.Model):
	    horn_length = models.IntegerField()
	
	    class Meta:
	        ordering = ["horn_length"]
	        verbose_name_plural = "oxen"
	```
	
- "모델 메타데이터"란 앞서 보았던 필드 단위의 옵션들과 달리 **모델 단위의 옵션**이라고 볼 수 있습니다. 예를들면, 정렬 옵션(ordering), 데이터베이스 테이블 이름(db\_table), 또는 읽기 좋은 이름이나 복수(plural) 이름을 지정해 줄 수 있습니다(verbose\_name, verbose_name\_plural). 모델클래스에 Meta 클래스를 반드시 선언해야 하는 것은 아니며, 모든 옵션을 모두 설정해야 하는 것도 아닙니다.

- 모든 메타데이터 옵션들을 살펴보려면 ["model option reference"](https://docs.djangoproject.com/en/1.11/ref/models/options/) 문서를 참고하세요.

-

- *__Model attributes__*

- objects
	- 모델 클래스에서 가장 중요한 어트리뷰트는 Manager 입니다. Manager 객체는 모델 클래스 선언을 기반으로 실제 데이터베이스에 대한 **쿼리 인터페이스를 제공**하며, **데이터베이스 레코드를 모델 객체로 인스턴스화 하는데 사용**됩니다. 특별히 Manager를 할당하지 않으면 Django는 Default Manager 객체를 클래스 어트리뷰트로 자동 할당 합니다. 이때 어트리뷰트의 이름이 objects 입니다.



- *__Model methods__*

- "레코드(row) 단위"의 기능을 구현하려면, 모델 클래스에 메서드를 구현해주면 됩니다. "테이블 단위"의 기능의 경우에는 Manager에 구현해 줍니다.
- 이러한 규칙은 비즈니스 로직을 모델에서 관리하는데 있어 중요한 테크닉입니다.
- 예를들어, 아래와 같이 커스텀 메서드를 추가할 수 있습니다.

	```
	from django.db import models

	class Person(models.Model):
	    first_name = models.CharField(max_length=50)
	    last_name = models.CharField(max_length=50)
	    birth_date = models.DateField()
	
	    def baby_boomer_status(self):
	        "Returns the person's baby-boomer status."
	        import datetime
	        if self.birth_date < datetime.date(1945, 8, 1):
	            return "Pre-boomer"
	        elif self.birth_date < datetime.date(1965, 1, 1):
	            return "Baby boomer"
	        else:
	            return "Post-boomer"
	
	    @property
	    def full_name(self):
	        "Returns the person's full name."
	        return '%s %s' % (self.first_name, self.last_name)
	```
	
- "model instance reference"를 보면 모델 클래스에 자동적으로 주어지는 메서드들이 나열되어있습니다. 이러한 메서드를 여러분이 오버라이드해서 사용할 수 있는데 이에 대한 자세한 내용은 다음 절에서 설명합니다.

- 그 중에서 거의 항상 오버라이드 해줘야 할 메서드들이 있습니다.
	- `__unicode__()` (Python 2)  
모델 객체가 문자열로 표현되어야 하는 경우에 호출됩니다. admin이나 console 에서 모델 객체를 표시하는 경우에 많이 쓰이게 됩니다.  

	- `__str__()` (Python 3)  
파이썬 3의 경우에는, __unicode__() 대신에 __str__() 로 선언합니다.  
기본 구현은 아무런 도움이 되지 않는 문자열을 리턴하기 때문에, 모든 모델에 대해 오버라이드 해서 알맞게 구현해주는게 좋습니다.

	- `get_absolute_url()`  
이 메서드는 Django가 해당 모델 객체의 URL을 계산할 수 있도록 합니다. Django는 이 메서드를 모델 객체를 URL로 표현하는 경우에 사용하며, admin 사이트에서도 사용합니다.  
모델 객체가 유일한 URL을 가지는 경우에 이 메서드를 구현해주어야 합니다.

-

- *__Overriding predefined model methods__*

- 모델 클래스가 제공하는 기본적인 메서드들을 커스터마이즈 하고자 하는 경우가 있을 수 있습니다. 특히나, save() 나 delete() 메서드를 오버라이드 하고자 하는 경우가 많을 것입니다.
- 이 메서드들을 얼마든지 오버라이드 해서 동작을 수정할 수 있습니다.
- 모델 객체를 저장할 때마다, 특정한 동작을 수행하기 위해서 save() 메서드를 오버라이드 할 수 있습니다.

	```
	from django.db import models

	class Blog(models.Model):
	    name = models.CharField(max_length=100)
	    tagline = models.TextField()
	
	    def save(self, *args, **kwargs):
	        do_something()
	        super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
	        do_something_else()
	```
	
- 아예 저장을 하지 못하게 할 수도 있습니다.

	```
	from django.db import models

	class Blog(models.Model):
	    name = models.CharField(max_length=100)
	    tagline = models.TextField()
	
	    def save(self, *args, **kwargs):
	        if self.name == "Yoko Ono's blog":
	            return # Yoko shall never have her own blog!
	        else:
	            super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.
	```
	
- 부모 클래스의 메서드를 호출해주는 것을 잊지마세요. 위 예제 코드에서 super(Blog, self).save(\*args, \**kwargs) 를 호출함으로써, 실제로 데이터베이스에 객체가 저장되었습니다. 부모 클래스의 메서드를 호출해주지 않는다면, **실제 데이터베이스에는 아무런 동작도 일어나지 않습니다.**

- 오버라이드한 메서드의 인자를 그대로 부모 클래스의 메서드에 넘겨주는 것도 잊지 마세요. "\*args, \*\*kwargs" 부분이 그것입니다. Django는 계속적으로 옵션이 추가되고 확장 될것입니다. 새로운 인자가 추가될 수도 있겠지요. 그렇기 때문에 당신이 오버라이드 하는 메서드에 "\*args, **kwargs" 형태로 인자를 넘겨 받고 그대로 부모 메서드에 넘겨준다면 당신의 코드는 Django의 변경사항에 관계없이 항상 잘 동작하게 됩니다.

	> *__재정의한 모델 메서드는 벌크 조작시(대량작업)에는 호출되지 않습니다.__*
	> 
	> QuerySet을 사용하여 대량으로 객체를 삭제할 때 또는 계단식 삭제의 결과로 객체의 delete () 메소드가 반드시 호출되지는 않습니다. 사용자 정의 삭제 논리를 실행하려면 pre\_delete 및 / 또는 post\_delete 신호를 사용할 수 있습니다.
	
	> 불행하게도 save (), pre\_save 및 post\_save가 호출되지 않으므로 대량으로 객체를 만들거나 업데이트 할 때 해결 방법이 없습니다.
	
-

- *__Executing custom SQL__*

- SQL 문을 직접 작성해서 실행할 수도 있습니다. 이 부분에 대해서는 "using raw SQL" 문서를 참고하세요.

-

- *__Model inheritance__*

- Django 에서의 모델 상속은 파이썬에서의 클래스 상속과 거의 동일한 형태로 이루어 집니다. 단, 모델 상속의 경우에 베이스 클래스는 django.db.models.Model 클래스의 서브 클래스여야 합니다. 

- 이때, 부모 모델이 자신의 데이터베이스 테이블을 가지도록 할 것인지, 아니면 부모 모델은 실제로 테이블을 생성하지 않고 자식 모델들이 부모 모델에 선언된 공통 필드를 각각 자신의 테이블에 생성할지를 결정해야 합니다.

- 위와 같은 특징으로 인해 Django에서는 3가지 스타일의 모델 상속이 존재합니다.

	- 먼저 Abstract class가 있습니다. 이 경우 부모 클래스는 실제로 테이블을 만들지 않고 자식 클래스들에 필드 선언이나 메서드 선언만 상속해 줍니다. 이를 상속 받은 자식 모델은 데이터베이스 테이블에 부모 클래스와 자기 자신에 선언된 필드들을 가지게 됩니다.
	
	- 두번째는 이미 존재하는 모델(아마도 다른 app에서 선언되어 사용중인..)을 상속하는 경우입니다. 이 경우 부모 모델은 자신의 데이터베이스 테이블을 가지며 자식 모델과는 별개로 독립적으로 사용 가능합니다. 이를 Multi-table 상속이라고 부릅니다.
	
	- 마지막으로, 모델의 필드 선언은 전혀 변경하지 않고 파이썬 레벨의 코드만 수정하고자 하는 경우 사용하는 방법입니다. 이 경우, Proxy 모델을 사용합니다.

-

- *__Abstract base classes__*

- 추상 클래스 방식은 여러개의 모델 클래스가 **공통적인 정보**를 가지도록 하고 싶은 경우에 유용합니다. **Meta클래스에 abstract=True 옵션을 선언하면 그 모델 클래스는 추상클래스가 됩니다.** 이렇게 만들어진 추상클래스는 데이터베이스에 **테이블을 생성하지 않습니다.** 다만, 다른 모델들이 이 클래스를 상속받을 수 있으며, 부모클래스에 선언된 필드들은 자식 클래스의 테이블에 추가됩니다. 이때 부모 클래스와 자식 클래스가 동일한 이름의 필드를 가지고 있는 경우에는 Django가 예외를 발생시킵니다.
- 아래는 추상 클래스 방식의 예제입니다.

	```
	from django.db import models
	
	class CommonInfo(models.Model):
	    name = models.CharField(max_length=100)
	    age = models.PositiveIntegerField()
	
	    class Meta:
	        abstract = True
	
	class Student(CommonInfo):
	    home_group = models.CharField(max_length=5)
	```
	
- **결과적으로 Student 모델은 3개의 필드(name, age, home_group)를 가지게 됩니다.** CommonInfo 모델은 일반적인 모델클래스 처럼 **독립적으로 사용 될 수 없습니다.** 앞에서 언급했듯이 데이터베이스에 테이블을 만들지도 않고 Manager도 가지지 않습니다. 또한 인스턴스화 할 수도 없습니다. 

- 추상클래스를 이용한 모델 상속은 데이터베이스에 영향을 주지 않고, **파이썬 레벨에서 공통 필드를 하나의 부모 클래스에서 관리할 수 있는 방법을 제공해줍니다.** 앞에서 설명했듯이, 이 경우 자식 모델 당 하나의 테이블만 만들어 진다는 것을 명심하세요.

-

- *__Meta inheritance__*

- 자식 클래스가 Meta 클래스를 가지지 않는 경우, 자식 클래스는 부모의 메타 클래스를 상속 받습니다. 만약 자식 클래스에서 확장을 위해 부모 Meta 클래스를 상속 받으려면 아래와 같이 부모 클래스에 선언된 Meta 클래스로부터 상속 받으면 됩니다. 

	```
	from django.db import models

	class CommonInfo(models.Model):
	    # ...
	    class Meta:
	        abstract = True
	        ordering = ['name']
	
	class Student(CommonInfo):
	    # ...
	    class Meta(CommonInfo.Meta):
	        db_table = 'student_info'
	```

- 이 경우 Django는 내부적으로 한가지 조정을 합니다. 자식클래스의 Meta 클래스를 활성화하기 전에, abstract 옵션을 False로 변경합니다. 즉, 추상 클래스를 상속한다고 해서 자식클래스 또한 추상 클래스가 되지는 않는다는 얘기입니다. 물론 자식클래스 또한 추상 클래스가 되길 원할 수도 있습니다. 이경우에는 자식 클래스의 Meta 클래스에서 abstract=True 옵션을 한번 더 선언해주면 됩니다.
- 몇몇 Meta 클래스 옵션은 추상 클래스에는 사용할 수 없습니다. 예를들면 추상 클래스는 데이터베이스 테이블을 만들지 않으므로, db_table 옵션은 아무 의미가 없습니다. 물론 자식 클래스들에는 상속됩니다. 그런데 모든 자식 클래스들이 동일한 테이블을 사용하도록 하려는것은 아닐겁니다. 이와같이, 추상 클래스에서 Meta 클래스 옵션을 선언할 때 주의를 기울여야 합니다.

-

- *__Be careful with related_name__*

- Person 모델에 ForeignKey 필드가 하나 있다고 칩시다. 이 때, 이 ForeignKey 필드는 Group 모델과 관계를 가집니다. 이 경우 기본적으로 Group 모델에 person\_set 이라는 어트리뷰트가 자동으로 생성되며, 이 어트리뷰트는 Group 모델과 관계된 Person 모델들을 엑세스 할 수 있도록 해줍니다. 이때 related\_name 옵션을 지정하여, person\_set이 아닌 다른 이름을 직접 지정할 수 있습니다. 
그런데, Animal 이라는 모델 또한 Group 모델에 대한 ForeignKey 필드를 가지고 있다면 어떻게 될까요? Group 필드는 person\_set 과 animal\_set 이라는 역참조 어트리뷰트를 가지게 됩니다. 그런데, Person 모델과 Animal 모델의 ForeignKey 필드에 related\_name 옵션을 동일하게 설정했다고 생각해봅시다. 이 경우 각각의 모델에 대한 역참조 어트리뷰트가 중복되기 때문에 에러가 발생됩니다. 물론 이 경우 Person 모델과 Animal 모델 각각의 related\_name 값을 다르게 설정해서 문제를 해결할 수 있습니다.

- 그런데 만약 추상 모델에 관계필드가 선언되어있고, related\_name 옵션을 설정했다고 가정해봅시다. 이 추상 모델을 상속 받는 자식들은 동일한 역참조 이름을 가지는 관계필드를 가지게 됩니다.

- 예, app common / models.py :

	```
	from django.db import models

	class Base(models.Model):
	    m2m = models.ManyToManyField(
	        OtherModel,
	        related_name="%(app_label)s_%(class)s_related",
	        related_query_name="%(app_label)s_%(class)ss",
	    )
	
	    class Meta:
	        abstract = True
	
	class ChildA(Base):
	    pass
	
	class ChildB(Base):
	    pass
	```
	
- rare/models.py:

	```
	from common.models import Base

	class ChildB(Base):
	    pass
	```
	
- common/models.py에 선언된 클래스들 부터 살펴봅시다. ChildA.m2m 필드의 역참조 이름은 common\_childa\_related 가 되며, ChildB.m2m 필드는 common\_childb\_related 가 됩니다. 즉, OtherModel은 common\_childa\_related, common\_childb\_related 두 개의 역참조 어트리뷰트를 가지게 됩니다.
- rare/models.py 에 선언된 모델의 경우에 역참조 이름은 rare\_childb\_related 가 됩니다. 
- 참고로, 만약 이 경우에 Base 모델 클래스에서 m2m 필드에 related\_name 옵션을 지정하지 않으면, 상속받은 자식클래스의 이름을 기준으로 역참조 이름이 결정됩니다. 즉, ChildA 클래스는 childa\_set, ChildB 클래스는 childb\_set 으로 역참조 이름이 결정됩니다.
- 그런데, **위의 예제에서 common 앱과 rare 앱이 동일한 이름의 모델(ChildB)이 Base 모델을 상속받았습니다. 그러므로 역참조 이름이 중복(childb\_set)되어 에러가 발생됩니다.** (역참조 이름을 지정하는 이유)

-

- *__Multi-table inheritance__*

- Multi-table 상속은 부모 모델이든 자식 모델이든 모두 각자의 데이터베이스 테이블을 가집니다. 즉, 공통부분의 데이터는 부모모델의 테이블에 저장하고, 자식모델의 데이터는 자식모델의 테이블에 저장되며, 자식 모델은 부모 모델에 대한 링크를 가집니다. 이때, 링크는 내부적으로 OneToOneField를 사용합니다.

- 아래의 Multi-table 상속의 예제입니다.

	```
	from django.db import models

	class Place(models.Model):
	    name = models.CharField(max_length=50)
	    address = models.CharField(max_length=80)
	
	class Restaurant(Place):
	    serves_hot_dogs = models.BooleanField(default=False)
	    serves_pizza = models.BooleanField(default=False)
	```
	
- Place 모델에 선언된 모든 필드는 Restaurant 모델에서도 사용가능합니다. 물론, 각 모델의 필드값들은 서로 다른 테이블에 각각 저장됩니다.

	```
	>>> Place.objects.filter(name="Bob's Cafe")
	>>> Restaurant.objects.filter(name="Bob's Cafe")
	```
	
- 만약 Place 모델을 통해서 Restaurant 모델 객체를 쿼리할 수 있습니다. 단 **Place 모델에 선언된 필드만 엑세스**할 수 있으며, **자동으로 제공되는 restaurant 어트리뷰트를 통해 Restaurant 객체에 접근 할 수도 있습니다.** 이때, 어트리뷰트 이름은 **자식 클래스의 이름을 소문자화한 이름**입니다. 

	```
	>>> p = Place.objects.get(id=12)
	# If p is a Restaurant object, this will give the child class:
	>>> p.restaurant
	<Restaurant: ...>
	```

- 하지만, 위의 예제에서 p가 Restaurant 객체가 아니라면(Place 모델을 통해 직접 생성되었다거나, Restaurant 모델이 아닌 다른 자식클래스를 통해 만들어진 경우), restaurant 어트리뷰트에 접근하면 Restaurant.DoesNotExist 예외가 발생됩니다.

- 식당에 자동으로 생성 된 OneToOneField가 다음과 같이 표시됩니다.

	```
	place_ptr = models.OneToOneField(
	    Place, on_delete=models.CASCADE,
	    parent_link=True,
	)
	```
	
- 식당에서 parent_link = True로 자신의 OneToOneField를 선언하여 해당 필드를 재정의 할 수 있습니다.

-

- *__Meta and multi-table inheritance__*

- multi-table 상속 관계에서 자식 모델은 부모 모델의 메타클래스를 상속 받아야 할까요? 부모 모델과 자식 모델 모두 자신의 테이블을 가지기 때문에 메타 클래스를 상속받는 경우 여러가지 문제를 발생시킬 수 있습니다. 

- 이와같은 이유로, multi-table 상속의 경우 기본적으로 자식모델은 부모모델의 Meta 클래스를 상속받지 않습니다. 단, 자식모델에 ordering, get\_latest_by 옵션이 지정되지 않은 경우에 한해, 부모 모델의 해당 설정값을 상속받습니다.

- 만약 부모 모델의 ordering 값을 상속받고 싶지 않다면, 자식모델에 ordering 옵션을 아래와 같이 설정해주면 됩니다.

	```
	class ChildModel(ParentModel):
    # ...
    class Meta:
        # Remove parent's ordering effect
        ordering = []
	```
	
-

- *__Inheritance and reverse relations__*

- 예를들어 아래와 같이 Supplier 모델이 Place 모델을 상속받으면서, Place 모델에 대한 ManyToManyField도 가지고 있다고 하면

	```
	class Supplier(Place):
		customers = models.ManyToManyField(Place)
	```
	
- 아래와 같이 에러가 발생됩니다.

	```
	Reverse query name for 'Supplier.customers' clashes with reverse query
	name for 'Supplier.place_ptr'.
	
	HINT: Add or change a related_name argument to the definition for
	'Supplier.customers' or 'Supplier.place_ptr'.
	```
	
- ManyToManyField 선언에 아래와 같이 related_name 옵션을 추가해주면 이 문제를 해결할 수 있습니다.

	```
	models.ManyToManyField(Place, related_name='provider')
	```
	
-

- *__Specifying the parent link field__*

- 앞에서 언급했듯이 multi-table 상속의 경우 OneToOneField 가 자동으로 생성됩니다. 만약 이 OneToOneField를 직접 지정하고 싶다면, OneToOneField 를 추가하고 필드 옵션에 parent_link=True로 설정해주면 됩니다.

-

- *__Proxy models__*

- multi-table 상속을 사용하는 경우, 각각의 자식 클래스들 마다 테이블이 생성됩니다. 부모 모델이 가지는 데이터 이외에 추가적으로 자식 모델이 가지는 데이터를 저장하기 위한 당연한 동작입니다. 하지만 가끔은 부모 모델의 메서드(파이썬 코드)만 재정의 한다던가 새로 추가하고 싶을 수도 있습니다. 즉, 테이블을 가지는 모델을 상속받되, 자식모델은 테이블을 만들필요가 없는 경우에 해당됩니다.

- 이런 경우에 proxy 모델 상속을 사용합니다. 이 경우 proxy 모델(자식모델)을 이용해서 모델객체를 만들고, 수정하고 삭제할 수도 있습니다. 물론 이러한 동작은 원본(부모)모델의 테이블 상에서 이루어 집니다. 

- proxy 모델이 원본모델과 다른 점은 기본 정렬값과 같은 설정값을 원하는 데로 변경할 수 있다는 점입니다. 물론 원본 모델의 설정값은 변경되지 않습니다.

- Proxy 모델 선언은 일반 모델들과 동일합니다. 다만, Meta 클래스에 proxy=True 로 선언해주면 됩니다.

- 예를들어, Person 모델에 메서드 하나를 추가하고 싶다면 아래와 같이 할 수 있습니다.

	```
	from django.db import models

	class Person(models.Model):
	    first_name = models.CharField(max_length=30)
	    last_name = models.CharField(max_length=30)
	
	class MyPerson(Person):
	    class Meta:
	        proxy = True
	
	    def do_something(self):
	        # ...
	        pass

	```
	
- MyPerson 클래스는 부모 클래스인 Person 클래스의 테이블을 사용합니다. 그렇기 때문에, 아래와 같이 Person 모델로 레코드를 추가하더라도 MyPerson 클래스로 조회가 가능합니다.

	```
	>>> p = Person.objects.create(first_name="foobar")
	>>> MyPerson.objects.get(first_name="foobar")
	<MyPerson: foobar>
	```
	
- 메서드를 재정의나 추가하는것 외에도, 기본 정렬 옵션을 변경할 수도 있습니다. 

	```
	class OrderedPerson(Person):
	    class Meta:
	        ordering = ["last_name"]
	        proxy = True
	```
	
- 이제, Person 모델을 이용한 쿼리를 정렬되지 않은 상태로, OrderedPerson 모델로 쿼리할때는 last_name 기준으로 정렬되어 리턴됩니다.

-

- *__QuerySets still return the model that was requested__*

- Person 모델로 쿼리하는 경우 리턴되는 모델 객체는 MyPerson이 아니라 Person 객체입니다. 즉, 어떤 모델 클래스로 쿼리했는지에 따라 리턴되는 모델 객체의 타입이 결정됩니다. proxy 모델에서 변경한 사항은 부모 모델에 영향을 끼치지 않는 다는 사실을 기억하시기 바랍니다.

-

- *__Base class restrictions__*

- proxy 모델은 하나의 (추상 클래스가 아닌)모델만 상속받을 수 있습니다. proxy 모델은 여러개의 테이블로부터 레코드를 쿼리하는 기능은 제공하지 않기 때문입니다. 추상 모델 클래스의 경우에는 그 추상 모델 클래스가 필드를 가지지 않는다면 몇 개든 상속이 가능합니다. 

- Proxy 모델은 자신이 선언하지 않은 Meta 옵션에 한해 부모(추상 클래스가 아닌) 모델로부터 상속받습니다.

-

- *__Proxy model managers__*

- Proxy 모델에 manager를 지정하지 않는 경우, 부모 모델의 manager를 상속받습니다. 직접 지정한 경우, 지정한 manager가 디폴트로 사용되며, 부모클래스의 manager도 사용할 수 있습니다.

- 아래와 같이 기본 manager를 변경할 수 있습니다.

	```
	from django.db import models

	class NewManager(models.Manager):
	    # ...
	    pass
	
	class MyPerson(Person):
	    objects = NewManager()
	
	    class Meta:
	        proxy = True
	```
	
- 아래와 같이 부모 클래스의 기본 manager를 상속 받되, 새로운 manager를 추가하려면 아래와 같이 추상클래스에 새로운 manager를 선언하고 그 추상클래스를 상속받으면 됩니다.

	```
	# Create an abstract class for the new manager.
	class ExtraManagers(models.Model):
	    secondary = NewManager()
	
	    class Meta:
	        abstract = True
	
	class MyPerson(Person, ExtraManagers):
	    class Meta:
	        proxy = True
	```
	
- 위와 같이 사용하는 경우가 흔하지는 않습니다. 다만, 위와 같이 할 수 있다는 것만 알아두세요.

-

- *__Differences between proxy inheritance and unmanaged models
__*

- 모델 클래스를 하나 선언해서 managed=False 옵션을 주면, 해당 모델은 자동으로 테이블을 생성하지 않게 됩니다. 직접 테이블을 만들어 주어야 합니다. 그런데 여기에 db_table 옵션에 기존에 존재하는 모델의 테이블 이름을 지정하게 되면 어떨까요? proxy 모델과 거의 비슷해 보입니다.

- 하지만 이 둘은 조금 다른 특징을 가지며, 목적에 맞게 사용해야합니다.

- 한가지 차이점은 unmanaged 모델의 경우 직접 데이터베이스 테이블을 생성/수정 해주어야 한다는 것입니다. proxy모델의 경우 원본 모델이 변경되더라도 proxy 모델을 수정할 일은 없습니다. 하지만 unmanaged 모델의 경우, 원본 모델에 변경사항이 생길때마다 unmanaged 모델 클래스 또한 동일하게 수정해주어야 합니다. 생각만 해도 피곤한 일입니다.

- 또다른 차이점은 manager 가 처리되는 방식입니다. proxy 모델의 경우 원본 모델의 디폴트 Manager 를 포함한 모든 Manager를 상속받습니다. unmanaged 모델의 경우 Django 입장에서 원본 모델과 아무런 관련이 없기 때문에 manager는 unmanaged 모델 자체의 선언에 따릅니다. 참고로 multi-table 모델의 경우에는 부모 모델의 manager를 상속받지 않습니다. 

- 두가지 방식(proxy, unmanaged)을 구현하면서 우리는 하나의 옵션으로 합쳐보려는 시도를 했었습니다만, API가 복잡하고 이해하기 어려워져버려서 그냥 2가지 옵션을 따로 제공하기로 했습니다. 

- 이 2가지 옵션 중 어떤것을 사용할지를 결정하는 일반적인 규칙은 아래와 같습니다.

	- 만약에 당신이 이미 존재하는 모델이나 데이터베이스 테이블을 참조하되, 원본 테이블의 모든 컬럼이 필요하지 않다면, Meta.managed=False 옵션을 사용하세요. Django에 의해 제어되지 않는 데이터베이스 뷰나 테이블을 사용하는 경우에 유용합니다.

	- 만약에 기존 모델의 파이썬 코드들을 오버라이드 하되, 원본 모델과 동일한 필드를 가지도록 하고 싶다면 Meta.proxy=True 옵션을 사용하세요.

-

- *__Multiple inheritance__*

- 파이썬의 상속과 마찬가지로 Django 모델 또한 다중 상속(Multiple Inheritance)이 가능합니다. 단, 이 경우 파이썬의 "name resolution rules" 이 적용됩니다. 예를들어, 부모 클래스들이 각각 Meta 클래스를 가지는 경우 첫번째 부모의 Meta 클래스를 상속받게 되며, 나머지 부모 클래스의 Meta 클래스는 무시됩니다.

- 일반적으로 여러 부모 모델로부터 상속받는 경우가 별로 없습니다만, 많이 쓰이는 경우는 'mix-in' 클래스 들입니다. 공통적으로 사용되는 필드나 메서드들을 묶어 하나의 클래스로 선언하고 이 클래스를 여러 모델 클래스에 상속하는 경우 입니다. 물론 이 경우, 특정 필드가 어느 부모 클래스에 선언되어있는 것인지 명확하게 간단명료하게 정리되어야 합니다.

- Django 1.7 이전에는 id 필드를 가지는 여러 모델로부터 상속을 받더라도 에러를 발생시키지 않았습니다. 하지만 이 경우 데이터 손실이 발생할 수 있습니다. 아래의 예제를 예로들면, "id" 필드가 중복되어 Article.id 필드는 무시됩니다.

	```
	class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    ...

	class Book(models.Model):
	    book_id = models.AutoField(primary_key=True)
	    ...
	
	class BookReview(Book, Article):
	    pass
	```

- 아래의 예제는 이로인한 문제점을 보여주고 있습니다. 아래의 예제에서 review 객체의 id값은 Book 클래스의 id 필드에 의해 결정됩니다. "class BookReview(Book, Article):" 에서 Book을 먼저 선언해주었기 때문입니다. 
결과적으로 review 객체의 id 값은 Book 모델에 의해 자동생성된 ID값인 1이 되며, 이로인해 Article 객체가 새로 추가되는 것이 아니라 id값이 1인 Article 객체를 덮어쓰게 됩니다.

	```
	>>> article = Article.objects.create(headline='Some piece of news.')
	>>> review = BookReview.objects.create(
	...     headline='Review of Little Red Riding Hood.',
	...     title='Little Red Riding Hood')
	>>>
	>>> assert Article.objects.get(pk=article.pk).headline == article.headline
	Traceback (most recent call last):
	  File "<console>", line 1, in <module>
	AssertionError
	>>> # the "Some piece of news." headline has been overwritten.
	>>> Article.objects.get(pk=article.pk).headline
	'Review of Little Red Riding Hood.'
	```
	
- 이러한 상황을 해결하려면 id 필드가 겹치지 않도록 부모 모델의 id 필드를 명시적으로 선언해주면 됩니다.

	```
	class Article(models.Model):
	    article_id = models.AutoField(primary_key=True)
	    ...
	
	class Book(models.Model):
	    book_id = models.AutoField(primary_key=True)
	    ...
	
	class BookReview(Book, Article):
	    pass
	```
	
- 또는 아래와 같이 id 필드(AutoField)를 가지는 공용 모델(Piece)을 만들어 id 값이 항상 공용모델을 기준으로 생성되도록 할 수도 있습니다.

	```
	class Piece(models.Model):
	    pass
	
	class Article(Piece):
	    ...
	
	class Book(Piece):
	    ...
	
	class BookReview(Book, Article):
	    pass
	```
	
-

- *__Field name “hiding” is not permitted__*

- 보통의 파이썬 클래스 상속에서, 자식 클래스는 부모 클래스의 어트리뷰트를 오버라이드 할 수 있습니다. 하지만 Django에서 필드 어트리뷰트의 경우에는 오버라이드가 허용되지 않습니다. 만약 부모 클래스가 author 라는 이름의 필드가 선언되어 있다면, 자식클래스는 같은 이름의 필드를 선언할 수 없습니다.

- 이러한 제약은 필드 어트리뷰트에만 해당합니다. 일반 파이썬 어트리뷰트는 원한다면 오버라이드 가능합니다. multi-table 상속의 경우에는 어트리뷰트 이름이 다르더라도 데이터베이스 컬럼명을 직접 지정하여, 부모와 자식 테이블 각각의 컬럼명을 동일하게 사용할 수는 있습니다.

- 참고로 Django는 부모 모델의 필드를 오버라이드 하면 FieldError를 발생시킵니다.

