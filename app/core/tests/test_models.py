from unittest.mock import patch

from recipe.models import Tag, Recipe, Ingredient, recipe_image_file_path
from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_user(email='test@psykweb.com', password='testpass123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModuleTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        sample_user = {'email': 'test@psykweb.com',
                       'password': 'Testpass123'}

        user = get_user_model().objects.create_user(**sample_user)

        self.assertEqual(user.email, sample_user['email'])
        self.assertTrue(user.check_password(sample_user['password']))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@psykweb.COM'

        user = sample_user(email)

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_is_mandatory(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@psykweb.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_str(self):
        """Test the User string representation"""
        email = 'test@psykweb.com'

        user = sample_user()

        self.assertEqual(str(user), email.lower())

    def test_tag_str(self):
        """Test the Tag string representation"""
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the Ingredient string representation"""
        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the Recipe string representation"""
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00,
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        file_path = recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)

    @patch('uuid.uuid4')
    def test_recipe_file_path_with_invalid_name(self, mock_uuid):
        """Test that invalid file name raises exception"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        payload = {'instance': None, 'filename': 'myimage'}
        self.assertRaises(ValueError, recipe_image_file_path, **payload)
