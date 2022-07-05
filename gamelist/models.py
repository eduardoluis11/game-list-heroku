from django.contrib.auth.models import AbstractUser # This will let me use the "AbstractUser" tool
from django.db import models    # This will allow me to create models

# This will allow me to generate UUIDs
import uuid

""" To let users create their own accounts and for them to be able to log in, I need to create the required models 
to create the tables that will store the users’ credentials. Remember that Django already has some functions that 
allow me to create tables that store user credentials. Django also has some functions that allow me to authenticate 
users that have created their accounts. I will use those Django functions. 

This will allow me to easily create a table with all of the data that I may need to create a user, and store
their information on my database. LEAVE THIS CLASS as the first class, or I may get errors.
"""
class User(AbstractUser):
    pass

""" To insert data into a new table, I need to create the model for that new table, which in this case will be a table 
called “games”. That table will have the same fields and the same limitations (character limits) as the ones in the 
form in the Add Game Page. I would prefer to add default values for each of the Games table’s fields to avoid any error 
messages from Django.

Remember that I need to insert as well the ID for the currently logged in user, since each user will have their own
individual wish list.

I will add the "__str__" snippet to verify that, if I create a wish list, that the command-line prints two of the 
fields for a particular game. That way, I can verify in the command-line that games are being added. 

Instead of a standard ID using "autoincrement" (which generates me numbers from 1 and onwards,) I will use a UUID.
Since UUIDs are longer than standard IDs' I won't have the problem in which, if a user adds a game for the 1st time
and then wants to edit it, they wont see a "20/edit" in the URL (which would look weird, since they would 
expect something like "1/edit".) With UUIDs, they will see a long string of random characters, which looks more
natural than smaller numbers that don't start from 1. To generate UUIDs in Django, I will use this as a reference: 
https://docs.djangoproject.com/en/4.0/ref/models/fields/ ( this is where I took the 
"id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)" snippet .)

I will have to redo the database. I want to insert an additional field into the Games table. I want to insert “UUID” 
as a new field. I will generate a UUID, and then give one to each game. That way, when I need to edit games, I can 
simple go to “/UUID_of_game/edit” to edit that particular game (I will fetch that UUID to see to which game it belongs 
to, and then update that game on the database once the user clicks on “Submit”. )
"""
class Games(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_of_games", default=0)
    title = models.CharField(max_length=255, default='')
    console = models.CharField(max_length=64, default='')
    store = models.CharField(max_length=64, default='')

    def __str__(self):
        return f"{self.id}: {self.user_id} to {self.store}"



