- 업데이트된 `.gitignore`를 적용해 다시 commit할 때

	```
	git rm -r --cached .
	git add .
	git commit -m "fixed untracked files"
	```
	
	> [https://stackoverflow.com/questions/11451535/gitignore-is-not-working](https://stackoverflow.com/questions/11451535/gitignore-is-not-working)