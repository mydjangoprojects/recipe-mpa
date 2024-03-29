from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from recipe.models import Tag

TAG_LIST_URL = reverse('recipe:tag_list')


def crud_url_by_action_and_pk(action, pk=1):
    """Return Tag URL by Action and PK"""
    return reverse(f'recipe:tag_{action}', args=[pk])


class PublicTagViewsTests(TestCase):
    """Tests for publicly accessed Tag's Views."""
    def setUp(self):
        self.client = Client()

    def test_tag_list_redirects_unauthenticated(self):
        """Test that Tag List view redirects unauthenticated users."""
        response = self.client.get(TAG_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_tag_detail_redirects_unauthenticated(self):
        """Test that Tag Detail view redirects unauthenticated users."""
        url = crud_url_by_action_and_pk('detail')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_tag_update_redirects_unauthenticated(self):
        """Test that Tag Update view redirects unauthenticated users."""
        url = crud_url_by_action_and_pk('update')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_tag_delete_redirects_unauthenticated(self):
        """Test that Tag Delete view redirects unauthenticated users."""
        url = crud_url_by_action_and_pk('delete')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


class PrivateTagViewsTests(TestCase):
    """Test the authorized user Tags Views"""

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            'test@domain.com',
            'testpass1'
        )
        self.client.force_login(self.user)

        self.tag = Tag.objects.create(name='First Tag', user=self.user)

    def login_as_superuser(self):
        """Utility function to login as superuser"""
        self.superuser = get_user_model().objects.create_superuser(
            'superuser@domain.com',
            'testpass1'
        )
        self.client.force_login(self.superuser)

    def login_as_another_user(self):
        """Utility function to login as another user.
           Which isn't the creator of the Tag"""
        self.another_user = get_user_model().objects.create_user(
            'another_user@domain.com',
            'testpass1'
        )
        self.client.force_login(self.another_user)

    def test_tag_list_GET(self):
        """Test retrieving List of Tags."""
        response = self.client.get(TAG_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'tag/tag_list.html')

    def test_tag_detail_GET(self):
        """Test retrieving Detail of Tag."""
        url = crud_url_by_action_and_pk('detail', self.tag.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'tag/tag_detail.html')

    def test_tag_update_GET(self):
        """Test retrieving Update of Tag."""
        url = crud_url_by_action_and_pk('update', self.tag.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'tag/tag_update.html')

    def test_tag_delete_GET(self):
        """Test retrieving Delete of Tag."""
        url = crud_url_by_action_and_pk('delete', self.tag.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'tag/tag_delete.html')

    def test_tag_update_GET_forbidden_for_another_user(self):
        """Test retrieving Update of Tag is forbidden.
           For user which isn't the creator of the Tag."""
        self.login_as_another_user()

        url = crud_url_by_action_and_pk('update', self.tag.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_delete_GET_forbidden_for_another_user(self):
        """Test retrieving Delete of Tag is forbidden.
           For user which isn't the creator of the Tag."""
        self.login_as_another_user()

        url = crud_url_by_action_and_pk('delete', self.tag.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_update_GET_always_accessible_for_superuser(self):
        """Test retrieving Update of Tag is always accessible for superuser."""
        self.login_as_superuser()

        url = crud_url_by_action_and_pk('update', self.tag.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'tag/tag_update.html')

    def test_tag_delete_GET_always_accessible_for_superuser(self):
        """Test retrieving Delete of Tag is accessible always for superuser."""
        self.login_as_superuser()

        url = crud_url_by_action_and_pk('delete', self.tag.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'tag/tag_delete.html')
