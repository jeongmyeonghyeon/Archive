# Requests/BeautifulSoup 정리

### Requests

> [http://docs.python-requests.org/en/master/user/quickstart/](http://docs.python-requests.org/en/master/user/quickstart/)

- 'requests는 Python을위한 유일한 Non-GMO HTTP 라이브러리이며, 사람이 소비하기에 안전합니다.' 라고 설명은 되있는데... 요청과 관련 있는 라이브러리 정도로 이해하고 있다.
- 인터넷 자원에 접근할 수 있도록 해주는 모듈...
- 예제에서는 웹툰페이지에 접근해 html 문서의 텍스트를 가져오는 정도로 사용했다.

### BeautifulSoup

> [https://www.crummy.com/software/BeautifulSoup/bs4/doc/](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 을 읽고 정리

- Beautiful Soup is a Python library for pulling data out of HTML and XML files.

	> Beautiful Soup은 HTML 및 XML 파일에서 데이터를 가져 오는 Python 라이브러리입니다.
	
- 설치

	- Beautiful Soup 설치
	
		- `pip install beautifulsoup4`
	
	- paser 설치

		- `pip install lxml`
		- lxml 을 추천함
		- `BeautifulSoup(markup, "lxml")` 로 사용

		> parser: 일단은 구문 분석 프로그램 정도로 보면 될듯하다.

- 네 가지 객체의 종류가 있다.

	- Tag, NavigableString, BeautifulSoup, Comment

- 메소드와 인자값으로 트리 탐색과 검색이 가능하다

	- 트리 탐색
	
		- 태그 이름을 이용한 탐색
	
			```
			soup.head
			soup.title
			soup.body.b
			soup.a
			위와 같이 접근 가능
			```
			```
			soup.find_all('a')
			모든 a 태그 탐색
			```
		- ... 뭐 많음
			
	- ✨트리 검색✨

		- `find_all()`
			- `class_`
			- `string=""`
			- `limit`
			- `find()` / `limit` 인자를 사용한 `find_all`과 비슷하다.
		
		- `select`
			- CSS 선택자를 인자값으로 선택이 가능하다.
				- `e e`, `e > e`, `e:nth-of-type(3)`, `a[href]`, ...

	- 수정

		- 은 패스...

	- 출력

		- `prettify()`