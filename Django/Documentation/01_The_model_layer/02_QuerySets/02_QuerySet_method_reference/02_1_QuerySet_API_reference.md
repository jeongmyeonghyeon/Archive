### QuerySet API reference - 2

<br>

*__Methods that do not return QuerySets__*  
*__(QuerySet를 반환하지 않는 메서드)__*

- 다음 QuerySet 메서드는 QuerySet을 평가하고 QuerySet 이외의 것을 반환합니다.

- 이러한 메소드는 캐시를 사용하지 않습니다 ([캐싱 및 QuerySet][Caching and QuerySets] 참조). 오히려, 그들은 호출 될 때마다 데이터베이스를 조회합니다.

#### **get()**

- **get(\*\*kwargs)**

	- 지정된 참조 매개 변수와 일치하는 객체를 반환합니다.이 조회는 [필드 조회][Field lookups]에서 설명하는 형식이어야합니다.

	- `get()`은 **둘 이상의 객체가 발견되면** [MultipleObjectsReturned]를 발생시킵니다. [MultipleObjectsReturned] 예외는 모델 클래스의 속성입니다.

	- 지정된 매개 변수에 대해 개체를 찾을 수없는 경우 `get()`은 [DoesNotExist] 예외를 발생시킵니다. 이 예외는 모델 클래스의 속성입니다. 예:

		```
		Entry.objects.get(id='foo')  
		# raises Entry.DoesNotExist
		```
		
	- [DoesNotExist] 예외는 [django.core.exceptions.ObjectDoesNotExist]에서 상속되므로 **여러 개의 DoesNotExist 예외를 대상으로 지정할 수 있습니다.** 예:

		```
		from django.core.exceptions import ObjectDoesNotExist
		try:
		    e = Entry.objects.get(id=3)
		    b = Blog.objects.get(id=1)
		except ObjectDoesNotExist:
		    print("Either the entry or blog doesn't exist.")
		```
		
	- 쿼리 세트가 한 행을 반환 할 것으로 **예상되는 경우** 인수없이 get ()을 사용하여 해당 행에 대한 객체를 반환 할 수 있습니다.

		```
		entry = Entry.objects.filter(...).exclude(...).get()
		```



[Caching and QuerySets]: https://docs.djangoproject.com/en/1.11/topics/db/queries/#caching-and-querysets

[Field lookups]: https://docs.djangoproject.com/en/1.11/ref/models/querysets/#id4

[MultipleObjectsReturned]: https://docs.djangoproject.com/en/1.11/ref/exceptions/#django.core.exceptions.MultipleObjectsReturned

[DoesNotExist]: https://docs.djangoproject.com/en/1.11/ref/models/instances/#doesnotexist

[django.core.exceptions.ObjectDoesNotExist]: https://docs.djangoproject.com/en/1.11/ref/exceptions/#django.core.exceptions.ObjectDoesNotExist