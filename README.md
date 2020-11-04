Quick start
=====================================

ArsenalQA is a framework that helps to abstract QA functional tests from  developers realisation in ORM style.

Model your data - Models helps you to change and test your data quicker.

Make you transports abstract - it helps you to add them faster.

Make relations between models by transports or other models - it helps your colleagues to understand your code easily.

**Instalation:**
```
$ pip install arsenalqa[http]
```

Lets make our first example:

``` python
from arsenalqa.fields import Field
from arsenalqa.models import Model
from arsenalqa.transports import TransportManager
from arsenalqa.transports.http import Http


class MyModel(Model):

    http: Http = TransportManager(Http, url='https://jsonplaceholder.typicode.com/todos/{id}')

    id = Field()
    user_id = Field(name='UserId')
    title = Field()
    completed = Field()
```

Our model was created.

Now you can:

``` python
print(MyModel.http.get())  # get list of todos models
>>> I:[{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}, {'userId': 1, 'id': 2, 'title': 'quis ut nam facilis et officia qui', 'completed': False}

my_model = MyModel()  # new instance of my model
my_model.id = 1
response_model = my_model.http.get()  # get single instance from web
print(response_model)  # model from web
>>> M:{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}

print(response_model.id == my_model.id)
>>> True

# Lets fill new instance of our model and post it to the web
new_model = MyModel()
new_model.user_id = 1
new_model.title = 'My new title'
new_model.completed = False

new_created_model = new_model.http.post()  # Send via http POST method
print(new_created_model)  # Response wrapped in new model. Has filled field id.
>>> M:{'id': 201}
print(new_model == new_created_model)  # False because, response model contains only id field.
>>> False

# Lets get list of todos from web, and filter it by completed status
print(MyModel.http.get().filter_by_attrs(completed=False))
>>> I:[{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}, {'userId': 1, 'id': 2, 'title': 'quis ut nam facilis et officia qui', 'completed': False},...

# Lets get list of todos from web, and filter single unique model by id
first_todo = MyModel.http.get().unique_by_attrs(id=1)
print(first_todo)
>>> M:{'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}

# Lets request again from response model, and get title attribute from response modle
print(first_todo.http.get().title)
>>> delectus aut autem
```
Congrats! Now you can start learning this framework. **You can find next steps inside the [docs](https://github.com/wgnet/arsenalqa/tree/main/docs) directory!**