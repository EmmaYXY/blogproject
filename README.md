# blogproject
a novice practice of django to develop a blog.

- 在迁移数据库表至数据库中，得到如下错误：

`TypeError: __init__() missing 1 required positional argument: 'on_delete'`

后去stackoverflow网站找到答案，需要

```
categorie = models.ForeignKey(
    'Categorie',
    on_delete=models.CASCADE,
)
```

但执行`python manage.py makemigrations`时依旧错误，后才发现ForeignKey有两个，我只改了一个。这是一个想当然的错误。