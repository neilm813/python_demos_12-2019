# Django 2.2 Cheat Sheet

# *Replace `your_project_name` and `app_name` with your chosen project & app names*

1. open terminal to where you want your project folder to be created
2. `mkdir your_project_name`
3. `cd your_project_name`
4. `mkdir server`
5. `cd server`
6. **windows**: `python -m venv env` **mac**: `python3 -m venv env`
    - new line in terminal will appear after finished
7. open vscode to `server` folder. From terminal, type: `code .`
    - mac - if `code .` doesn't work, open vscode:
      1. cmd + shift + p
      2. type: shell command: install 'code' command in PATH
      3. restart terminal
      4. open terminal to `server` folder then type `code .` again
8. Ctrl+shift+P -> 'select interpreter' -> choose the one from the env
    - if it doesn't show up, your env is still being created, wait then select interpreter again
9. Open new integrated terminal, should show `(env)` in the terminal
    - if integrated terminal doesn't show `(env)`, press the **`+`** button to open new integrated terminal
10. Install dependencies from your integrated terminal that shows `(env)` so these will be installed only for this project
    - `pip install Django==VERSION_NUMBER`
    - [Check Ver. Num On Learn Platform](http://learn.codingdojo.com/m/119/6152/42896)
11. From `server` folder `django-admin startproject your_proj_name .`
    - ` .` will make it so there's only one folder with the your_proj_name instead of also having an inner folder with the same name
12. Click debug icon in vscode side bar (bug icon Ctrl+shift+D)
    1. click gear icon
    2. select python
    3. select django
    - `launch.json` will be created - ok to close it. Can delete if you need to re-do this step.
13. `python manage.py startapp app_name` to make a new app with it's own folder
14. Add app in `settings.py` which is in `your_proj_name` folder
    - add *`'app_name',`* to 0 idx (top) of `INSTALLED_APPS` list (don't forget the comma)
15. `urls.py` inside `your_proj_name` folder
    - ``` py
      # from django.contrib import admin
      from django.urls import path, include

      urlpatterns = [
          # path('admin/', admin.site.urls),
          path('', include('app_name.urls')),
      ]
        ```
16. create `urls.py` in `app_name` folder
    - ``` py
      from django.urls import path
      from . import views

      # NO LEADING SLASHES
      urlpatterns = [
          path('', views.index, name='index'),
      ]
        ```
17. create following folder structure in `app_name` folder
    - `templates`
      - `index.html`
18. `views.py`
    - ``` py
      from django.shortcuts import render


      def index(request):
          return render(request, 'index.html')
        ```
19. `python manage.py runserver` - see Debugging Notes below

# When reopening vscode
- vscode needs to be opened to the `server` folder so it detects the virtual environment
- if terminal doesn't show `(env)`: press **`+`** icon on terminal

# Debugging Notes
## To Debug with breakpoints (won't auto reload on code changes)
- **Stop server** `ctrl + c` then press play button in debug panel or press F5
  - add a breakpoint by clicking to the LEFT of the line number so that a red circle appears

# Route Parameters / URL clarifications
## `urls.py` - NO LEADING SLASHES
- `path('users/<int:user_id>', views.user_profile, name="users_profile"),`
- this is to MATCH a *requested* URL in order for django to know which view function to route to when a URL is requested so that the proper *response* can be given to the client
- `<int:id>` is a PLACEHOLDER for whatever integer will be located at that section of the URL
  - it is a route parameter, just like a function parameter, it will store the value that is passed in when the url is visited just like a function parameter will store the value that is passed in when the function is executed
  - e.g., `http://localhost:8000/users/15` - `15` is the value of route parameter `user_id`
- when this url is visited, the `user_profile` function in `views.py` will be executed and it MUST have a corresponding parameter with the same name as the route parameter: `def user_profile(request, user_id)`

## When are values inserted into urls?
- when a client types in a url

### HTML files
- in `html` files you generally have **leading slashes on your urls**
- in `<a>` tags
- in `action` attribute of a `<form>` tag
- the above are all places where you will use jinja to insert the actual value that you want `user_id` to have
- `<a href="/users/{{ user.id }}">`
- `<form action="/users/{{ user.id }}/update" method="POST">`

### `views.py`
- you generally have **leading slashes on your urls** here
- when you `return redirect(f'/users/{some_id}')`


# Terminal Commands
## `python manage.py runserver`
- stop debug mode if it is on
- this command will auto reloading server on code changes which is useful for when you are making many changes

## Migrating
1. `python manage.py makemigrations`
2. `python manage.py migrate`

## Shell
1. `python manage.py shell`
2. `from apps.app_name.models import *`

## Source Control - Only when you need to add to github
- add the `env` folder to `.gitignore`
  - `pip freeze > requirements.txt` to create a file that lists installed packages (dependencies)
  - when repo is cloned / shared
    - create env
    - activate it
    - `pip install -r requirements.txt` to install everything required

# Django MTV (Model Template View)
- the view retrieves data from the database via the model, formats it, bundles it up in an HTTP response object and sends it to the client (browser).
- In other words, the view presents the model to the client as an HTTP response.

# App flow walkthrough
1. *Request* is made (URL visited, network tab in chrome dev tools will show the request)
2. URL is compared to the URLs in project-level `urls.py`
3. project-level `urls.py` routes to the appropriate app's `urls.py`
4. app-level `urls.py` matches the requested URL to the listed URLS
5. matched URL runs the specified method in the `views.py` file
    - view method is passed the request as the first arg and any URL parameters as additional args
6. view method redirects to another URL or renders an HTML page as a *response*

# Model Examples
- user can have many tasks, but a task can be added by only 1 user
- many to many between user and tasks for liking: user can like many tasks, task can be liked by many users
- the value of `related_name` will become a key/prop by that name on the related model that can be accessed via dot notation
- ``` py
  class User(models.Model):
      first_name = models.CharField(max_length=60)
      last_name = models.CharField(max_length=60)
      email = models.CharField(max_length=60)
      password = models.CharField(max_length=60)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)


  class Task(models.Model):
      title = models.CharField(max_length=60)
      description = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      # When a User is deleted
      # the delete will 'cascade' to delete all the user's assigned_tasks as well
      assigned_to = models.ForeignKey(
          "User", related_name="assigned_tasks", on_delete=models.CASCADE)
      liked_by = models.ManyToManyField("User", related_name="liked_tasks")
  ```

# Troubleshooting
## `pip` not recognized (windows)
- add it to path
- use current python path to see where python is installed
- pip is located in same directory with `\Scripts\` appended

## segmentation failure
- don't use bash

## Invalid Salt
- add `decode` to end `hashed_pw = bcrypt.hashpw('test'.encode(), bcrypt.gensalt()).decode()`
- is pw in db plaintext?

## Migration Issues
### Reset DB
1. `pip install django-extensions`
2. add `django_extensions` to `INSTALLED_APPS`
3. `python manage.py reset_db`

### New Column Issue / Default Value
- can add a bogus default value just to get passed the error, then delete the existing rows from that table to start fresh, or the below
1. delete new field from model
2. `python manage.py makemigrations`
3. `python manage.py migrate`
4. if error
  - `python manage.py migrate --fake`
5. add field back
6. makemigrations & migrate

## `RuntimeError: __class__ not set defining 'AbstractBaseUser' django`
- downgrade python to 3.7.x (to be compatible with django 1.10) or upgrade django

## Terminal
### Powershell
- [Running Py With Powershell](https://www.windowscentral.com/how-create-and-run-your-first-powershell-script-file-windows-10#run_powershell_script_windows10)

## Misc
### Erroneous Unresolved Import
- ctrl + shift + p > Open Settings (JSON)
- comment out `{"python.jediEnabled": false}` in `settings.json`

# Deployment
-[console.aws](https://us-west-1.console.aws.amazon.com/console/home?region=us-west-1#)
- create an account then go back to this url after logging in or navigate to the AWS Management Console manually after logging in

## USE GIT BASH IF ON WINDOWS, NOT COMMAND PROMPT
1. Launch a virtual machine With EC2
2. select Ubuntu Server 18.04 LTS (HVM)
3. select free tier option
4. click Review and Launch
5. click Edit security groups
6. Under Source: select My IP
7. click Add Rule
    - Type: HTTP
    - Source: Anywhere
8. click Add Rule
    - Type: HTTP
    - Source: Anywhere
9. click Review and Launch
10. click Launch
11. Select an existin gkey pair or create a new key pair
    - steps to create a new key pair if you don't have one
    1. select Create a new key pair
    2. Key pair name: django_pem
    3. click Download Key Pair
        - save it to a folder you will **NEVER** use as a github repo
    4. click Launch Instances
12. click View Instances
13. update Name column: django
14. http://learn.codingdojo.com/m/119/6138/42635
- https://us-west-1.console.aws.amazon.com/ec2/v2/home?region=us-west-1#Instances:sort=desc:publicIp


# Optional Design Patterns
- only try these if you are not struggling

## multiple views & template sub folders - better organization
- You can do everything in 1 `views.py` file and all `.html` files in `templates` folder if it's easier
- Splitting views is useful when you have more than one model, e.g., `User` and `Task` and you want to have a route for all users and a route for all tasks, you can't have the two view functions with the name 'all' and two html files named 'all' unless they are split into separate view files and separate template sub-folders
- **create the following structure replacing `users` and `tasks` with what is relevant to your project (you may only need 1 view file and 1 `templates` sub folder to start, but this will make it easier to add more when needed)**
- delete `views.py` and create the following dir structure in `app_name` folder
  - `views`
    - `users.py`
    - `tasks.py`
    - **`__init__.py`**
  - `templates`
    - `app_name`
      - `users`
        - `all.html`
      - `tasks`
        - `all.html`
      - `shared`
  - `static`
    - `app_name`
      - `css`
- `shared` is for `.html` files that are used by multiple different views files
- `app_name` folder prevents the following problem: django will merge each app's `templates` folder into a single `templates` folder, which may cause folder or file name conflicts if different apps use the same folder or file names

## `__init__.py` in `views` folder
- ``` py
  # import all functions from all view files
  from .users import *
  from .tasks import *
    ```

## `users.py`
- ``` py
  from django.shortcuts import render


  def login(request):
      return render(request, 'app_name/users/login.html')


  def all(request):
      return render(request, 'app_name/users/all.html')

    ```

## `tasks.py`
- ``` py
  from django.shortcuts import render


  def all(request):
      return render(request, 'app_name/tasks/all.html')

    ```

## `app_name/urls.py`
- ``` py
  from django.urls import path
  from . import views

  urlpatterns = [
      path('', views.users.login, name='login'),
      path('users/all', views.users.all, name='all_users'),
      path('tasks/all', views.tasks.all, name='all_tasks'),
  ]
  
    ```

## `base.html` pattern
- [Django Girls base.html tutorial](https://tutorial.djangogirls.org/en/template_extending/)
- create a block in the head of the `base.html` that you can use to inject stylesheet `<link>` tags into from other html files
  - e.g., your extension html file has it's own personal stylesheet that you need the `base.html` to load
- create a block in between the `<title>` if you want each page to be able to set the `<title>` of the html page

## Fat models, skinny views
- move all the logic that relates to the model onto the model itself to keep that separate from the views (separation of concerns)
- ``` py
  import re # regex

  EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

  class UserManager(models.Manager):

    def create(self, request):
        user = None

        if self.is_reg_valid(request):
            user = User(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
            user.save()
        return user


    def is_reg_valid(self, request):

        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, "invalid email address.")
      
        if len(request.POST['first_name']) < 3:
            messages.error(request,
                           "First Name must be more than 2 characters.")

        if len(request.POST['first_name']) < 3:
            messages.error(request,
                           "Last Name must be more than 2 characters.")

        if len(request.POST['password']) < 8:
            messages.error(request,
                           "Password must be more than 8 characters.")

        if request.POST["password"] != request.POST["password_confirm"]:
            messages.error(request, "Passwords must match.")

        storage = messages.get_messages(request)
        storage.used = False  # don't clear messages
        return len(storage) == 0
    ```
- in `User` class
  - ``` py
      # give User.objects access to the methods on UserManager
      objects = UserManager()
      ```
- in views
  - ``` py
      new_user = User.objects.create(request)

      if new_user:
        pass # success - add to session
      else:
        pass # fail - redirect
      ```

## [Split models into multiple files](https://chrisbartos.com/articles/how-to-organize-your-models/)
- implemented in same way as multiple views

## `admin` app
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site