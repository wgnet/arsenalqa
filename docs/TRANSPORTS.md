Transports
===========

We will use http transport as example.

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


post = Post()
post.id = 1
print(post.http.get())
```
We has added new http transport with TransportManager and Http class. Now we can use all of the http methods(POST, GET, PUT, etc.)
with our model. By default all responses are wrapped in new instance of current model(Post in our case)

``` python
response = post.http.get()
print(type(response))
```

Response is not the same instance as we sent(this is true for their data too)
```python
print(post is response)  # False
```
This behavior was made for QA engineers. We always need to comparison of expected and actual results. That's why we don't
update our current model by response.

**How does it works?**

When we get `post.http` attribute first time, the TransportManager creates new instance of Http class, and sets others
parameters like:

``` python
Http(url='https://jsonplaceholder.typicode.com/posts/{id}', model=post)
# Parameter `model` has been added by TransportManager backend.
```
TransportManager links the instance of Http to our `post` instance back.
When we call `post.http` again, we will use the same instance of Http as before.

**How does Http understands how to get a post with id=1?**

``` python
class Post(Model):

    http: Http = TransportManager(Http, url='https://jsonplaceholder.typicode.com/posts/{id}')
    ...
```
It is url pattern. It works like `safe format`. `Http.prepare_url` method gets url, and trying to fill out all `{name}`
parameters from model fields. After this procedure, it strips all `//` symbol duplicates, except scheme(http://).

In this case, if my REST service returns list of posts on `https://jsonplaceholder.typicode.com/posts/` resource, then I can get it, if
`post.id` attribute is blank:

``` python
post = Post()
print(post.http.get())
```
We can get list of posts from `Post` class:

``` python
print(Post.http.get())
```
When we calling http from class, it creates new instance of Http on every call.

``` python
print(Post.http.get())  # first Http instance
print(Post.http.get())  # second Http instance
```
Http methods like POST, PUT and PATCH takes request body from linked `model.data` attribute.

``` python
post = Post()
post.title = 'My title'
post.body = 'New body'

print(post.http.post())
# This post was created by POST method. Attribute `id` was set by the server side.
```
Before sending POST request `Http.post` takes `model.data` from model. `model.data` is python prepared data(dict) for sending to the web.
It means that, all dates saved as strings, all submodels saved as dicts or lists of dicts and etc.
