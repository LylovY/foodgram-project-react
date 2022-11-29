from djoser.serializers import SetPasswordSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import Follow, User

from .fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            if Follow.objects.filter(user=user, author=obj).exists():
                return True
        return False


class UserPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomSetPasswordSerializer(SetPasswordSerializer):
    class Meta:
        fields = (
            'new_password',
            'current_password',
        )


class RecipesSubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscribeSerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            if Follow.objects.filter(user=user, author=obj).exists():
                return True
        return False

    def get_recipes(self, obj):
        recipes_limit = self.context.get('recipes_limit')
        if recipes_limit is not None:
            recipes_limit = int(self.context.get('recipes_limit'))
            queryset = Recipe.objects.filter(author=obj)[:recipes_limit]
        else:
            queryset = Recipe.objects.filter(author=obj)
        serializer = RecipesSubscribeSerializer(queryset, many=True)
        return serializer.data


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class TagPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeIngredientPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipesSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image = Base64ImageField(allow_null=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RecipeIngredientSerializer(
        source='recipes_ingredient',
        read_only=True,
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            if obj.favorited.filter(id=user.id).exists():
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            if obj.shopping_cart.filter(id=user.id).exists():
                return True
        return False


class RecipesPostSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientPostSerializer(
        source='recipes_ingredient',
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        ingredients = validated_data.pop('recipes_ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_note in ingredients:
            id = ingredient_note['ingredient'].get('id')
            amount = ingredient_note.get('amount')
            current_ingredient = Ingredient.objects.get(id=id)
            recipe.ingredients.add(
                current_ingredient, through_defaults={'amount': amount})
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        ingredients = validated_data.pop('recipes_ingredient')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        for ingredient_note in ingredients:
            id = ingredient_note['ingredient'].get('id')
            amount = ingredient_note.get('amount')
            current_ingredient = Ingredient.objects.get(id=id)
            instance.ingredients.add(
                current_ingredient, through_defaults={'amount': amount})
        instance.tags.set(tags)
        return instance
