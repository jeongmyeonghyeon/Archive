from django.db import models


# 모델 자체가 이해가 안간다.

# name과 tagline을 필드로 갖는 Blog Model
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


# name과 email을 필드로 갖는 Author(저자) Model
class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


# Post의 entry라는게 어떤거지?...
# entry 작성시 Blog와 Author를 선택함...
class Entry(models.Model):
    # Blog Model을 참조하는 blog field
    blog = models.ForeignKey('Blog')
    # headline field (아마 제목)
    headline = models.CharField(max_length=255)
    # body_text field (아마 본문)
    body_text = models.TextField()
    # pub_date field (아마 생성일)
    pub_date = models.DateField()
    # mod_date field (아마 수정일)
    mod_date = models.DateField()
    # Author(저자)와 다대다 관계인 authors field
    # 하나의 저자는 많은 기입을 할 수 있다.
    # 하나의 기입은 여러 작성자가 생성할 수 있다.
    authors = models.ManyToManyField('Author')
    # n_comments (아마 댓글수(!))
    n_comments = models.IntegerField()
    # n_pingbacks (아마 조회수)
    n_pingbacks = models.IntegerField()
    # rating field (아마 별점)
    rating = models.IntegerField()

    def __str__(self):
        return self.headline
