Models
=======

Model is a class, that helps you to operate with your data.

For example. We have json entity Post:

``` json
{
    "userId": 1,
    "id": 1,
    "title": "delectus aut autem",
    "body": "consectetur animi nesciunt iure dolore enim quia ad veniam autem ut quam"
}
```
We can represent this entity like python model:


``` python
from arsenalqa.fields import Field
from arsenalqa.models import Model


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

Lets create the new instance of our Post, and fill it out.

``` python
post = Post()
post.title = "Hello World"
post.id = 1
print(post)  # output model of our Post
```
We see model, that looks like python dict, but this is not a dict. This is your wrapper for manipulations around dict.
When we fill model fields - fields represents your data and saves it in attribute "data":

``` python
print(post.data)
>>> {'title': 'Hello World', 'id': 1}
```
Attribute data is a temporary storage of your "raw" python dict. This dict is a prepared data for sending by transports.

Model can be linked to existing dict:

``` python
post_dict = {'title': 'Hello World', 'id': 1}
post = Post.wrap(post_dict)

post_copy_1 = Post.wrap(post_dict)
post_copy_2 = Post()
post_copy_2.data = post_dict

print(post == post_copy_1 == post_copy_2)  # True because their data are equals
print(post is post_copy_1 is post_copy_2)  # False because this is different instances
```
All 3 model instances wraps one dict. If we change this dict, it will be changed in all linked models.

``` python
post_dict = {'title': 'Hello World', 'id': 1}
post_dict['title'] = 'Hello New World'

# All three prints will output the same titles
print(post.title)
print(post_copy_1.title)
print(post_copy_2.title)
```
Models only creates new dicts, if they wasn't linked on existing dicts in creation time.