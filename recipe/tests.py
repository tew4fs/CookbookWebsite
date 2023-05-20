from django.test import TestCase
from recipe.models import Recipe


# Create your tests here.
class BreakfastRecipeTestCase(TestCase):
    def setUp(self):
        breakfast = Recipe.objects.create(
            food="Breakfast Food",
            food_type="breakfast",
            description="A Breakfast Food",
            cook_time=20,
            serves=1,
        )
        breakfast.ingredients.add("Ingredient 1")

    def testBreakfastRecipeWasAdded(self):
        Recipe.objects.filter(
            food="Breakfast Food",
            food_type="breakfast",
            description="A Breakfast Food",
            cook_time=20,
            serves=1,
        )
        self.assertEqual(2, 1)
