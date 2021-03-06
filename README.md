# url-shortener-api
An API for creating quick redirect links

## Modes
There are two modes the API can run in. When the environment variable `REDIRECT`
is set to `True` then any short link sent to the API root will return a 302 redirect.
However, if `REDIRECT` is set to `False`, the API will merely return a JSON respone
with the location of where the redirect is set.

Default is set to `True`.

## How to Deploy to DigitalOcean's App Platform

* This app will need a database, so either stand up your own or use an App Platform dev db.
* The run command should be `gunicorn --worker-tmp-dir /dev/shm url_shortener.wsgi`
* Env Vars
    * `DJANGO_ALLOWED_HOSTS` - Set this to your custom domain or `${APP_DOMAIN}` to get the default app domain from DigitalOcean
    * `DATABASE_URL` -  The database connection URL. If using App Platform dev db set to `${<NAME_OF_DB>.DATABASE_URL}` where `<NAME_OF_DB>` is the name you specify for the db at creation
    * `REDIRECT` - Set to `False` if you want the API to return where the redirect is pointed instead of actually performing the redirect
    * `APP_PLAT_ROUTE` - If you run this app under a subfolder, ex: my.api.example/api then you'll need to specify what subfolder it's running under. Format should be `/route` with a leading an no trailing slash
    * `ALLOW_OPEN_ACCESS` - Set to `True` if you want to allow open access to the POST method to add redirects. 
* Once deployed access the console and run `python manage.py migrate` to perform the initial migrations
* After performing the initial migrations run `python manage.py createsuperuser` in the console and follow the prompt to create a super user

## API Spec
A full Open API Spec can be found at `/docs/` in Swagger format.

All examples are using [`httpie`](https://httpie.org/). If you haven't checked 
it out you should.

Below are all of the public endpoints currently available.

**Note:** - All API methods end with a `/`. If you attempt to call an API method
without this you will receive a 404.


### POST `/login/`
Retrieve a users API token

*Parameters*

* `username` - Your username
* `password` - Your Password

*Example*

`http POST https://example.api/login/ username=user password=pass`

*Returns*

```
{
    "token": "YOUR_API_TOKEN"
}
```

### GET `/<YOUR_SHORT_LINK>`

#### With `REDIRECT` set to `True`

Get either a 302 redirect or a 404.

*Example*
`http https://example.api/<YOUR_SHORT_LINK>`

#### With `REDIRECT` set to `False`
Get a JSON response with the location of your redirect

*Example*
`http https://example.api/<YOUR_SHORT_LINK>`
```json
{
    "redirect": "https://mason.dev"
}
```

### GET `/manage/` - **Auth Required**
List all the redirects available

*Example*

`http https://example.api/manage/ 'Authorization: Token '$TOKEN` 

*Returns 200*
```json
[
    {
        "id": 2,
        "short_link": "do",
        "url": "https://digitalocean.com",
        "visit_count": 1
    }
    ...
]

```



### POST `/manage/` - **Auth Required**
Add an URL Redirect.

*Parameters*

* `short_link` - The short link you wish to visit to be redirected to another URL
* `url` - The URL to redirect to

*Example*

`http POST https://example.api/manage/ 'Authorization: Token '$TOKEN short_link=mason url="https://mason.dev"`

*Returns 200*
```json
{
    "message": "Redirect successfully added"
}
```

*Returns 422*
```
{
    "message": {
        "short_link": [
            "URL Redirect with this short link already exists."
        ],
        "url": [
            "This field is required."
        ]
    }
}
```

### PUT `/manage/` - **Auth Required**
Update an URL Redirect.

*Parameters*

* `short_link` - The short link you wish to visit to be redirected to another URL. This is the key
* `url` - The URL to redirect to 

*Example*

`http PUT https://example.api/manage/ 'Authorization: Token '$TOKEN short_link=mason url="https://masonegger.com"`

*Returns*
```json
{
    "message": "Redirect successfully updated"
}
```

*Returns 422*
```
{
    "message": {
        "url": [
            "This field is required."
        ]
    }
}
```

### DELETE `/manage/<str:short_link>` - **Auth Required**
Delete an URL Redirect.

*URI Parameters*

* `short_link` - The short link to delte

*Example*

`http DELETE http://example.api/manage/<SHORT_LINK>/ 'Authorization: Token '$TOKEN`

*Returns 200*
```json
{
    "message": "Redirect successfully deleted"
}
```

*Returns 404*
```json
{
    "detail": "Not found."
}
```
