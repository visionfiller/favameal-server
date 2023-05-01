from django.db import models
from django.contrib.auth.models import User

class Meal(models.Model):
    """Meal Model
    """
    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    favorites = models.ManyToManyField(User, through="FavoriteMeal")
    # TODO: establish a many-to-many relationship with User through the join model
    @property
    def is_favorite(self):
        return self.__is_favorite
    # TODO: Add a `is_favorite` custom property. Remember each JSON representation of a restaurant should have a `is_favorite` property. Not just the ones where the value is `true`.
    @is_favorite.setter
    def is_favorite(self, value):
        self.__is_favorite = value

    @property
    def user_rating(self):
        return self.__user_rating
    @user_rating.setter
    def user_rating(self, value):
        self.__user_rating = value
    @property
    def avg_rating(self):
        return self.__avg_rating
    @avg_rating.setter
    def avg_rating(self, value):
        self.__avg_rating = value
    # TODO: Establish a many-to-many relationship with User through the appropriate join model

    # TODO: Add an user_rating custom properties

    # TODO: Add an avg_rating custom properties
