from rest_framework import viewsets, request
from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User




# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raisexception = True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                    'token' : token.key,
                    },
            status=status.HTTP_400_BAD_REQUEST)



class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    # , is very important

    @action(methods=['POST'], detail=True)
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            meal = Meal.objects.get(id=pk)
            user = request.user
            user = request.data['username']
            stars = request.data['stars']
            user = User.object.get(user = user)

            try:
                # Update
                rating = Rating.objects.get(user=user.id, meal=meal.id)
                Rating.stars = stars
                Rating.save()
                serializer = RatingSerializer(Rating, many=False)
                json = {
                    'message' : 'Meal Rate Updated',
                    'result' : serializer.data,
                }
                return Response(json, status=status.HTTP_400_BAD_REQUEST)


            except:
                # Create if the rate not found
                rating = Rating.objects.create(stars=stars, meal=meal, user=user)
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message' : 'Meal Rate Updated',
                    'result' : serializer.data,
                }
                return Response(json, status=status.HTTP_200_OK)

        else:
            # Create
            json = {
                'message' : 'stars not found'
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)




class RatingViewSet(viewsets.ModelViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated)
    # Not anyone can rating

    def update(self, request, *args, **kwargs):
        response = {
            'message' : 'u cant rate',
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)