"""
 Test for blog API endpoints
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from core.models import BlogPost
from blog.serializers import BlogPostSerializer, BlogPostDetailSerializer


BLOGS_URL = reverse('blog:blogpost-list')


def detail_url(blog_id):
    """Create and return a blog post detail URL."""
    return reverse('blog:blogpost-detail', args=[blog_id])


def create_blog(user, **params):
    """Create and return a blog post."""
    defaults = {
        'title': 'Sample Blog Post',
        'content': 'This is a sample blog post content.',
        'is_published': True,
        'author': user,
    }
    defaults.update(params)

    blog_post = BlogPost.objects.create(**defaults)
    return blog_post


class PublicBlogAPITests(TestCase):
    """ Test for the Blog API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving blog posts """
        res = self.client.get(BLOGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBlogAPITests(TestCase):
    """ Test for the Authenticated user"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'testuser',
            'test1@example.com',
            'test12345'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrive_blog(self):
        """ Test retrieving blog posts """
        create_blog(user=self.user)
        create_blog(user=self.user)

        res = self.client.get(BLOGS_URL)

        blogs = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_blog_limited_to_user(self):
        """ Test that blog posts returned are for the authenticated user """
        other_user = get_user_model().objects.create_user(
            'otheruser',
            'ohter@example.com',
            'other12345'
            )
        create_blog(user=other_user)
        create_blog(user=self.user)
        res = self.client.get(BLOGS_URL)
        blogs = BlogPost.objects.filter(author=self.user).order_by(
            '-created_at'
        )
        serializer = BlogPostSerializer(blogs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_blog_detail(self):
        """ Test getting blog post detail """
        blog = create_blog(user=self.user)
        url = detail_url(blog.id)
        res = self.client.get(url)
        serializer = BlogPostDetailSerializer(blog)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        payload = {
            'title': 'New Blog Post',
            'content': 'This is the content of the new blog post.',
            'is_published': True,
            'author': self.user.id,
        }
        res = self.client.post(BLOGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        blog = BlogPost.objects.get(id=res.data['id'])
        serializer = BlogPostDetailSerializer(blog, many=False)
        self.assertEqual(res.data, serializer.data)
