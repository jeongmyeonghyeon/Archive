### Working with forms

<br>

- About this document

	- 이 문서는 웹 폼의 기본 사항과 장고에서 다루는 방법을 소개합니다. form API의 특정 영역에 대한 자세한 내용은 [The Forms API], [Form fields] 및 [Form and field validation]을 참조하십시오.

- 콘텐츠를 게시하고 방문자의 의견을 수락하지 않는 웹 사이트 및 응용 프로그램을 만들 계획이 아니라면 form을 이해하고 사용해야 할 것입니다.

- Django는 사이트 방문자의 의견을 수락하고 입력을 처리하고 응답하는 form을 작성하는데 도움이되는 다양한 도구와 라이브러리를 제공합니다.


[The Forms API]: https://docs.djangoproject.com/en/1.11/ref/forms/api/

[Form fields]: https://docs.djangoproject.com/en/1.11/ref/forms/fields/

[Form and field validation]: https://docs.djangoproject.com/en/1.11/ref/forms/validation/

<br>

*__HTML forms__*

- HTML에서, 폼은 `<form> ... </ form>` 내에있는 방문자가 텍스트를 입력하고, 옵션을 선택하고, 객체 나 컨트롤을 조작하는 등의 작업을 수행 한 다음 해당 정보를 다시 서버로 보내는 엘리먼트들의 모음이다.

- 이러한 form 인터페이스 요소 중 일부 (텍스트 입력 또는 확인란)는 매우 간단하며 HTML 자체에 내장되어 있습니다. 다른 것들은 훨씬 더 복잡합니다. 날짜 선택 도구를 팝업하거나 슬라이더를 이동하거나 컨트롤을 조작 할 수있는 인터페이스는 일반적으로 JavaScript 및 CSS뿐만 아니라 HTML form `<input>` 요소를 사용하여 이러한 효과를 얻습니다.

- form은 `<input>` 요소뿐만 아니라 두 가지를 지정해야합니다.

	- where: 사용자의 입력에 해당하는 데이터가 반환되어야하는 URL

	- how: 데이터가 반환되어야하는 HTTP 메소드

- 예를 들어, Django 관리자의 로그인 폼에는 여러 개의 `<input>` 요소가 있습니다. 하나는 사용자 이름에 `type = "text"`, password에는 `type = "password"`, 다른 하나는 로그인 버튼인 `type = "submit"`입니다. 또한 사용자가 볼 수없는 몇 가지 숨겨진 텍스트 필드가 포함되어 있으며 장고는 다음에 수행할 작업을 결정하는 데 사용합니다.

- 또한 폼 데이터가 `<form>`의 action 속성 - / admin / -에 지정된 URL로 보내져야하며 메서드 속성 -post에 지정된 HTTP 메커니즘을 사용하여 보내야한다고 브라우저에 알립니다.

- `<input type = "submit"value = "Log in">` 요소가 트리거되면 데이터는 / admin /로 리턴됩니다.

<br>

*__GET and POST__*

- GET과 POST는 폼을 다룰 때 사용할 수 있는 **유일한 HTTP 메소드**입니다.

- Django의 로그인 폼은 POST 메서드를 사용하여 반환됩니다. POST 메서드는 브라우저가 form 데이터를 묶어서 전송 인코딩하고 서버로 보낸 다음 응답을 수신합니다.

- 반대로 GET은 제출 된 데이터를 문자열로 묶어 URL을 작성하는 데 사용합니다. URL에는 데이터를 전송해야하는 주소는 물론 데이터 키와 값이 포함됩니다. Django 문서에서 검색을하면 `https://docs.djangoproject.com/search/?q=forms&release=1` 형식의 URL이 생성됩니다.

- GET 및 POST는 일반적으로 다른 용도로 사용됩니다.

- **시스템의 상태를 변경하는 데 사용할 수있는 요청** (예 : 데이터베이스 변경 요청)은 POST를 사용해야합니다. GET은 시스템 상태에 영향을주지 않는 요청에만 사용해야합니다.

- GET은 또한 암호 형식에 적합하지 않습니다. 암호가 URL에 표시되고 브라우저 기록 및 서버 로그에도 모두 일반 텍스트로 표시되기 때문입니다. 또한 대량의 데이터 또는 또는 이미지와 같은 2 진 데이터의 경우 적합하지 않습니다. 관리 form에 GET 요청을 사용하는 웹 응용 프로그램은 보안 위험이 있습니다. 공격자가 시스템의 민감한 부분에 액세스하기위한 form의 요청을 모방하는 것이 쉽습니다. POST는 Django의 [CSRF protection]와 같은 다른 보호 기능과 결합되어 액세스를보다 효율적으로 제어합니다.

- 반면 GET 요청을 나타내는 URL은 쉽게 책갈피, 공유 또는 다시 제출할 수 있기 때문에 GET은 웹 검색 form과 같은 것에 적합합니다.


[CSRF protection]: https://docs.djangoproject.com/en/1.11/ref/csrf/

<br>

-

*__Django’s role in forms__*

- form 처리는 복잡한 비지니스입니다. Django의 관리자를 생각해보십시오. 다양한 유형의 여러 데이터 항목을 form으로 표시하기 위해 준비하고, HTML로 렌더링하고, 편리한 인터페이스를 사용하여 편집하고, 서버에 반환하고, 유효성을 검사하고 정리 한 다음 추가 처리를 위해 저장하거나 전달해야 할 수 있습니다.

- Django의 폼 기능은 이 작업의 상당 부분을 단순화하고 자동화 할 수 있으며, 대부분의 프로그래머가 작성한 코드에서 수행 할 수있는 것보다 더 안전하게 수행 할 수 있습니다.

- **Django는 폼과 관련된 세 가지 부분을 처리**합니다.

	- 데이터 준비 및 재구성하여 렌더링 준비
	- 데이터 용 HTML form 작성
	- 제출 된 form 및 데이터 수신 및 처리

- 이 모든 작업을 수동으로 수행하는 코드를 작성하는 것은 가능하지만 장고는이를 모두 처리 할 수 ​​있습니다.

<br>

-

*__Forms in Django__*

- 우리는 HTML 폼을 간단히 설명했지만 HTML `<form>`은 필요한 시스템의 일부일뿐입니다.

- 웹 애플리케이션의 맥락에서 'form'은 HTML <form>을 참조하거나 그것을 생성하는 [Django Form]을 참조 할 수 있습니다. 또는 제출 될 때 반환된 구조화 된 데이터나 이러한 파트의 종단 간 작업 모음에 적용됩니다.

<br>

*__The Django [Form][Django Form] class__*

- 이 컴포넌트 시스템의 핵심은 Django의 [Form][Django Form] 클래스입니다. **Django 모델이 객체의 논리적 구조, 동작 및 파트가 우리에게 표시되는 방식을 설명하는 것과 거의 같은 방식**으로 [Form][Django Form] 클래스는 form을 설명하고 form이 작동하고 나타나는 방식을 결정합니다.

- 모델 클래스의 필드가 데이터베이스 필드에 매핑되는 것과 비슷한 방식으로 폼 클래스의 필드는 HTML 폼 `<input>` 요소에 매핑됩니다. ([ModelForm]은 [Form][Django Form]을 통해 모델 클래스의 필드를 HTML 폼의 `<input>` 요소로 매핑합니다; 이것이 장고 관리자의 기반입니다.)

- Form의 필드 자체는 클래스입니다. **Form이 제출 될 때 form 데이터를 관리하고 유효성 검사를 수행합니다.** [DateField]와 [FileField]는 매우 다른 종류의 데이터를 처리하며 서로 다른 작업을 수행해야합니다.

- form 필드는 브라우저의 사용자에게 HTML "위젯"(사용자 인터페이스 machinery)으로 표현됩니다. 각 필드 유형에는 적절한 기본 [위젯 클래스][Widget class]가 있지만 필요에 따라 재정의 할 수 있습니다.


[Django Form]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form

[ModelForm]: https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#django.forms.ModelForm

[DateField]: https://docs.djangoproject.com/en/1.11/ref/forms/fields/#django.forms.DateField

[FileField]: https://docs.djangoproject.com/en/1.11/ref/forms/fields/#django.forms.FileField

[Widget class]: https://docs.djangoproject.com/en/1.11/ref/forms/widgets/

<br>

-

*__Instantiating, processing, and rendering forms__*

- Django에서 객체를 렌더링 할 때 우리는 일반적으로 다음을 수행합니다.

	1. view에서 그것을 get hold.(데이터베이스에서 가져옵니다. 예를 들면 다음과 같습니다.)
	2. 템플릿 컨텍스트에 전달하십시오.
	3. 템플릿 변수를 사용하여 HTML 마크 업으로 확장하십시오.

- 템플릿의 폼 렌더링은 다른 종류의 오브젝트를 렌더링하는 것과 거의 동일한 작업을 포함하지만 몇 가지 주요 차이점이 있습니다.

- 데이터가없는 모델 인스턴스의 경우, 템플릿으로 템플릿을 사용하여 아무 것도하지 않는 것이 거의 불가능합니다. 반면에, 그것은 사용자가 채워 넣기를 원할 때 우리가하는 것입니다.

- 따라서 뷰에서 모델 인스턴스를 처리 할 때 일반적으로 데이터베이스에서 모델 인스턴스를 검색합니다. form을 처리 할 때 일반적으로 view에서 인스턴스를 인스턴스화합니다.

- form을 인스턴스화 할 때 form을 비워 두거나 미리 채울 수 있습니다. 예를 들면 다음과 같습니다.

	- 저장된 모델 인스턴스의 데이터(편집을위한 관리 form의 경우와 같이)
	- 다른 출처에서 수집 한 데이터
	- 이전 HTML form submit에서 form받은 데이터

- 마지막으로 이러한 경우가 가장 흥미로운 이유는 사용자가 웹 사이트를 읽는 것이 아니라 정보를 다시 보낼 수있게하기 때문입니다.

<br>

-

*__Building a form__*

*__The work that needs to be done__*

- 사용자 이름을 얻기 위해 웹 사이트에서 간단한 form을 만들고 싶다고 가정 해보십시오. 템플릿에 다음과 같은 내용이 필요합니다.

	```
	<form action="/your-name/" method="post">
	    <label for="your_name">Your name: </label>
	    <input id="your_name" type="text" name="your_name" value="{{ current_name }}">
	    <input type="submit" value="OK">
	</form>
	```
	
- POST 메서드를 사용하여 폼 데이터를 URL / your-name /로 반환하도록 브라우저에 지시합니다. "Your name :"이라는 텍스트 필드와 "OK"라고 표시된 버튼이 표시됩니다. 템플릿 컨텍스트에 current_name 변수가 있으면 your_name 필드를 미리 채우는 데 사용됩니다.

- HTML form을 포함하는 템플리트를 렌더링하고 current_name 필드를 적절히 제공 할 수있는 뷰가 필요합니다.

- form이 제출되면 서버로 전송 된 POST 요청에는 form 데이터가 포함됩니다.

- 이제 해당 / your-name / URL에 해당하는보기가 필요합니다. 그러면 해당 요청에서 적절한 키 / 값 쌍을 찾아서 처리 할 수 ​​있습니다.

- 이것은 매우 간단한 형태입니다. 실제로 form에는 수십 또는 수백 개의 필드가 포함될 수 있으며 대부분 필드가 미리 채워 져야 할 수도 있습니다. 사용자는 작업을 완료하기 전에 편집 - 제출주기를 여러 번 검토해야 할 것입니다.

- form을 제출하기 전에도 브라우저에서 일부 유효성 검사를 수행해야 할 수도 있습니다. 우리는 훨씬 복잡한 필드를 사용하여 사용자가 달력에서 날짜를 선택하는 등의 작업을 수행 할 수 있습니다.

- 이 시점에서 Django가 우리를 위해 대부분의 작업을 수행하는 것이 훨씬 쉽습니다.

<br>

-

*__Building a form in Django__*

*__The Form class__*

- **우리는 HTML form이 어떻게 보이길 원하는지 이미 알고 있습니다.** 장고에서 우리의 출발점은 이것입니다 :

	```
	from django import forms

	class NameForm(forms.Form):
	    your_name = forms.CharField(label='Your name', max_length=100)
	```
	
- 이것은 단일 필드 (your_name)로 Form 클래스를 정의합니다. 인간 친화적 인 레이블을 필드에 적용했습니다.이 레이블은 레이블이 렌더링 될 때 `<label>`에 나타납니다 (이 경우 지정된 레이블은 실제로 레이블을 생략 한 경우 자동으로 생성되는 레이블과 동일합니다).

- 필드의 최대 허용 길이는 max_length에 의해 정의됩니다. 이것은 두 가지 일을합니다. HTML `<input>`에 `maxlength = "100"`을 넣습니다 (브라우저가 사용자가 처음에 그 수보다 많은 문자를 입력하지 못하게해야합니다). **또한 Django가 브라우저에서 form을 다시 받으면 데이터 길이를 확인합니다.**

- Form 인스턴스에는 모든 필드에 대한 유효성 검사 루틴을 실행하는 [`is_valid()`][is_valid] 메서드가 있습니다. 이 메서드가 호출되면 모든 필드에 유효한 데이터가 포함되어 있으면 다음을 수행합니다.

	- return True
	- 폼의 데이터를 [cleaned_data] 속성에 저장하십시오.

- 전체 form은 처음 렌더링 될 때 다음과 같이 표시됩니다.

	```
	<label for="your_name">Your name: </label>
	<input id="your_name" type="text" name="your_name" maxlength="100" required />
	```
	
- 여기에는 `<form>` 태그 또는 제출 버튼이 포함되지 않습니다. 우리는 템플릿에 자신을 제공해야합니다.


[is_valid]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form.is_valid

[cleaned_data]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form.cleaned_data

<br>

-

*__The view__*

- Django 웹 사이트로 보내진 form 데이터는 일반적으로 **form을 게시한 view와 ​​같은 view로 처리**됩니다. 이것은 우리가 동일한 논리의 일부를 **재사용** 할 수있게 해줍니다.

	```
	from django.shortcuts import render
	from django.http import HttpResponseRedirect
	
	from .forms import NameForm
	
	def get_name(request):
	    # if this is a POST request we need to process the form data
	    if request.method == 'POST':
	        # create a form instance and populate it with data from the request:
	        form = NameForm(request.POST)
	        # check whether it's valid:
	        if form.is_valid():
	            # process the data in form.cleaned_data as required
	            # ...
	            # redirect to a new URL:
	            return HttpResponseRedirect('/thanks/')
	
	    # if a GET (or any other method) we'll create a blank form
	    else:
	        form = NameForm()
	
	    return render(request, 'name.html', {'form': form})
	```

- POST 요청을 사용하여 form을 제출하면 view에서 form 인스턴스를 다시 작성하고 요청의 데이터로 채웁니다. form = NameForm(request.POST) "form에 데이터 바인딩"이라고합니다 (이제는 바운드 형식).

- 우리는 폼의 `is_valid()` 메소드를 호출한다. True가 아니라면 form이있는 템플릿으로 돌아갑니다. 이번에는 form이 더 이상 비어 있지 않으므로 HTML form은 이전에 제출 된 데이터로 채워지며 필요에 따라 편집 및 수정할 수 있습니다.

- `is_valid()`가 True이면 이제 `cleaned_data` 속성에서 모든 유효성이 검사된 form 데이터를 찾을 수 있습니다. 이 데이터를 사용하여 데이터베이스를 업데이트하거나 브라우저로 HTTP 리디렉션을 보내기 전에 다른 처리를 수행하여 다음에 어디로 가야하는지 알려줍니다.

<br>

-

*__The template__*

- 우리는 `name.html` 템플릿에서 많은 작업을 수행 할 필요가 없습니다. 가장 간단한 예는 다음과 같습니다.

	```
	<form action="/your-name/" method="post">
	    {% csrf_token %}
	    {{ form }}
	    <input type="submit" value="Submit" />
	</form>
	```
	
- 모든 폼의 필드와 속성은 **장고의 템플릿 언어에 의해** {{form}}의 HTML 마크 업으로 풀립니다.

	> **_Forms and Cross Site Request Forgery protection_**
	
	> Django는 Cross Site Request Forgeies에 대한 사용하기 쉬운 보호 기능을 제공합니다. CSRF 보호가 활성화 된 상태에서 POST를 통해 form을 제출할 때 앞의 예와 같이 csrf_token 템플리트 태그를 사용해야합니다. 그러나 CSRF 보호는 템플릿의 form에 직접 연결되어 있지 않으므로이 태그는이 문서의 다음 예제에서 생략되었습니다.
	
	> **_HTML5 input types and browser validation_**
	
	> form에 URLField, EmailField 또는 정수 필드 유형이 포함 된 경우 Django는 URL, 이메일 및 숫자 HTML5 입력 유형을 사용합니다. 기본적으로 브라우저는 이 필드에 대해 자체 유효성 검사를 적용 할 수 있습니다. 이는 장고의 유효성 검사보다 엄격 할 수 있습니다. 이 동작을 사용하지 않으려면 form 태그에 novalidate 속성을 설정하거나 TextInput과 같이 필드에 다른 위젯을 지정하십시오.

- 우리는 이제 Django Form에 의해 설명되고 보기에 의해 처리되고 HTML <form>으로 렌더링되는 작업 웹 form을 갖습니다.

- 그만하면 시작할 수 있지만 폼 프레임 워크는 훨씬 더 손쉽게 사용할 수 있습니다. 위에 설명 된 프로세스의 기본 사항을 이해하면 form 시스템의 다른 기능을 이해하고 기본 시스템에 대해 더 배울 준비를해야합니다.

<br>

-

*__More about Django Form classes__*

- 모든 폼 클래스는 Django의 admin에서 발생하는 [ModelForm]을 포함하여 [django.forms.Form]의 서브 클래스로 생성됩니다.

- **Models and Forms**

	- 사실 Django 모델을 직접 추가하거나 편집하기 위해 form을 사용한다면 [ModelForm]은 적절한 필드와 속성과 함께 form을 작성하기 때문에 많은 시간과 노력 및 코드를 절약 할 수 있습니다 Model 클래스에서 가져옵니다.


[django.forms.Form]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form

- *__Bound and unbound form instances__*

- [Bound and unbound forms]의 차이점은 중요합니다.

	- 언 바운드 형식에는 연결된 데이터가 없습니다. 사용자에게 표시되면 **비어 있거나 기본값을 포함합니다.**
	- 바운드 폼이 데이터를 제출 했으므로 해당 데이터가 유효한지 여부를 알리는 데 사용할 수 있습니다. 잘못된 바운드 form이 렌더링되면 인라인 오류 메시지를 포함하여 사용자에게 수정해야 할 데이터를 알려줍니다.

- form의 [`is_bound`] 속성은 form에 데이터가 바인드되어 있는지 여부를 알려줍니다.



[Bound and unbound forms]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#bound-and-unbound-forms

[`is_bound`]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.Form.is_bound

<br>

-

*__More on fields__*

- 개인 웹 사이트에 "contanc me"기능을 구현하는 데 사용할 수 있는 위의 최소 예제보다 유용한 form을 고려하십시오.

	```
	from django import forms
	
	class ContactForm(forms.Form):
	    subject = forms.CharField(max_length=100)
	    message = forms.CharField(widget=forms.Textarea)
	    sender = forms.EmailField()
	    cc_myself = forms.BooleanField(required=False)
	```
	
- 우리의 이전 form은 하나의 필드 인 `your_name`, `CharField`를 사용했습니다. 이 경우 form에는 제목, 메시지, 보낸 사람 및 `cc_myself`의 네 가지 필드가 있습니다. `CharField`, `EmailField` 및 `BooleanField`는 사용 가능한 필드 유형 중 세 가지입니다. 전체 목록은 [Form fields]에서 찾을 수 있습니다.


*__Widgets__*

- 각 form 필드에는 해당 [Widget] 클래스가 있으며,이 클래스는 `<input type = "text">`와 같은 HTML form 위젯에 해당합니다.

[Widget]: https://docs.djangoproject.com/en/1.11/ref/forms/widgets/

- 대부분의 경우이 필드에는 유용한 **기본 위젯**이 있습니다. 예를 들어 기본적으로 `CharField`에는 HTML에서 `<input type = "text">`을 생성하는 `TextInput` 위젯이 있습니다. 대신 `<textarea>`가 필요하다면, 우리는 메시지 필드에서했던 것처럼 form 필드를 정의 할 때 적절한 위젯을 지정해야합니다.

<br>

-

*__Field data__*

- form과 함께 제출 된 데이터가 무엇이든간에 `is_valid()`를 호출하여 유효성을 검사하고 `is_valid()`가 True를 반환하면 유효성이 검사 된 form 데이터는 `form.cleaned_data` dictionary에 저장됩니다. 이 데이터는 당신을 위해 파이썬 유형으로 멋지게 변환되었을 것입니다.

- **Note**

	- 이 시점에서 `request.POST`에서 유효성 검사를 거치지 않은 데이터에 **직접 액세스 할 수는 있지만 검증된 데이터가 더 좋습니다.**

- 위 연락처 form 예제에서 `cc_myself`는 bool 값이됩니다. 마찬가지로 `IntegerField` 및 `FloatField`와 같은 필드는 값을 각각 Python int 및 Float로 변환합니다.

- 이 form을 처리하는 view에서 form 데이터를 처리하는 방법은 다음과 같습니다.

	```
	from django.core.mail import send_mail

	if form.is_valid():
	    subject = form.cleaned_data['subject']
	    message = form.cleaned_data['message']
	    sender = form.cleaned_data['sender']
	    cc_myself = form.cleaned_data['cc_myself']
	
	    recipients = ['info@example.com']
	    if cc_myself:
	        recipients.append(sender)
	
	    send_mail(subject, message, sender, recipients)
	    return HttpResponseRedirect('/thanks/')
	```
	
- **Tip**

	- Django에서 이메일을 보내는 방법에 대한 자세한 내용은 [Sending email]를 참조하십시오.

[Sending email]: https://docs.djangoproject.com/en/1.11/topics/email/

- 일부 필드 유형은 추가 처리가 필요합니다. 예를 들어, **form을 사용하여 업로드 된 파일은 다르게 처리해야합니다 (request.POST보다는 request.FILES에서 검색 할 수 있습니다).** form으로 파일 업로드를 처리하는 방법에 대한 자세한 내용은 [Binding uploaded files to a form]을 참조하십시오.


[Binding uploaded files to a form]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#binding-uploaded-files

<br>

-

*__Working with form templates__*

- form을 템플릿으로 가져 오려면 form 인스턴스를 템플릿 컨텍스트에 배치하기 만하면됩니다. 따라서 form이 컨텍스트에서 form이라고 불리면 {{form}}은 **`<label>` 및 `<input>` 요소를 적절하게 렌더링**합니다

*__Form rendering options__*

- **Additional form template furniture**

	- form의 출력에 주변 **`<form>` 태그** 또는 **양식의 submit control**이 **포함되지 않는다는 사실**을 잊지 마십시오. 직접 제공해야 합니다.

- `<label>` / `<input>` 쌍에 대해서는 다른 출력 옵션이 있습니다.

	- {{form.as_table}}은 표 셀을 `<tr>` 태그로 싸서 표 셀로 렌더링합니다.
	- {{form.as_p}}는 그것들을 <p> 태그로 감싸줍니다.
	- {{form.as_ul}}은 그것들을 <li> 태그로 감싸줍니다.

- **주위의 `<table>` 또는 `<ul>` 요소를 직접 제공해야합니다.**

- ContactForm 인스턴스의 {{form.as_p}} 결과는 다음과 같습니다.

	```
	<p><label for="id_subject">Subject:</label>
	    <input id="id_subject" type="text" name="subject" maxlength="100" required /></p>
	<p><label for="id_message">Message:</label>
	    <textarea name="message" id="id_message" required></textarea></p>
	<p><label for="id_sender">Sender:</label>
	    <input type="email" name="sender" id="id_sender" required /></p>
	<p><label for="id_cc_myself">Cc myself:</label>
	    <input type="checkbox" name="cc_myself" id="id_cc_myself" /></p>
    ```

- 각 양식 필드에는 `id_<field-name>`으로 설정된 ID 속성이 있습니다.이 속성은 함께 제공되는 label 태그에 의해 참조됩니다. 양식이 화면 판독기 소프트웨어와 같은 보조 기술에 액세스 할 수 있도록하는 데 중요합니다. [레이블과 ID가 생성되는 방식을 사용자 정의][customize the way in which labels and ids are generated] 할 수도 있습니다.

- 자세한 내용은 [Outputting forms as HTML]을 참조하십시오.


[customize the way in which labels and ids are generated]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#ref-forms-api-configuring-label

[Outputting forms as HTML]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#ref-forms-api-outputting-html

<br>

-

*__Rendering fields manually__*

- 우리는 장고가 form 필드를 풀도록(unpack) 할 필요가 없습니다. 우리가 원한다면 수동으로 처리 할 수 ​​있습니다 (예를 들어, 필드를 재정렬 할 수있게 해줍니다). 각 필드는 `{{form.name_of_field}}` 및 장고 템플릿을 사용하여 적절히 표현되게끔 양식의 속성으로 사용할 수 있습니다. 예:

	```
	{{ form.non_field_errors }}
	<div class="fieldWrapper">
	    {{ form.subject.errors }}
	    <label for="{{ form.subject.id_for_label }}">Email subject:</label>
	    {{ form.subject }}
	</div>
	<div class="fieldWrapper">
	    {{ form.message.errors }}
	    <label for="{{ form.message.id_for_label }}">Your message:</label>
	    {{ form.message }}
	</div>
	<div class="fieldWrapper">
	    {{ form.sender.errors }}
	    <label for="{{ form.sender.id_for_label }}">Your email address:</label>
	    {{ form.sender }}
	</div>
	<div class="fieldWrapper">
	    {{ form.cc_myself.errors }}
	    <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
	    {{ form.cc_myself }}
	</div>
	```
	
- 완전한 `<label>` 요소는 `label_tag()`를 사용하여 생성 할 수도 있습니다. 예 :

	```
	<div class="fieldWrapper">
	    {{ form.subject.errors }}
	    {{ form.subject.label_tag }}
	    {{ form.subject }}
	</div>
	```
	
*__Rendering form error messages__*

- 물론, 이 유연성의 가치는 더 많습니다. 지금까지 우리는 form 오류를 표시하는 방법에 대해 걱정할 필요가 없었습니다. 왜냐하면 이것이 양식 오류를 처리했기 때문입니다. 이 예제에서 우리는 각 필드의 모든 오류와 양식 전체의 오류를 처리해야합니다. 양식의 맨 위에있는 `{{form.non_field_errors}}` 및 각 필드의 오류에 대한 템플릿 조회를 참고하십시오.

- `{{form.name_of_field.errors}}`를 사용하면 양식 오류 목록이 표시되고 순서가 지정되지 않은 목록으로 표시됩니다. 이것은 다음과 같이 보일 것이다.

	```
	<ul class="errorlist">
	    <li>Sender is required.</li>
	</ul>
	```
	
- 이 목록에는 오류 목록의 CSS 클래스가있어 모양을 스타일 지정할 수 있습니다. 오류 표시를 추가로 사용자 정의하려는 경우 반복하여 오류를 표시 할 수 있습니다.

	```
	{% if form.subject.errors %}
	    <ol>
	    {% for error in form.subject.errors %}
	        <li><strong>{{ error|escape }}</strong></li>
	    {% endfor %}
	    </ol>
	{% endif %}
	```
	
- 필드가 아닌 오류 (`form.as_p()`와 같은 헬퍼를 사용할 때 양식 맨 위에 렌더링되는 숨겨진 필드 오류 및 / 또는 숨김 필드 오류) 필드 별 오류와 구별 할 수 있도록 추가 필드 클래스로 렌더링됩니다. 예를 들어, `{{form.non_field_errors}}`는 다음과 같습니다.

	```
	<ul class="errorlist nonfield">
	    <li>Generic validation error</li>
	</ul>
	```
	
- 오류, 스타일 및 템플릿의 양식 속성 사용에 대한 자세한 내용은 [The Forms API]를 참조하십시오.

<br>

-

*__Looping over the form’s fields__*

- 각 양식 필드에 대해 동일한 HTML을 사용하는 경우 `{% for %}` 루프를 사용하여 차례대로 각 필드를 반복하여 중복 코드를 줄일 수 있습니다.

	```
	{% for field in form %}
	    <div class="fieldWrapper">
	        {{ field.errors }}
	        {{ field.label_tag }} {{ field }}
	        {% if field.help_text %}
	        <p class="help">{{ field.help_text|safe }}</p>
	        {% endif %}
	    </div>
	{% endfor %}
	```
	
- `{{field}}`의 유용한 속성에는 다음이 포함됩니다.

- **`{{ field.label }}`**
	- 입력란의 라벨 (예 : 이메일 주소)

- **`{{ field.label_tag }}`**
	- 필드의 레이블이 적절한 `HTML <label>` 태그에 래핑됩니다. 여기에는 양식의 `label_suffix`가 포함됩니다. 예를 들어 기본 `label_suffix`는 `콜론(:)`입니다.

	```
	<label for="id_email">Email address:</label>
	```
	
- **`{{ field.id_for_label }}`**

	- 이 필드에 사용할 ID입니다 (위 예에서 `id_email`). 라벨을 수동으로 구성하는 경우 `label_tag` 대신이 라벨을 사용할 수 있습니다. 예를 들어 인라인 자바 스크립트가 있고 필드의 ID를 하드 코딩하지 않으려는 경우에도 유용합니다.

- **`{{ field.value }}`**

	- 필드의 값입니다. 예 : someone@example.com

- **`{{ field.html_name }}`**

	- 입력 요소의 이름 필드에 사용될 필드의 이름입니다. 양식 접두어가 설정되어 있으면 이를 계정으로 가져옵니다.

- **`{{ field.help_text }}`**

	- 필드와 관련된 도움말 텍스트.

- **`{{ field.errors }}`**

	- 이 필드에 해당하는 유효성 검사 오류가 포함 된 `<ul class = "errorlist">`를 출력합니다. `{% for error in field.errors %}` 루프로 오류 표시를 사용자 정의 할 수 있습니다. 이 경우 루프의 각 객체는 오류 메시지가 포함 된 간단한 문자열입니다.

- **`{{ field.is_hidden }}`**

	- 이 특성은 form 필드가 숨겨진 필드이면 True이고 그렇지 않으면 False입니다. 템플릿 변수로 특히 유용하지는 않지만 **다음과 같은 조건부 테스트에 유용 할 수 있습니다.**

		```
		{% if field.is_hidden %}
		   {# Do something special #}
		{% endif %}
		```

- **`{{ field.field }}`**

	- 이 [`BoundField`]가 래핑하는 form 클래스의 [Field][Form fields] 인스턴스입니다. **이 속성을 사용하여 필드 속성에 액세스 할 수 있습니다.** 예: `{{char_field.field.max_length}}`

- **See also**

	- 특성 및 메서드의 전체 목록은 [`BoundField`]를 참조하십시오.

	
[`BoundField`]: https://docs.djangoproject.com/en/1.11/ref/forms/api/#django.forms.BoundField

<br>

*__Looping over hidden and visible fields__*

- 장고의 기본 폼 레이아웃에 의존하지 않고 수동으로 템플릿에 폼을 배치하는 경우 `<input type = "hidden">` 필드를 숨겨진 필드와 다르게 처리해야 할 수 있습니다. 예를 들어, 숨겨진 필드는 아무 것도 표시하지 않기 때문에 오류 메시지를 필드 옆에 배치하면 사용자에게 혼동을 줄 수 있으므로 해당 필드의 오류를 다르게 처리해야합니다.

- Django는 `hidden_fields()` 및 `visible_fields()`와 같이 숨김 필드와 표시 필드를 독립적으로 반복 할 수있는 두 가지 메서드를 제공합니다. 다음은이 두 가지 방법을 사용하는 이전 예제를 수정 한 것입니다.

	```
	{# Include the hidden fields #}
	{% for hidden in form.hidden_fields %}
	{{ hidden }}
	{% endfor %}
	{# Include the visible fields #}
	{% for field in form.visible_fields %}
	    <div class="fieldWrapper">
	        {{ field.errors }}
	        {{ field.label_tag }} {{ field }}
	    </div>
	{% endfor %}
	```
	
- 이 예제는 숨겨진 필드의 오류를 처리하지 않습니다. 일반적으로, 숨겨진 필드의 오류는 일반적인 형태 상호 작용이 변경되지 않기 때문에 형식 변조의 징후이다. 그러나 이러한 형식 오류에 대한 일부 오류 표시도 쉽게 삽입할 수 있습니다.

<br>

-

*__Reusable form templates__*

- 사이트에서 여러 위치의 양식에 동일한 렌더링 논리를 사용하는 경우 양식의 루프를 독립형 템플릿에 저장하고 [include] 태그를 사용하여 다른 템플릿에서 다시 사용하여 중복을 줄일 수 있습니다.

	```
	# In your form template:
	{% include "form_snippet.html" %}
	
	# In form_snippet.html:
	{% for field in form %}
	    <div class="fieldWrapper">
	        {{ field.errors }}
	        {{ field.label_tag }} {{ field }}
	    </div>
	{% endfor %}
	```
	
- 템플리트에 전달 된 form 오브젝트가 **컨텍스트 내에서 다른 이름을 갖는 경우** [include]태그의 **with 인수**를 사용하여 별명(alias)을 지정할 수 있습니다.

	```
	{% include "form_snippet.html" with form=comment_form %}
	```
	
- 이 작업을 자주 수행하는 경우 [사용자 지정 포함 태그][inclusion tag]를 만드는 것이 좋습니다.


[include]: https://docs.djangoproject.com/en/1.11/ref/templates/builtins/#std:templatetag-include

[inclusion tag]: https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#howto-custom-template-tags-inclusion-tags