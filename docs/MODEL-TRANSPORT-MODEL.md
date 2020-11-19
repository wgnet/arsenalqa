Model-Transport-Model relations
================================

Relations between entities are very important part. If you have visual relations in your code, you can see how this code
works without documentations.

We can make relations between models by transports. It means that you can create model, send model data by http, receive
response wrapped in other model instance, and make a new request from this model.

Our post entity has relation with it comments.

``` python
from arsenalqa.fields import Field
from arsenalqa.models import Model
from arsenalqa.transports.managers import TransportManager
from arsenalqa.transports.http import Http


class Comment(Model):

    http: Http = TransportManager(Http, url='https://jsonplaceholder.typicode.com/comments/{id}/')

    id = Field()
    post_id = Field(name='postId')  # relation id with our Post model
    name = Field()
    email = Field()

print(Comment.http.get())
```
This is a list of comments which users sent on posts. This end user logic is looks like:

- User creates his own post first.
- Others users post comments on the user post.
- Server backend creates new relation between post and comments.

User can find post comments by two different resources:
- `https://jsonplaceholder.typicode.com/posts/{postId}/comments/`
- `https://jsonplaceholder.typicode.com/comments/{commentId}/`

First one is the relation between posts and comments. And the second one is the root resource for comments only.

Lets adapt our Post model and Http.

At first we have to customise Http class for Post and it comments

``` python
from urllib.parse import urljoin

from arsenalqa.fields import Field
from arsenalqa.models import Model
from arsenalqa.transports.managers import TransportManager
from arsenalqa.transports.http import Http


class Comment(Model):

    http: Http = TransportManager(Http, url='https://jsonplaceholder.typicode.com/comments/{id}/')

    id = Field()
    post_id = Field(name='postId')  # relation id with our Post model
    name = Field()
    email = Field()


class PostsHttp(Http):

    def get_comments(self, wrapper=Comment.wrap, expected_status=200, **kwargs):
        return self.get(
            url=urljoin(self.prepare_url(), 'comments/'),
            wrapper=wrapper,
            expected_status=expected_status,
            **kwargs
        )
```
Our custom http relation is ready in `PostsHttp` class. It contains one new method `get_comments`:

- `wrapper=Comment.wrap` this parameter says which wrapper callable should be used.
- `expected_status=200` validates that response status is 200, if not raises exception.

Let's replace our Http transport in Post model:

```python
class Post(Model):

    http: PostsHttp = TransportManager(PostsHttp, url='https://jsonplaceholder.typicode.com/posts/{id}/')

    id = Field()
    user_id = Field(name='userId')
    title = Field()
    body = Field()


print(Post(id=1).http.get_comments())
```

Method returns list of comments wrapped in Comment model. Lets get one comment from this post comments and make request in chain.

``` python
print(Post(id=1).http.get_comments()[0].http.get())
```
We got post comments list which elements wrapped in Comment model(`Post.http.get_comments()`), than we got first comment(`[0]`) model,
and made a request to `https://jsonplaceholder.typicode.com/comments/{id}/` resource(`.http.get()`) which has returned new Comment model instance.

