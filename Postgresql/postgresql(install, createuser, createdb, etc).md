brew install postgresql
brew info postgresql
brew services start postgresql

postgresql =>

user 만들때 그냥 터미널에서 createuser라고 만들면 된다
* create -s <user명)> (슈퍼유저만들기)

DB를 만들때 사용자 설정 ->
createdb —owner=<생성한 유저> <DB NAME>

‘psql postgres’ 로 패스워드 설정
\password <ID>
비밀번호 입력
\q