"""View module for handling requests about meals"""
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from favamealapi.models import Meal, MealRating, Restaurant, FavoriteMeal
from favamealapi.views.restaurant import RestaurantSerializer


class MealSerializer(serializers.ModelSerializer):
    """JSON serializer for meals"""
    restaurant = RestaurantSerializer(many=False)

    class Meta:
        model = Meal
        # TODO: Add 'user_rating', 'avg_rating', 'is_favorite' fields to MealSerializer
        fields = ('id', 'name', 'restaurant', 'favorites', 'is_favorite', 'mealrating', 'user_rating', 'avg_rating')



class MealView(ViewSet):
    """ViewSet for handling meal requests"""

    def create(self, request):
        """Handle POST operations for meals

        Returns:
            Response -- JSON serialized meal instance
        """
        try:
            meal = Meal.objects.create(
                name=request.data["name"],
                restaurant=Restaurant.objects.get(
                    pk=request.data["restaurant_id"])
            )
            serializer = MealSerializer(meal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single meal

        Returns:
            Response -- JSON serialized meal instance
        """
        try:
            meal = Meal.objects.get(pk=pk)

            # TODO: Get the rating for current user and assign to `user_rating` property
            rating_object = MealRating.objects.get(user=request.auth.user, meal=meal)
            meal.user_rating=rating_object.rating
            # TODO: Get the average rating for requested meal and assign to `avg_rating` property

            # TODO: Assign a value to the `is_favorite` property of requested meal
            meal.is_favorite = request.auth.user in meal.favorites.all()
            serializer = MealSerializer(meal)
            return Response(serializer.data)
        except Meal.DoesNotExist as ex:
            return Response({"reason": ex.message}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to meals resource

        Returns:
            Response -- JSON serialized list of meals
        """
        meals = Meal.objects.all()

        # TODO: Get the rating for current user and assign to `user_rating` property

        # TODO: Get the average rating for each meal and assign to `avg_rating` property

        # TODO: Assign a value to the `is_favorite` property of each meal
        for meal in meals:
                meal.is_favorite = request.auth.user in meal.favorites.all()
                rating_object = MealRating.objects.get(user=request.auth.user, meal=meal)
                meal.user_rating=rating_object.rating
                all_ratings = MealRating.objects.all()
                total_rating = 0
                for rating in all_ratings:
                    total_rating += rating.rating 
                meal.avg_rating = total_rating/len(all_ratings)
               

        serializer = MealSerializer(meals, many=True)

        return Response(serializer.data)

    # TODO: Add a custom action named `rate` that will allow a client to send a
    #  POST and a PUT request to /meals/3/rate with a body of..
    #       {
    #           "rating": 3
    #       }
    # If the request is a PUT request, then the method should update the user's rating instead of creating a new one

    # TODO: Add a custom action named `favorite` that will allow a client to send a
    #  POST request to /meals/3/favorite and add the meal as a favorite

    # TODO: Add a custom action named `unfavorite` that will allow a client to send a
    # DELETE request to /meals/3/unfavorite and remove the meal as a favorite
    @action(methods=['post'], detail=True)
    def favorite(self, request, pk):
        """Post request for a user to sign up for an event"""
    
       
        meal = Meal.objects.get(pk=pk)
        meal.favorites.add(request.auth.user)
        return Response({'message': 'Meal favorited'}, status=status.HTTP_201_CREATED)
    @action(methods=['delete'], detail=True)
    def unfavorite(self, request, pk):
        """Post request for a user to sign up for an event"""
    
        meal = Meal.objects.get(pk=pk)
        meal.favorites.remove(request.auth.user)
        return Response({'message': 'Restaurant unfavorited'}, status=status.HTTP_204_NO_CONTENT) 
    @action(methods=['post'], detail=True)
    def rate(self, request, pk):
        """Post request for a user to sign up for an event"""
        meal = Meal.objects.get(pk=pk)
        rating_value = request.data.get('rating')
        rating = MealRating.objects.create(user=request.auth.user, meal=meal, rating=rating_value)
        
        return Response({'message': 'Meal rated'}, status=status.HTTP_201_CREATED)
    @action(methods=['put'], detail=True)
    def rate(self, request, pk):
        """Post request for a user to sign up for an event"""
        meal = Meal.objects.get(pk=pk)
        mealrating = MealRating.objects.get(user=request.auth.user, meal=meal)
        mealrating.rating = request.data.get('rating')
        mealrating.save()
        return Response({'message': 'Meal rated'}, status=status.HTTP_204_NO_CONTENT)