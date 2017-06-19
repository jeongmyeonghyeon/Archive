### Working with forms

<br>

- About this document

	- 이 문서는 웹 폼의 기본 사항과 장고에서 다루는 방법을 소개합니다. 양식 API의 특정 영역에 대한 자세한 내용은 [The Forms API], [Form fields] 및 [Form and field validation]을 참조하십시오.

- 콘텐츠를 게시하고 방문자의 의견을 수락하지 않는 웹 사이트 및 응용 프로그램을 만들 계획이 아니라면 양식을 이해하고 사용해야 할 것입니다.

- Django는 사이트 방문자의 의견을 수락하고 입력을 처리하고 응답하는 양식을 작성하는데 도움이되는 다양한 도구와 라이브러리를 제공합니다.


[The Forms API]: https://docs.djangoproject.com/en/1.11/ref/forms/api/

[Form fields]: https://docs.djangoproject.com/en/1.11/ref/forms/fields/

[Form and field validation]: https://docs.djangoproject.com/en/1.11/ref/forms/validation/

<br>

*__HTML forms__*

- HTML에서, 폼은 `<form> ... </ form>` 내에있는 방문자가 텍스트를 입력하고, 옵션을 선택하고, 객체 나 컨트롤을 조작하는 등의 작업을 수행 한 다음 해당 정보를 다시 서버로 보내는 엘리먼트들의 모음이다.

- 이러한 양식 인터페이스 요소 중 일부 (텍스트 입력 또는 확인란)는 매우 간단하며 HTML 자체에 내장되어 있습니다. 다른 것들은 훨씬 더 복잡합니다. 날짜 선택 도구를 팝업하거나 슬라이더를 이동하거나 컨트롤을 조작 할 수있는 인터페이스는 일반적으로 JavaScript 및 CSS뿐만 아니라 HTML 양식 `<input>` 요소를 사용하여 이러한 효과를 얻습니다.

- form은 `<input>` 요소뿐만 아니라 두 가지를 지정해야합니다.

	- where: 사용자의 입력에 해당하는 데이터가 반환되어야하는 URL

	- how: 데이터가 반환되어야하는 HTTP 메소드

- 예를 들어, Django 관리자의 로그인 폼에는 여러 개의 `<input>` 요소가 있습니다. 하나는 사용자 이름에 `type = "text"`, password에는 `type = "password"`, 다른 하나는 로그인 버튼인 `type = "submit"`입니다. 또한 사용자가 볼 수없는 몇 가지 숨겨진 텍스트 필드가 포함되어 있으며 장고는 다음에 수행할 작업을 결정하는 데 사용합니다.

- 또한 폼 데이터가 `<form>`의 action 속성 - / admin / -에 지정된 URL로 보내져야하며 메서드 속성 -post에 지정된 HTTP 메커니즘을 사용하여 보내야한다고 브라우저에 알립니다.

- `<input type = "submit"value = "Log in">` 요소가 트리거되면 데이터는 / admin /로 리턴됩니다.

<br>

*__GET and POST__*

- GET과 POST는 폼을 다룰 때 사용할 수 있는 **유일한 HTTP 메소드**입니다.

- Django의 로그인 폼은 POST 메서드를 사용하여 반환됩니다. POST 메서드는 브라우저가 양식 데이터를 묶어서 전송 인코딩하고 서버로 보낸 다음 응답을 수신합니다.

- 반대로 GET은 제출 된 데이터를 문자열로 묶어 URL을 작성하는 데 사용합니다. URL에는 데이터를 전송해야하는 주소는 물론 데이터 키와 값이 포함됩니다. Django 문서에서 검색을하면 `https://docs.djangoproject.com/search/?q=forms&release=1` 형식의 URL이 생성됩니다.

- GET 및 POST는 일반적으로 다른 용도로 사용됩니다.

- **시스템의 상태를 변경하는 데 사용할 수있는 요청** (예 : 데이터베이스 변경 요청)은 POST를 사용해야합니다. GET은 시스템 상태에 영향을주지 않는 요청에만 사용해야합니다.

- GET은 또한 암호 형식에 적합하지 않습니다. 암호가 URL에 표시되고 브라우저 기록 및 서버 로그에도 모두 일반 텍스트로 표시되기 때문입니다. 또한 대량의 데이터 또는 또는 이미지와 같은 2 진 데이터의 경우 적합하지 않습니다. 관리 양식에 GET 요청을 사용하는 웹 응용 프로그램은 보안 위험이 있습니다. 공격자가 시스템의 민감한 부분에 액세스하기위한 양식의 요청을 모방하는 것이 쉽습니다. POST는 Django의 [CSRF protection]와 같은 다른 보호 기능과 결합되어 액세스를보다 효율적으로 제어합니다.

- 반면 GET 요청을 나타내는 URL은 쉽게 책갈피, 공유 또는 다시 제출할 수 있기 때문에 GET은 웹 검색 양식과 같은 것에 적합합니다.


[CSRF protection]: https://docs.djangoproject.com/en/1.11/ref/csrf/

<br>

-

*__Django’s role in forms__*

- 양식 처리는 복잡한 비지니스입니다. Django의 관리자를 생각해보십시오. 다양한 유형의 여러 데이터 항목을 양식으로 표시하기 위해 준비하고, HTML로 렌더링하고, 편리한 인터페이스를 사용하여 편집하고, 서버에 반환하고, 유효성을 검사하고 정리 한 다음 추가 처리를 위해 저장하거나 전달해야 할 수 있습니다.

- Django의 폼 기능은 이 작업의 상당 부분을 단순화하고 자동화 할 수 있으며, 대부분의 프로그래머가 작성한 코드에서 수행 할 수있는 것보다 더 안전하게 수행 할 수 있습니다.

- **Django는 폼과 관련된 세 가지 부분을 처리**합니다.

	- 데이터 준비 및 재구성하여 렌더링 준비
	- 데이터 용 HTML 양식 작성
	- 제출 된 양식 및 데이터 수신 및 처리

- 이 모든 작업을 수동으로 수행하는 코드를 작성하는 것은 가능하지만 장고는이를 모두 처리 할 수 ​​있습니다.

<br>

-

*__Forms in Django__*

- 우리는 HTML 폼을 간단히 설명했지만 HTML `<form>`은 필요한 시스템의 일부일뿐입니다.

- 웹 애플리케이션의 맥락에서 'form'은 HTML <form>을 참조하거나 그것을 생성하는 [Django Form]을 참조 할 수 있습니다. 또는 제출 될 때 반환된 구조화 된 데이터나 이러한 파트의 종단 간 작업 모음에 적용됩니다.

<br>

*__The Django [Form][Django Form] class__*

- 이 컴포넌트 시스템의 핵심은 Django의 [Form][Django Form] 클래스입니다. **Django 모델이 객체의 논리적 구조, 동작 및 파트가 우리에게 표시되는 방식을 설명하는 것과 거의 같은 방식**으로 [Form][Django Form] 클래스는 양식을 설명하고 양식이 작동하고 나타나는 방식을 결정합니다.

- 모델 클래스의 필드가 데이터베이스 필드에 매핑되는 것과 비슷한 방식으로 폼 클래스의 필드는 HTML 폼 `<input>` 요소에 매핑됩니다. ([ModelForm]은 [Form][Django Form]을 통해 모델 클래스의 필드를 HTML 폼의 `<input>` 요소로 매핑합니다; 이것이 장고 관리자의 기반입니다.)

- Form의 필드 자체는 클래스입니다. **Form이 제출 될 때 양식 데이터를 관리하고 유효성 검사를 수행합니다.** [DateField]와 [FileField]는 매우 다른 종류의 데이터를 처리하며 서로 다른 작업을 수행해야합니다.

- 양식 필드는 브라우저의 사용자에게 HTML "위젯"(사용자 인터페이스 machinery)으로 표현됩니다. 각 필드 유형에는 적절한 기본 [위젯 클래스][Widget class]가 있지만 필요에 따라 재정의 할 수 있습니다.


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

- 따라서 뷰에서 모델 인스턴스를 처리 할 때 일반적으로 데이터베이스에서 모델 인스턴스를 검색합니다. 양식을 처리 할 때 일반적으로 view에서 인스턴스를 인스턴스화합니다.

- 양식을 인스턴스화 할 때 양식을 비워 두거나 미리 채울 수 있습니다. 예를 들면 다음과 같습니다.

	- 저장된 모델 인스턴스의 데이터(편집을위한 관리 양식의 경우와 같이)
	- 다른 출처에서 수집 한 데이터
	- 이전 HTML 양식 제출에서받은 데이터

- 마지막으로 이러한 경우가 가장 흥미로운 이유는 사용자가 웹 사이트를 읽는 것이 아니라 정보를 다시 보낼 수있게하기 때문입니다.

<br>

-

*__Building a form__*

*__The work that needs to be done__*

- 사용자 이름을 얻기 위해 웹 사이트에서 간단한 양식을 만들고 싶다고 가정 해보십시오. 템플릿에 다음과 같은 내용이 필요합니다.

	```
	<form action="/your-name/" method="post">
	    <label for="your_name">Your name: </label>
	    <input id="your_name" type="text" name="your_name" value="{{ current_name }}">
	    <input type="submit" value="OK">
	</form>
	```
	
- POST 메서드를 사용하여 폼 데이터를 URL / your-name /로 반환하도록 브라우저에 지시합니다. "Your name :"이라는 텍스트 필드와 "OK"라고 표시된 버튼이 표시됩니다. 템플릿 컨텍스트에 current_name 변수가 있으면 your_name 필드를 미리 채우는 데 사용됩니다.

- HTML 양식을 포함하는 템플리트를 렌더링하고 current_name 필드를 적절히 제공 할 수있는 뷰가 필요합니다.

- 양식이 제출되면 서버로 전송 된 POST 요청에는 양식 데이터가 포함됩니다.

- 이제 해당 / your-name / URL에 해당하는보기가 필요합니다. 그러면 해당 요청에서 적절한 키 / 값 쌍을 찾아서 처리 할 수 ​​있습니다.

- 이것은 매우 간단한 형태입니다. 실제로 양식에는 수십 또는 수백 개의 필드가 포함될 수 있으며 대부분 필드가 미리 채워 져야 할 수도 있습니다. 사용자는 작업을 완료하기 전에 편집 - 제출주기를 여러 번 검토해야 할 것입니다.

- 양식을 제출하기 전에도 브라우저에서 일부 유효성 검사를 수행해야 할 수도 있습니다. 우리는 훨씬 복잡한 필드를 사용하여 사용자가 달력에서 날짜를 선택하는 등의 작업을 수행 할 수 있습니다.

- 이 시점에서 Django가 우리를 위해 대부분의 작업을 수행하는 것이 훨씬 쉽습니다.

<br>

-

*__Building a form in Django__*

*__The Form class__*

- **우리는 HTML 양식이 어떻게 보이길 원하는지 이미 알고 있습니다.** 장고에서 우리의 출발점은 이것입니다 :

	```
	from django import forms

	class NameForm(forms.Form):
	    your_name = forms.CharField(label='Your name', max_length=100)
	```
	
- 이것은 단일 필드 (your_name)로 Form 클래스를 정의합니다. 인간 친화적 인 레이블을 필드에 적용했습니다.이 레이블은 레이블이 렌더링 될 때 `<label>`에 나타납니다 (이 경우 지정된 레이블은 실제로 레이블을 생략 한 경우 자동으로 생성되는 레이블과 동일합니다).

- 필드의 최대 허용 길이는 max_length에 의해 정의됩니다. 이것은 두 가지 일을합니다. HTML `<input>`에 `maxlength = "100"`을 넣습니다 (브라우저가 사용자가 처음에 그 수보다 많은 문자를 입력하지 못하게해야합니다). **또한 Django가 브라우저에서 양식을 다시 받으면 데이터 길이를 확인합니다.**

- Form 인스턴스에는 모든 필드에 대한 유효성 검사 루틴을 실행하는 [`is_valid()`][is_valid] 메서드가 있습니다. 이 메서드가 호출되면 모든 필드에 유효한 데이터가 포함되어 있으면 다음을 수행합니다.

	- return True
	- 폼의 데이터를 [cleaned_data] 속성에 저장하십시오.

- 전체 양식은 처음 렌더링 될 때 다음과 같이 표시됩니다.

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

- Django 웹 사이트로 보내진 양식 데이터는 일반적으로 **양식을 게시한 view와 ​​같은 view로 처리**됩니다. 이것은 우리가 동일한 논리의 일부를 **재사용** 할 수있게 해줍니다.

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

- POST 요청을 사용하여 양식을 제출하면 view에서 양식 인스턴스를 다시 작성하고 요청의 데이터로 채웁니다. form = NameForm(request.POST) "양식에 데이터 바인딩"이라고합니다 (이제는 바운드 형식).

- 우리는 폼의 `is_valid()` 메소드를 호출한다. True가 아니라면 양식이있는 템플릿으로 돌아갑니다. 이번에는 양식이 더 이상 비어 있지 않으므로 HTML 양식은 이전에 제출 된 데이터로 채워지며 필요에 따라 편집 및 수정할 수 있습니다.

- `is_valid()`가 True이면 이제 `cleaned_data` 속성에서 모든 유효성이 검사된 양식 데이터를 찾을 수 있습니다. 이 데이터를 사용하여 데이터베이스를 업데이트하거나 브라우저로 HTTP 리디렉션을 보내기 전에 다른 처리를 수행하여 다음에 어디로 가야하는지 알려줍니다.

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
	
	> Django는 Cross Site Request Forgeies에 대한 사용하기 쉬운 보호 기능을 제공합니다. CSRF 보호가 활성화 된 상태에서 POST를 통해 양식을 제출할 때 앞의 예와 같이 csrf_token 템플리트 태그를 사용해야합니다. 그러나 CSRF 보호는 템플릿의 양식에 직접 연결되어 있지 않으므로이 태그는이 문서의 다음 예제에서 생략되었습니다.
	
	> **_HTML5 input types and browser validation_**
	
	> 양식에 URLField, EmailField 또는 정수 필드 유형이 포함 된 경우 Django는 URL, 이메일 및 숫자 HTML5 입력 유형을 사용합니다. 기본적으로 브라우저는 이 필드에 대해 자체 유효성 검사를 적용 할 수 있습니다. 이는 장고의 유효성 검사보다 엄격 할 수 있습니다. 이 동작을 사용하지 않으려면 양식 태그에 novalidate 속성을 설정하거나 TextInput과 같이 필드에 다른 위젯을 지정하십시오.

- 우리는 이제 Django Form에 의해 설명되고 보기에 의해 처리되고 HTML <form>으로 렌더링되는 작업 웹 양식을 갖습니다.

- 그만하면 시작할 수 있지만 폼 프레임 워크는 훨씬 더 손쉽게 사용할 수 있습니다. 위에 설명 된 프로세스의 기본 사항을 이해하면 양식 시스템의 다른 기능을 이해하고 기본 시스템에 대해 더 배울 준비를해야합니다.