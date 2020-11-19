Fields
========

Fields are used for data operating by models. Fields are python `Descriptors`. When you get a field, it reads
some value from dict data by a key, and transform it in some python object. When you set field, it transform a value into
simple type and writes it out into the dict data.

**DateTime example:**

We have dict with date in ISO format, which came from web.

```json
{"date": "1981-02-21"}
```
We want to compare this date with some other date generated in python. We cant just compare string and python datetime format.
We must convert date into python datetime for comparison, and into string when we want to send this date to the web.

```python
from datetime import datetime

expected_datetime = datetime(year=1981, day=21, month=2)
actual_datetime = {"date": "1981-02-21"}["date"]

print(expected_datetime == actual_datetime)
```

Fields can do this on the fly.

``` python
from datetime import datetime
from arsenalqa.fields import Field, DateTimeField
from arsenalqa.models import Model


class DateTimeExample(Model):

    date = DateTimeField(fmt='%Y-%m-%d')  # fmt - datetime format mask for saving

expected_datetime = DateTimeExample()
expected_datetime.date = datetime(year=1981, day=21, month=2)

actual_datetime = DateTimeExample.wrap({"date": "1981-02-21"})

print(expected_datetime.date == actual_datetime.date)  # True
```

Lets look inside:

``` python
datetime_model = DateTimeExample()
print(datetime_model.data)  # data of our model is empty. Lets add datetime

datetime_model.date = datetime.now()  # create datetime and set it to field date
print(datetime_model.data)  # descriptor DateTimeField converts datetime in str type and saves it into data
print(datetime_model.date)  # get field from data converts field in python datetime
print(type(datetime_model.data['date']))
print(type(datetime_model.date))
```

**ModelField and ListModelField**

We can make entities relations in deep by models.

``` json

{
    "id": 1,
    "logo":
        {
            "icon": "icon.png",
            "background": "background.png"
        },
    "countries":[
        {"code": "ru", "currency": "rub"},
        {"code": "eu", "currency": "eur"},
        {"code": "by", "currency": "byn"},
    ]
}
```
In this case `logo` is submodel, and countries is submodels list of User model

``` python
from arsenalqa.fields import Field, ModelField, ListModelField
from arsenalqa.models import Model


class Logo(Model):
    icon = Field()
    background = Field()


class Country(Model):

    code = Field()
    currency = Field()


class User(Model):
    id = Field()
    logo = ModelField(Logo)
    countries = ListModelField(Country)
```

We have wrote all models for this case. Main model is User. Logo and Country are submodels of our model.

Lets fill this model by our dict.

``` python
user = User.wrap({
    "id": 1,
    "logo":
        {
            "icon": "icon.png",
            "background": "background.png"
        },
    "countries":[
        {"code": "ru", "currency": "rub"},
        {"code": "eu", "currency": "eur"},
        {"code": "by", "currency": "byn"},
    ]
})

print(user)
print(user.logo.icon)

print(user.countries.unique_by_attrs(code="ru").currency)  # This string filters one submodel from countries list and gets country currency

new_country = Country()
new_country.code = 'us'
new_country.currency = 'usd'
user.countries.append(new_country)
print(user.countries)  # New country in countries list
```
