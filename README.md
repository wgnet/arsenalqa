Quick start
=====================================

ArsenalQA is a framework that helps to abstract QA functional tests from  developers realisation in ORM style.

Model your data - Models help you to change and test your data faster.

Make you transports abstract - it helps you to add them on the fly.

Make relations between models by transports or other models - it helps your colleagues to understand your code easily.

**Why not django, graphql, etc?**

Because all of this instruments are created for developers. Developers code works in the middle of project logic,
between two endpoints: users and database(for example), and are adapted for using strong interaction protocols,
whereas QA need more flexible and comfortable behavior.


**Instalation:**
```
$ pip install arsenalqa[http]
```

Lets make our first example with Post model:

``` python
from arsenalqa.fields import Field
from arsenalqa.models import Model
from arsenalqa.transports.managers import TransportManager
from arsenalqa.transports.http import Http


class Post(Model):

    http: Http = TransportManager(Http, url='https://jsonplaceholder.typicode.com/posts/{id}')

    id = Field()
    user_id = Field(name='userId')
    title = Field()
    body = Field()
```

Our entity was created.

Now you can:

``` python
print(Post.http.get())  # get list of posts models

my_model = Post()  # new instance of my model
my_model.id = 1
response_model = my_model.http.get()  # get single instance from web
print(response_model)  # model from web
print(response_model.id == my_model.id)

# Lets fill new instance of our model and post it to the web
new_model = Post()
new_model.title = 'My new title'
new_model.body = 'My new Post body'

new_created_model = new_model.http.post(expected_status=201)  # Send via http POST method
print(new_created_model)  # Response wrapped in new model. Has filled field id.
print(new_model == new_created_model)  # False because, response model contains only id field.

# Lets get list of posts from web, and filter it by user
print(Post.http.get().filter_by_attrs(user_id=1))

# Lets get list of posts from web, and filter single unique model by id
first_post = Post.http.get().unique_by_attrs(id=1)
print(first_post)

# Lets request again from response model, and get title attribute from response model
print(first_post.http.get().title)
```
Congrats! Now you can start learning this framework. **More [docs](https://github.com/wgnet/arsenalqa/blob/main/docs/INDEX.md) page!**