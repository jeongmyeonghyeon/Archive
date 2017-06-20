### The Forms API

<br>

- **About this document**

	- 이 문서는 Django의 폼 API에 대한 자세한 내용을 다룹니다. 먼저 [introduction to working with forms]를 읽어야합니다.

[introduction to working with forms]: https://docs.djangoproject.com/en/1.11/ref/forms/api/

<br>

*__Bound and unbound forms__*

- Form 인스턴스는 데이터 세트에 바인딩되거나 바인딩되지 않습니다.

	- 데이터 세트에 바인딩되어있는 경우 **해당 데이터의 유효성을 검사**하고 **HTML 형식의 데이터를 HTML 형식의 데이터로 표시** 할 수 있습니다.
	- 언 바운드 인 경우 유효성을 검사 할 데이터가 없기 때문에 **유효성 검사를 수행 할 수 없지만 빈 양식을 HTML로 렌더링** 할 수는 있습니다.

**class Form**

- **언 바운드 Form 인스턴스**를 만들려면 클래스를 인스턴스화하기 만하면됩니다.

	```
	>>> f = ContactForm()
	```
	
- **데이터를 폼에 바인딩하려면** 데이터를 dictionary로 Form 클래스 생성자의 첫 번째 매개 변수로 전달합니다.

	```
	data = {'subject': 'hello',
	...         'message': 'Hi there',
	...         'sender': 'foo@example.com',
	...         'cc_myself': True}
	>>> f = ContactForm(data)
	```
	
- 이 dictionary에서 **키**는 Form 클래스의 속성에 해당하는 **필드 이름**입니다. **값은 유효성을 검사하려는 데이터**입니다. 이들은 일반적으로 문자열이지만, 문자열이 될 필요는 없습니다. 전달하는 데이터의 유형은 [Field]에 따라 달라지며, 잠시 후에 살펴 보겠습니다.

[Field]: https://docs.djangoproject.com/en/1.11/ref/forms/fields/#django.forms.Field

**Form.is_bound**

- 런타임에 바인딩 된 폼 인스턴스와 언 바운드 폼 인스턴스를 구별해야하는 경우 폼의 `is_bound` 특성 값을 확인하십시오

	```
	>>> f = ContactForm()
	>>> f.is_bound
	False
	>>> f = ContactForm({'subject': 'hello'})
	>>> f.is_bound
	True
	```
	
- 빈 dictionary를 전달하면 빈 데이터가있는 바운드 양식이 만들어집니다.

	```
	>>> f = ContactForm({})
	>>> f.is_bound
	True
	```
	
- 바운드 Form 인스턴스가 있고 어떻게든 데이터를 변경하려는 경우 또는 언 바운드 Form 인스턴스를 일부 데이터에 바인딩하려면 다른 Form 인스턴스를 만듭니다. **Form 인스턴스에서 데이터를 변경할 수 있는 방법은 없습니다.** Form 인스턴스가 만들어지면 데이터가 있는지 여부에 관계없이 해당 인스턴스를 수정할 수 없습니다.

<br>

-

*__Using forms to validate data__*  
*__form을 사용해 데이터 유효성 검사하기__*

**Form.clean()**

- 상호 의존적인 필드에 대해 사용자 지정 유효성 검사를 추가해야하는 경우 양식에 `clean()` 메서드를 구현합니다. 사용법은 [Cleaning and validating fields that depend on each other]를 참조하십시오.

[Cleaning and validating fields that depend on each other]: https://docs.djangoproject.com/en/1.11/ref/forms/validation/#validating-fields-with-clean

**Form.is_valid()**

- **Form 객체의 기본 작업은 데이터의 유효성을 검사하는 것입니다.** **바운드 Form 인스턴스를 사용**하여 `is_valid()` 메서드를 호출하여 유효성 검사를 실행하고 데이터가 유효한지 여부를 지정하는 boolean을 반환합니다.

	```
	>>> data = {'subject': 'hello',
	...         'message': 'Hi there',
	...         'sender': 'foo@example.com',
	...         'cc_myself': True}
	>>> f = ContactForm(data)
	>>> f.is_valid()
	True
	```
	
- 잘못된 데이터로 시도해 보겠습니다. 이 경우 제목이 비어 있습니다 (모든 필드가 기본적으로 필요하므로 오류). 발신자는 유효한 이메일 주소가 아닙니다.

	```
	>>> data = {'subject': '',
	...         'message': 'Hi there',
	...         'sender': 'invalid email address',
	...         'cc_myself': True}
	>>> f = ContactForm(data)
	>>> f.is_valid()
	False
	```
	
**Form.errors**

- errors 속성에 액세스하여 오류 메시지 dictionary 가져 오기

	```
	>>> f.errors
	{'sender': ['Enter a valid email address.'], 'subject': ['This field is required.']}
	```
	
- 이 dictionary에서 **키는 필드 이름**이고 **값은 오류 메시지**를 나타내는 유니 코드 문자열의 목록입니다. 필드에 여러 오류 메시지가있을 수 있으므로 오류 메시지는 목록에 저장됩니다.

- 먼저 `is_valid()`를 호출하지 않고도 오류에 액세스 할 수 있습니다. 양식의 데이터는 처음으로 `is_valid()` 또는 액세스 오류를 호출 할 때 유효성이 검사됩니다.

- **유효성 검사 루틴**은 오류에 액세스 한 횟수 또는 `is_valid()`를 호출 한 횟수에 관계없이 **한 번만 호출됩니다.** 즉, 유효성 검사에 부작용이있을 경우 해당 부작용은 한 번만 발생합니다.

**Form.errors.as_data()**

- 필드를 원래의 ValidationError 인스턴스에 매핑하는 dict를 반환합니다.

	```
	>>> f.errors.as_data()
	{'sender': [ValidationError(['Enter a valid email address.'])],
	'subject': [ValidationError(['This field is required.'])]}
	```
	
- 해당 코드로 오류를 식별해야 할 때마다 이 메서드를 사용하십시오. 이렇게하면 주어진 오류가있을 때 오류 메시지를 다시 작성하거나보기에 사용자 지정 논리를 작성하는 작업을 수행 할 수 있습니다. 또한 맞춤 형식 (예 : XML)으로 오류를 직렬화하는 데 사용할 수도 있습니다. 예를 들어, `as_json()`은 `as_data()`에 의존합니다.

- `as_data()` 메소드의 필요성은 이전 버전과의 호환성 때문입니다. 이전에는 ValidationError 인스턴스가 렌더링 된 오류 메시지가 Form.errors 사전에 추가되는 즉시 손실되었습니다. 이상적으로 Form.errors는 ValidationError 인스턴스와 as_ 접두어가있는 메소드를 렌더링 할 수 있지만 Form.errors에서 렌더링 된 오류 메시지를 예상하지 못하도록 다른 방법으로 처리해야합니다.

**Form.errors.as_json(escape_html=False)**

- JSON으로 직렬화(serialized) 된 오류를 반환합니다.

	```
	>>> f.errors.as_json()
	{"sender": [{"message": "Enter a valid email address.", "code": "invalid"}],
	"subject": [{"message": "This field is required.", "code": "required"}]}
	```
	
- 기본적으로 `as_json()`은 출력을 이스케이프 처리하지 않습니다. 클라이언트가 응답을 해석하고 페이지에 오류를 삽입하는 양식보기에 AJAX 요청과 같은 용도로 사용하는 경우 클라이언트 측에서 결과를 이스케이프 처리하여 십자가가 표시되지 않도록해야합니다 - 사이트 스크립팅 공격. jQuery와 같은 자바 스크립트 라이브러리를 사용하는 것은 간단합니다. 단순히 `.html()` 대신 `$(el).text(errorText)`를 사용하십시오.

- 어떤 이유로 클라이언트 측 이스케이핑을 사용하지 않으려는 경우 `escape_html = True`로 설정하면 오류 메시지가 이스케이프되므로 HTML에서 직접 사용할 수 있습니다.

**Form.add_error(field, error)**

- 이 메서드를 사용하면 `Form.clean()` 메서드 내에서 또는 폼 외부에서 특정 필드에 오류를 추가 할 수 있습니다. 예를 들어보기에서

- field 인수는 오류가 추가되어야하는 필드의 이름입니다. 이 값이 None이면 오류는 `Form.non_field_errors()`가 반환 한 비 필드 오류로 처리됩니다.

- error 인수는 단순한 문자열이거나 ValidationError의 인스턴스가 될 수 있습니다. 양식 오류를 정의 할 때 유용한 정보는 [ValidationError]를 참조하십시오.

- `Form.add_error()`는 `cleaned_data`에서 관련 필드를 자동으로 제거합니다.


[ValidationError]: https://docs.djangoproject.com/en/1.11/ref/forms/validation/#raising-validation-error

**Form.has_error(field, code=None)**

- 이 메소드는 필드에 특정 오류 코드가있는 오류가 있는지 여부를 지정하는 부울을 반환합니다. code가 None이면 필드에 오류가있는 경우 True를 반환합니다.

- 필드 오류가 아닌지 확인하려면 `NON_FIELD_ERRORS`를 필드 매개 변수로 사용하십시오.

**Form.non_field_errors()**

- 이 메소드는, 특정의 필드와 관련 지을 수 있지 않은 Form.errors로부터의 에러의리스트를 돌려줍니다. 여기에는 `Form.clean()`에서 발생한 ValidationErrors와 `Form.add_error(None, "...")`를 사용하여 추가 된 오류가 포함됩니다.

*__Behavior of unbound forms__*

- 데이터가없는 폼의 유효성을 검사하는 것은 의미가 없지만, 레코드의 경우, 언 바운드 폼의 경우 다음과 같이됩니다.

	```
	>>> f = ContactForm()
	>>> f.is_valid()
	False
	>>> f.errors
	{}
	```
	
	> 유효성 검사와 관련된 클래스라 그런지 error를 처리하는 메서드가 많은듯...0.0 `clean()`, `is_valid()`, `errors()` 말고는 음...
	
<br>

-

*__Dynamic initial values__*

**Form.initial**

- `initial`을 사용하여 런타임에 양식 필드의 초기 값을 선언하십시오. 예를 들어, 현재 세션의 사용자 이름으로 사용자 이름 필드를 채울 수 있습니다.

- 이를 수행하려면 Form에 대한 initial 인수를 사용하십시오. 이 인수는 필드 이름을 초기 값으로 매핑하는 dict여야합니다. 초기값을 지정하는 입력란 만 포함하십시오. 양식에 모든 입력란을 포함 할 필요는 없습니다.

	```
	>>> f = ContactForm(initial={'subject': 'Hi there!'})
	```
	
- 이 값은 **언 바운드 형식에만 표시되며 특정 값이 제공되지 않으면 대체 값으로 사용되지 않습니다.**

- Field가 initial을 정의하고 Form을 인스턴스화 할 때 initial을 포함하면 후자의 initial이 우선합니다. 이 예에서는 [Field] 수준과 form 인스턴스 수준에서 초기 값이 제공되며 후자는 우선 순위를 갖습니다:

	```
	>>> from django import forms
	>>> class CommentForm(forms.Form):
	...     name = forms.CharField(initial='class')
	...     url = forms.URLField()
	...     comment = forms.CharField()
	>>> f = CommentForm(initial={'name': 'instance'}, auto_id=False)
	>>> print(f)
	<tr><th>Name:</th><td><input type="text" name="name" value="instance" required /></td></tr>
	<tr><th>Url:</th><td><input type="url" name="url" required /></td></tr>
	<tr><th>Comment:</th><td><input type="text" name="comment" required /></td></tr>
	```
	
**`Form.get_initial_for_field(field, field_name)`**

- **New in Django 1.11.**

- `get_initial_for_field()`를 사용하여 form 필드의 초기 데이터를 검색하십시오. 이 명령은 `Form.initial` 및 `Field.initial`에서 이 순서대로 데이터를 검색하고 호출 가능한 초기 값을 평가합니다.

<br>

-

*__Checking which form data has changed__*

**Form.has_changed()**

- 양식 데이터가 초기 데이터에서 변경되었는지 확인해야 할 때 양식에서 `has_changed()` 메소드를 사용하십시오.

	```
	>>> data = {'subject': 'hello',
	...         'message': 'Hi there',
	...         'sender': 'foo@example.com',
	...         'cc_myself': True}
	>>> f = ContactForm(data, initial=data)
	>>> f.has_changed()
	False
	```
	
- form이 제출되면 이를 재구성하고 비교가 가능하도록 원본 데이터를 제공합니다.

	```
	>>> f = ContactForm(request.POST, initial=data)
	>>> f.has_changed()
	```
	
- request.POST의 데이터가 initial에서 제공 한 것과 다르거나 그렇지 않으면 `has_changed()`가 True가됩니다. 결과는 폼의 각 필드에 대해 `Field.has_changed()`를 호출하여 계산됩니다.

**Form.changed_data**

- changed_data 속성은 폼의 바운드 데이터 (대개 request.POST)의 값이 initial에서 제공된 것과 다른 필드 이름 목록을 반환합니다. 데이터가 다르지 않으면 빈 목록을 반환합니다.

	```
	>>> f = ContactForm(request.POST, initial=data)
	>>> if f.has_changed():
	...     print("The following fields changed: %s" % ", ".join(f.changed_data))
	```
	
<br>

-

*__Accessing the fields from the form__*

**Form.fields**

- fields 속성에서 Form 인스턴스의 필드에 액세스 할 수 있습니다.

	```
	>>> for row in f.fields.values(): print(row)
	...
	<django.forms.fields.CharField object at 0x7ffaac632510>
	<django.forms.fields.URLField object at 0x7ffaac632f90>
	<django.forms.fields.CharField object at 0x7ffaac3aa050>
	>>> f.fields['name']
	<django.forms.fields.CharField object at 0x7ffaac6324d0>
	```
	
	> for loop를 통해 조회한 필드와 주소가 다르다.
	
- form 인스턴스의 양식을 변경하여 양식에 표시되는 방식을 변경할 수 있습니다.

	```
	>>> f.as_table().split('\n')[0]
	'<tr><th>Name:</th><td><input name="name" type="text" value="instance" required /></td></tr>'
	>>> f.fields['name'].label = "Username"
	>>> f.as_table().split('\n')[0]
	'<tr><th>Username:</th><td><input name="name" type="text" value="instance" required /></td></tr>'
	```
	
	> `<th>Name:<th>` 에서 `<th>Username:<th>` 으로
	
- 이 수정은 동일한 Python 프로세스 내의 모든 후속 ContactForm 인스턴스에 영향을 미치기 때문에 base_fields 특성을 변경하지 않도록 주의하십시오.

	```
	>>> f.base_fields['name'].label = "Username"
	>>> another_f = CommentForm(auto_id=False)
	>>> another_f.as_table().split('\n')[0]
	'<tr><th>Username:</th><td><input name="name" type="text" value="class" required /></td></tr>'
	```
	
<br>

-

*__Accessing “clean” data__*

**Form.cleaned_data**

- Form 클래스의 각 필드는 데이터의 유효성을 검사 할뿐만 아니라 **일관된 형식으로 정규화하는 "정리(cleaning)"작업도 담당**합니다. 특정 필드의 데이터를 다양한 방법으로 입력 할 수 있으므로 항상 일관된 결과를 얻을 수 있기 때문에 좋은 기능입니다.

- 예를 들어 DateField는 입력을 Python datetime.date 객체로 정규화합니다. 여부에 관계없이 '1994-07-15'형식의 문자열, datetime.date 개체 또는 기타 여러 형식을 전달하더라도 DateField는 항상 유효 기간 동안 datetime.date 개체로 정규화합니다.

- 일단 데이터 세트로 Form 인스턴스를 생성하고 유효성을 검사하면 cleaned_data 속성을 통해 깨끗한 데이터에 액세스 할 수 있습니다.

	```
	>>> data = {'subject': 'hello',
	...         'message': 'Hi there',
	...         'sender': 'foo@example.com',
	...         'cc_myself': True}
	>>> f = ContactForm(data)
	>>> f.is_valid()
	True
	>>> f.cleaned_data
	{'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
	```
	
- CharField 또는 EmailField와 같은 텍스트 기반 필드는 항상 입력을 **유니 코드 문자열로 정리**합니다. 이 문서 뒷부분의 인코딩 의미에 대해 설명합니다.

- 데이터가 유효하지 않은 경우, cleaned_data 사전에는 유효한 필드만 포함됩니다.

	```
	>>> data = {'subject': '',
	...         'message': 'Hi there',
	...         'sender': 'invalid email address',
	...         'cc_myself': True}
	>>> f = ContactForm(data)
	>>> f.is_valid()
	False
	>>> f.cleaned_data
	{'cc_myself': True, 'message': 'Hi there'}
	```
	
- **cleaned_data는 양식을 정의할 때 추가 데이터를 전달하는 경우에도 양식에 정의 된 필드의 키만 항상 포함합니다.** 이 예제에서는 ContactForm 생성자에 여러 개의 추가 필드를 전달하지만 cleaned_data에는 양식의 필드만 포함되어 있습니다.

	```
	>>> data = {'subject': 'hello',
	...         'message': 'Hi there',
	...         'sender': 'foo@example.com',
	...         'cc_myself': True,
	...         'extra_field_1': 'foo',
	...         'extra_field_2': 'bar',
	...         'extra_field_3': 'baz'}
	>>> f = ContactForm(data)
	>>> f.is_valid()
	True
	>>> f.cleaned_data # Doesn't contain extra_field_1, etc.
	{'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
	```
	
- form이 유효하면 일부 선택적 필드의 값이 데이터에 포함되지 않은 경우에도 `cleaned_data`는 해당 필드의 키와 값을 포함합니다. 이 예에서 데이터 딕셔너리는 `nick_name` 필드의 값을 포함하지 않지만 cleaned_data에는 빈 값이 포함되어 있습니다.

	```
	>>> from django import forms
	>>> class OptionalPersonForm(forms.Form):
	...     first_name = forms.CharField()
	...     last_name = forms.CharField()
	...     nick_name = forms.CharField(required=False)
	>>> data = {'first_name': 'John', 'last_name': 'Lennon'}
	>>> f = OptionalPersonForm(data)
	>>> f.is_valid()
	True
	>>> f.cleaned_data
	{'nick_name': '', 'first_name': 'John', 'last_name': 'Lennon'}
	```
	
- 위의 예에서 `nick_name`에 대한 `cleaned_data` 값은 빈 문자열로 설정됩니다. `nick_name`은 CharField이고 CharFields는 빈 값을 빈 문자열로 처리하기 때문입니다. **각 필드 유형은 "빈 값(blank)"이 무엇인지 알고 있습니다.** 예를 들어 DateField의 경우 빈 문자열 대신 None입니다. 이 경우 각 필드의 동작에 대한 자세한 내용은 아래의 "내장 필드 클래스"섹션의 각 필드에 대한 "빈 값(Empty value)"참고를 참조하십시오.

- 특정 양식 필드 (이름을 기반으로 함) 또는 전체 양식 (다양한 필드의 조합을 고려)에 대해 유효성 검사를 수행하는 코드를 작성할 수 있습니다. 자세한 내용은 [Form and field validation]를 참조하십시오.


[Form and field validation]: https://docs.djangoproject.com/en/1.11/ref/forms/validation/

<br>

-

*__Outputting forms as HTML__*

- **Form 객체의 두 번째 작업은 자신을 HTML로 렌더링하는 것입니다.** 그렇게하려면 print 만하면됩니다.

	> form 클래스의 각 필드는 데이터 유효성을 검사할 뿐만 아니라 일관된 형식으로 정리(cleaning)하고, 자신을 HTML로 렌더링 한다.
	
	```
	>>> f = ContactForm()
	>>> print(f)
	<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" required /></td></tr>
	<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" required /></td></tr>
	<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" required /></td></tr>
	<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" /></td></tr>
	```
	
- 양식이 데이터에 바인딩되어 있으면 HTML 출력에 해당 데이터가 적절하게 포함됩니다. 예를 들어 필드가 `<input type = "text">`로 표시되면 데이터는 value속성에 있습니다. 필드가 `<input type = "checkbox">`에 의해 표현되는 경우 해당 HTML은 적절한 경우 선택됩니다.

	```
	>>> data = {'subject': 'hello',
	...         'message': 'Hi there',
	...         'sender': 'foo@example.com',
	...         'cc_myself': True}
	>>> f = ContactForm(data)
	>>> print(f)
	<tr><th><label for="id_subject">Subject:</label></th><td><input id="id_subject" type="text" name="subject" maxlength="100" value="hello" required /></td></tr>
	<tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" value="Hi there" required /></td></tr>
	<tr><th><label for="id_sender">Sender:</label></th><td><input type="email" name="sender" id="id_sender" value="foo@example.com" required /></td></tr>
	<tr><th><label for="id_cc_myself">Cc myself:</label></th><td><input type="checkbox" name="cc_myself" id="id_cc_myself" checked /></td></tr>
	```
- **Changed in Django 1.11**

	- checked 속성이 checked = "checked"가 아닌 HTML5 boolean 구문을 사용하도록 변경되었습니다.

- 이 기본 출력은 각 필드에 `<tr>`이있는 두 개의 열 HTML 표입니다. 다음 사항에 유의하십시오.

	- 유연성을 위해 출력에는 `<table>` 및 `</table>` 태그가 포함되지 않으며 `<form>` 및 `</form>` 태그 또는 `<input type = "submit">` 태그도 포함되지 않습니다. 그렇게하는 것은 당신의 몫입니다.

	- 각 필드 유형에는 기본 HTML 표현이 있습니다. CharField는 `<input type = "text">` 및 EmailField로 `<input type = "email">`으로 표시됩니다. BooleanField는 `<input type = "checkbox">`로 표현됩니다. 이들은 단지 합리적인 기본값 일뿐입니다. **위젯을 사용하여 주어진 필드에 사용할 HTML을 지정할 수 있습니다.** 곧 설명 드리겠습니다.

	- 각 태그의 HTML 이름은 ContactForm 클래스의 속성 이름에서 직접 가져옵니다.

	- 각 입력란의 텍스트 라벨 (예 : 'Subject :', 'Message :'및 'Cc myself :'은 **필드 이름에서 밑줄을 모두 공백으로 변환하고 첫 글자를 대문자로 변환하여 생성됩니다.** 다시 말하지만, 이것들은 단지 합리적인 기본값 일뿐입니다. **라벨을 수동으로 지정할 수도 있습니다.**

	- 각 텍스트 레이블은 id를 통해 적절한 양식 필드를 가리키는 HTML `<label>` 태그로 둘러 쌓여 있습니다. **id는 필드 이름 앞에 `'id_'`를 붙임으로써 생성된다.** id 속성과 `<label>` 태그는 모범 사례를 따르기 위해 기본적으로 출력에 포함되지만 그 동작을 변경할 수 있습니다.

	- 출력 결과는 `<!DOCTYPE html>`을 대상으로하는 HTML5 구문을 사용합니다. 예를 들어, `checked = 'checked'`의 XHTML 스타일 대신 checked 속성과 같은 boolean 속성을 사용합니다.

- 양식을 인쇄 할 때 `<table>` 출력이 기본 출력 스타일이지만 다른 출력 스타일을 사용할 수 있습니다. 각 스타일은 양식 객체의 메서드로 사용할 수 있으며 각 렌더링 메서드는 유니 코드 객체를 반환합니다.

<br>

-

❗️❗️❗️나머지 부분은 차후에... 아직 중요한거 아니야 😤❗️❗️❗️

- form을...
	-  `<p>`태그로 렌더링 하는 `as_p()`
	-  `<li>`태그로 렌더링 하는 `as_ul()`(`<ul></ul>`은 포함하지 않음)
	-  `<table>`형식으로 렌더링 하는 `as_table()`(그냥 폼 객체를 출력하면 `as_table()`을 호출한다고 함)

- id속성 과 연관된 `auto_id=False`, `auto_id=True` 외 `auto_id='id_for_%s'`

- `label_suffix` 설정

- error 관련 내용

- BoundField 관련 내용 (Attribute, methods, customizing)

- `multipart/form-data`, form 연관 내용 등...