# Emmet Syntax 정리

> [https://docs.emmet.io/abbreviations/syntax/](https://docs.emmet.io/abbreviations/syntax/) 를 읽고 정리 + (implicit-names, lorem-ipsum)
> 
> 2017년 5월 8일 월요일 정리 

- *__Emmet__*

	- 빠른 HTML 마크업/CSS 스타일링을 위한 패키지
	- CSS selectors 와 유사한 구문 사용
	- 구문을 작성한 뒤 `tab`키를 눌러 사용

<br>

- DTD*(document type definition, 문서형식정의)*
	- `html:5` + `tab` == `!`  + `tab` (느낌표 하나로도 가능!!!)
	- 그 외 4t, 4s 등 또 다양함...

<br>

- 요소*(Elements_시작 태그와 끝 태그를 갖는 의미적인 하나의 덩어리)*

	- Emmet은 어떤 단어라도 태그로 변환할 수 있다.

		```
		foo + tab → <foo></foo>
		abc + tab → <abc></abc>
		div + tab → <div></div>
		```
		
<br>
	
- 중첩 연산자*(Nesting operators)*
	
	- 자식*(Child)* 요소: >  
	: `> 연산자`를 사용하여 서로의 요소를 서로 중첩시킬 수 있다.

		```
		div>ul>li
		```
		```
		<div>
			<ul>
				<li></li>
			</ul>
		</div>
	  	```
	  	
	- 형제*(Sibling)* 요소: +  
	: `+ 연산자`를 사용하여 동일한 수준의 요소를 서로 배치한다.
	
		```
		div+p+bq
		```
		```
		<div></div>
		<p></p>
		<blockquote></blockquote>
		```
	
	- 한 레벨 위로 트리를 올라감*(Climb-up)*: ^  
	: `> 연산자`를 사용하면 한 레벨씩 트리가 내려가고 형제요소를 가장 깊은 요소에 넣는다.
	
		```
		<div></div>
		<div>
			<p><span><em></em></span></p>
		</div>
		```
		
		하지만(!), `^ 연산자`를 사용하면 **한 레벨 위**로 트리를 올라갈 수 있다.
		
		```
		div+div>p>span+em^bq
		```
		```
		<div></div>
		<div>
			<p><span></span><em></em></p>
			<blockquote></blockquote>
		</div>
		```
		
		`^ 연산자`를 **여러개** 사용할 수 있다.
		
		```
		div+div>p>span+em^^^bq
		```
		```
		<div></div>
		<div>
			<p><span></span><em></em></p>
		</div>
		<blockquote></blockquote>
		```
		
	- 요소 출력 횟수*(Multiplication)*: *
	
		```
		ul>li*5
		```
		```
		<ul>
			<li></li>
			<li></li>
			<li></li>
			<li></li>
			<li></li>
		</ul>
		```
		
	- 하위 트리를 그룹화*(Grouping)*: ()

		`<header>...<header>` 영역과 `<footer>...</footer>` 영역 그룹화한 예제  
		**(두 그룹이 동일한 레벨을 가진다)**
	
		```	
		div>(header>ul>li*2>a)+footer>p
		```
		```	
		<div>
			<header>
				<ul>
					<li><a href=""></a></li>
					<li><a href=""></a></li>
				</ul>
			</header>
			<footer>
				<p></p>
			</footer>
		</div>
		```
		
		그룹에 * 연산자를 사용할 수도 있다.
		
		```
		(div>dl>(dt+dd)*3)+footer>p
		```
		```
		<div>
			<dl>
				<dt></dt>
				<dd></dd>
				<dt></dt>
				<dd></dd>
      			<dt></dt>
				<dd></dd>
			</dl>
		</div>
		<footer>
			<p></p>
		</footer>
		```
		
<br>

- 속성 연산자*(Attribute operators)*  
: 출력된 요소의 속성값 수정할 때 사용

	- ID and CLASS 속성

		```
		div#header+div.page+div#footer.class1.class2.class3
		```
		```
		<div id="header"></div>
		<div class="page"></div>
		<div id="footer" class="class1 class2 class3"></div>
		```
	
	- 맞춤 속성*(Custom attributes)*: [attr]

		```
		td[tile="Hello world!" colspan="3"]
		```
		```
		<td tile="Hello world!" colspan="3"></td>
		```
	
		사이띄기로 속성 구분하는 예제
	
		```
		td[colspan title]
		```
		```
		<td colspan="" title=""></td>
		```
	- 번호 매기기*(Item numbering)*: $  
	: 숫자 위치에 $ 연산자 사용
	
		```
		ul>li.item$.5
		```
		```
		<ul>
			<li class="item1"></li>
			<li class="item2"></li>
			<li class="item3"></li>
			<li class="item4"></li>
			<li class="item5"></li>
		</ul>
		```
		
		```
		ul>li.item$$$.*5
		```
		```
		<ul>
			<li class="item001"></li>
			<li class="item002"></li>
			<li class="item003"></li>
			<li class="item004"></li>
			<li class="item005"></li>
		</ul>
		```
		
	- 번호 매기기 기본 및 방향 변경: @(@-, @N)

		\- (hyphen): 방향 변경
	
		```
		ul>li.item$@-*5
		```
		```
		<ul>
			<li class="item5"></li>
			<li class="item4"></li>
			<li class="item3"></li>
			<li class="item2"></li>
			<li class="item1"></li>
		</ul>
		```
	
		@N: 시작번호 설정
	
		```
		ul>li.item$@3*5
		```
		```
		<ul>
			<li class="item3"></li>
			<li class="item4"></li>
			<li class="item5"></li>
			<li class="item6"></li>
			<li class="item7"></li>
		</ul>
		```
		```
		ul>li.item$@-3*5
		```
		```
		<ul>
			<li class="item7"></li>
			<li class="item6"></li>
			<li class="item5"></li>
			<li class="item4"></li>
			<li class="item3"></li>
		</ul>
		```

<br>

- 문자*(Text)*: {}

	```
	a{Click me}
	```
	```
	<a href="">Click me</a>
	```
	
	div, p 와 같은 요소 뒤에 사용하면 특별한 의미를 가진다.
	
	```
	<!-- a{Click}+b{here} -->
	<a href="">Click</a><b>here</b>
	
	<!-- a>{Click}>b{here} -->
	<a href="">Click<b>here</b></a>
	```
	
	```
	<!-- p>{Click }+a{here}+{ to coninue} -->
	<p>Click <a href="">here</a> to coninue</p>
	
	<!-- p{Click }+a{here}+{ to coninue} -->
	<p>Click </p>
	<a href="">here</a> to coninue
	```
	
<br>

- 참고! 
	- 띄어쓰기 하지 않기. `사이띄기`는 Emmet에서 구문 분석 정지 기호!

		```
		(header > ul.nav > li*5) + footer
		```
	
	- 텍스트에서 약어 입력하고 확장 가능함

- Emmet 작성시 생각해 볼 사항

	- 읽기 쉽게(readable), 신속하게 확장 및 제거 가능(quickly expandable and removable)		
	→ 내가 이해하기로는 Emmet 을 사용하는 목적을 의식하며 작성하기
	- 약어는 간단하게 사용하기. 하나의 복잡한 약어를 작성하는 것이 몇 가지 간단한 것을 작성하고 입력하는 것보다 훨씬 느리고 오류가 발생하기 쉽다. *(오늘 겪은 일;;)*
	- **요약:** *간단하게, 읽기 쉽게, 신속하게 확장 및 제거 가능하게.*

<br>

- *__암시적(!) 태그 이름__*  
: Emmet 에서는 태그 이름을 생략할 수 있다.
	- 생략 후 확장할 시 상위 요소를 찾음

		```
		div.content → .content
		```
		```
		<div class="content"></div>
		```
	
	- 일부 상위 요소의 이름을 확인하는 방법
		- li → ul, ol
		- tr → table, tbody, thead, tfoot
		- td → tr
		- option → select, optgroup

	- 추가 예
		- .wrap>.content	→ div.wrap>div.content
		- em>.info → em>span.info
		- ul>.item*3 → ul>li.item*3
		- table>#row$*4>[colspan=2] → table>tr#row$*4>td[colspan=2]

<br>

- *__더미 텍스트(Lorem ipsum) 생성__*
	- 그냥 lorem 또는 ipsum
	- 뒤에 숫자만 더붙여서 양 조절 가능  
		`lorem5``lorem10`
		
		```
		ul.generic-list>lorem10.item*4
		```
		
<br>

- *__tip!__*
	- atom 에디터, 문서 설정 시 주언어 설정 변경
		- `Settings → Package → emmit → settings → View code` 로 들어간다
		- Emmit 코드가 열리면 `emmet → node_modules → emmet → lib → snippets.json` 을 연다.
		- "lang": "ko", "locale": "ko-KR" 로 변경하면 완료~

		- 클라우드 서비스 (ex: Drop box) 로 세팅관리
			- 관리하는 이유: 패키지가 업데이트 됐을 시, 충돌로 인해 (주언어 설정 이외의 다른) 설정을 다시해야하는 경우도 생긴다. 그것을 대비해 클라우드에 세팅 파일을 저장~ _20170510(내용추가)

<br>

❗️  
CSS, Actions 부분 추가 정리 예정...  
Actions 는 내일... - 170509

<br>

### Actions (5월 15일 추가)

- Expand Abbreviation (interactive)

	`ctrl` + `alt` + `enter`
	
	> 구문 입력과 동시에 코드 블록으로 변형
	
- Wrap with Abbreviation

	`ctrl` + `alt` + `w`
	
	> 현재  커서가 위치한 태그를 감싸는 태그 생성
	
- Previous/Next Edit Point

	- 이전: `ctrl` + `alt` + `←`
	- 다음: `ctrl` + `alt` + `→`

	> 이전/다음 **편집점**으로 이동
	
	> 현재는 마그넷과 단축키가 겹쳐 `ctrl` + `←` 또는  `→` 로 변경
	
- Select Previous/Next Item

	- 이전: `ctrl` + `shift` + `←`
	- 다음: `ctrl` + `shift` + `→`

- 주어진 식의 값을 구함

	`⌘` + `shift` + `y`
	
[출처](http://alistasha.com/2017/03/23/atompackage-emmet-actions/)