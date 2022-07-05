""" This is the default imported function in older versions of Django for the views.py file (source:
https://www.youtube.com/watch?v=pRNhdI9PVmg&list=PLH9Qw2PrioB4_n5Z4nLCQGp82zxl5R7Pq&index=2&t=704s)"""
from django.shortcuts import render
from django.http import HttpResponse

""" These libraries will allow me to authenticate a user that has created their account, as well as manipulate data
from the database (source: https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip . If that link's unavailable,
try this link instead: https://cs50.harvard.edu/web/2020/projects/2/commerce/ .)
"""
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

""" This will allow me to use the "@login_required" attribute, which will prevent a view from being executed 
unless the user has logged in (source: 
https://docs.djangoproject.com/en/4.0/topics/auth/default/#the-login-required-decorator )
"""
from django.contrib.auth.decorators import login_required

# This will import the forms from forms.py
from .forms import AddGameForm

# This will import the models from models.py
from .models import User, Games

# Create your views here

""" This view() will render the home page.

I will also render the games for the currently logged-in user if a user logs in. To check if a user is logged in, 
I will use an "if" statement with the following snippet: "request.user.is_authenticated:"  (source: daphtdazz's 
answer from https://stackoverflow.com/questions/42794518/show-different-content-based-on-logged-in-user-django .)
"""
def index(request):

    # If a user logs in, I will show them their games
    if request.user.is_authenticated:

        logged_user = request.user  # This stores the data from the currently logged in user
        logged_user_id = logged_user.id  # PK of the currently logged in user

        return render(request, "index.html", {
            "games": Games.objects.filter(user_id=logged_user_id)
        })
    # This will render the page if the user is not logged in
    else:
        # This renders the index.html file
        return render(request, "index.html")

""" I will create the sign up view(). For the time being, the only thing that this will do is redirect the user to a 
page called /signup or /create. For this, I need to create a page called create.html or signup.html. And, for the time 
being, that page will be empty.

After completing the fields for the Sign Up form in forms.py, I need to go to views.py, call the forms from there, and 
send them to sign_up.html.

I will need to use an “if” statement in the sign_up view() to detect if the user has submitted the form from the Sign 
Up page. Otherwise, I will simply render the Sign Up page using “return render()”. I will detect if a POST request has 
been made. If it was made, I will insert the data from each input into a different variable.

Then, I will use Django’s Query Set syntax to insert the data stored in those variables into the database.

Source of the code used in "try", "except", and using the login() function: 
https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip . If that link's unavailable,
try this link instead: https://cs50.harvard.edu/web/2020/projects/2/commerce/ .
"""
def sign_up(request):

    # This variable will store the Sign Up form from forms.py
    # form = SignUpForm()

    # This detects if the user submitted the form in the Sign Up page
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]


        # If the user's password is different than the one in "confirm password", I will display an error
        if password != confirm_password:
            return render(request, "sign_up.html", {
                "error_message": "The passwords don't match. Please, type them again."
            })

        # This will try to create the new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        # If the username's been taken by someone else, I will display an error message
        except IntegrityError:
            return render(request, "sign_up.html", {
                "error_message": "That username is being used by someone else. Try another username."
            })

        # This will login the user if they successfully create an account
        login(request, user)

        # This will send the user to the home page
        return HttpResponseRedirect(reverse("index"))

    else:
        # This renders the sign up page
        return render(request, "sign_up.html")

""" I will create the login page, and the user should be able to enter that page from the links on the home page.

This is more or less similar to creating the sign up page. I need to to create the appropriate view() function, create 
a new html file for the login page, and add that views() as a URL in urls.py. Then, I will modify the 2 links from the 
home page that say “login” so that they redirect me to the login page.

I need to process the data from the login page into the login view(), so that I can check if that data’s available on 
the database. If the user exists, I will let the user log in into their account. Otherwise, I will show an error 
message.

I will redirect the user to the home page once they log in, and I will display their username. I think I will put the 
username in layout.html, since I want the username to be displayed in all of the website’s pages.

I don’t know if I will add the ability to logout in this part of the algorithm, or if I’ll create a new sub algorithm 
just add the ability to log out.
"""
def login_user(request):
    # This checks if the user has submitted the form in the login page
    if request.method == "POST":

        # This inserts the inputs into variables
        username = request.POST["username"]
        password = request.POST["password"]

        # This is a Django function that will let me check if the user exists in my database
        user = authenticate(request, username=username, password=password)

        # If the user exists, they will login and go to the home page
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        # If the user doesn't exist, they will get an error message
        else:
            return render(request, "login.html", {
                "error_message": "Error: Invalid username and/or password."
            })

    # This will render the page if the user hasn't submitted the form
    else:
        return render(request, "login.html")

""" I will add the ability for users to log out after they log in.

I need to create a new view() function to let logged in users to log out. I will also try to use the 
“is_authenticated” decorator so that only logged in users are able to see the log out link, and so only them are able 
to log out.

Source: https://cdn.cs50.net/web/2020/spring/projects/2/commerce.zip . If that link's unavailable,
try this link instead: https://cs50.harvard.edu/web/2020/projects/2/commerce/ .
"""
def logout_user(request):

    # This is a Django function that will log out the user who's logged in
    logout(request)

    # This will redirect the user to the home page
    return HttpResponseRedirect(reverse("index"))

""" I will add a link that says “Add Game”. If the user clicks on this link, they will be 
taken to a new page with a form that lets them enter the fields “title”, “store”, and 
“console”.

I will need to create a view() for the “Add Game” functionality. For the time being, the only thing that this function 
will do will be to redirect the user to a new html page that I need to create (I could call it “add.html”.) I will 
also need to add a "login required" decorator here in the add game view() so that this view() is only executed
if the user is logged in.

Then, I would need to add that view() as a URL in urls.py.

REMEMBER that I need to get the ID of the currently logged in user and insert that into the database when I insert a 
game so that game is inserted in the wish list of that particular user.

I will also use debugging code to print all of the games inserted into the database in the Add Game page to check
that the games are being properly being added to the database.

Now, I need to redirect the user to the home page after inserting a game into their wish list.

To print the games for the currently logged in user using Query Set syntax, I will use add 
".filter(user_id=id_of_logged_user)" to the end of the "Games.objects" snippet (source: Willem Van Onsem's reply from
https://stackoverflow.com/questions/56293211/get-values-from-a-specific-user-queryset-in-django .) I already stored 
the ID of the currently logged-in user in a variable called "logged_user_id".
"""
@login_required
def add_game(request):

    # This will store the Add Game form from forms.py
    form = AddGameForm()

    logged_user = request.user      # This stores the data from the currently logged in user
    logged_user_id = logged_user.id     # PK of the currently logged in user

    # This creates an instance of the User table, which I'll need to use in the Query Set syntax
    user_instance = User.objects.get(id=logged_user_id)

    # This will execute if the user submits the Add Game form
    if request.method == "POST":

        # This inserts the inputs inside of variables
        title = request.POST["title"]
        console = request.POST["console"]
        store = request.POST["store"]

        # This inserts the inputs into the database using the Query Set syntax
        game = Games(user_id=user_instance, title=title,
                               console=console, store=store)

        game.save()

        # This will send the user to the home page after adding a game
        return HttpResponseRedirect(reverse("index"))

    else:
        # DEBUGGING CODE: I will print all games for a specific user in the Add Game page
        return render(request, "add.html", {
            "form": form,
            "games": Games.objects.filter(user_id=logged_user.id)
        })

""" I will add a link to the edit page in urls.py, and create a view() function to allow the user edit their game on 
their wish list. I also need to create a new HTML file for the edit page (I could call it “edit.html”).

Remember that only logged in users should have access to this view() (as well as this page in general). So, I need to 
add a decorator on the edit view() to prevent the user from entering the edit page if they’re not logged in.

I will add a 2nd parameter, which will be the game's ID, which, in my case, it's a UUID. I will take that from
the URL, whci will have the form "game_uuid/edit". That's already configured on urls.py.

First, I need to get the specific game that I want to edit. To do that, I will use Query Set notation to get that game, 
and then I will insert that game into a variable. To obtain the game whose ID is the UUID in the URL of the edit page, 
that is, to obtain the game that was on the same row as the edit link that I clicked on, I need to use syntax like the 
following: “Games.objects.filter(id=variable_with_game_uuid)” . The variable that stores the current game0s UUID is 
the 2nd parameter of the Edit view().

After I fetch the proper game, I will use Jinja notation to send the title, console, and store of that game to 
pre-populate the from on the Edit page (which I have to create.)

For security reasons, I will also make sure that the game that I'm editing belongs to the current user. That 
way, another user whose logged in won't be able to edit a game that's not theirs (that is, to prevent hacking.)

Now, I need to check if the user has submitted the form on the Edit page. If the have, I will update the current game 
on the database (UPDATE, NOT INSERT.) I need to find out how to update an entry in a database using Query Set syntax.

The equivalent of SQL’s UPDATE in Query Set syntax is the update() function. To use it, I need to use syntax like the 
following: “Table.objects.filter(field=value).update(field_that_I_want_updated=updated_value)” (source: 
https://docs.djangoproject.com/en/4.0/topics/db/queries/#topics-db-queries-update .)
"""
@login_required
def edit(request, game_uuid):

    logged_user = request.user  # This stores the data from the currently logged in user
    logged_user_id = logged_user.id  # PK of the currently logged in user

    # This creates an instance of the User table, which I'll need to use in the Query Set syntax
    user_instance = User.objects.get(id=logged_user_id)

    # This grabs the game that I want to edit
    current_game = Games.objects.filter(id=game_uuid, user_id=logged_user_id)

    # Checking if the user submitted the Edit Page form
    if request.method == "POST":

        # This inserts the inputs inside of variables
        title = request.POST["title"]
        console = request.POST["console"]
        store = request.POST["store"]

        # This prepares the data to update the entry on the database
        updated_game = Games.objects.filter(id=game_uuid, user_id=logged_user_id).update(title=title,
                                   console=console, store=store)

        # With update(), I DON'T need to use save()
        # updated_game.save()

        # This will send the user to the home page after adding a game
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "edit.html", {
            "current_game": current_game
        })

""" First, I will redirect the user to a new page if they click on the “Delete” link. This will be the “Delete” page.

This is the standard procedure: I will create a new HTML file for this page, I will add a new link on urls.py, and 
I will create a new view() function. The new URL on the urls.py file will be similar than that of the edit page. That 
is, I will add the game’s UUID into the URL, and insert it into a <str:variable> tag in urls.py.

To delete the game, I need to look up the Query Set syntax to delete an entry from a database. Once I look that up, I 
will delete the game with the UUID that is the same as the UUID in the URL, and that belongs to the logged-in user.

I already stored the current game in a variable. Now, I just need to delete that game from the database.
	
I also need to check if the user hits the “submit” button from the Delete page before deleting that game. The request 
method of the form will be POST.

The Query Set syntax that I need for deleting a record in the database is “.delete()”, which needs to be written to 
the side of a Query Set query or of a variable that contains Query set syntax (source: Wolph’s reply from: 
https://stackoverflow.com/questions/3805958/how-to-delete-a-record-in-django-models .)

I will add the name of the game on the confirmation message so that it says “Would you like to delete NAME OF THE GAME 
from your wish list?”

I need to use Jinja notation for this. This is really similar to the code that I wrote for the Edit view(). I would 
need to send the variable with the current selected game to the Delete HTML page. Then, I would need to use a “for” 
loop, and then put the property “title” using Jinja.
"""
@login_required
def delete(request, game_uuid):

    logged_user = request.user  # This stores the data from the currently logged in user
    logged_user_id = logged_user.id  # PK of the currently logged in user

    # This grabs the game that I want to edit
    current_game = Games.objects.filter(id=game_uuid, user_id=logged_user_id)

    # Checking if the user pressed the "Submit" button
    if request.method == "POST":
        current_game.delete()   # This deletes the game

        # This will send the user to the home page
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "delete.html", {
            "current_game": current_game
        })

