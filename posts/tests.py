from django.test import TestCase, Client
from django.urls import reverse
from .models import Post, Category
from django.contrib.auth.models import User


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Test Category", slug='test-category')
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            author=self.user,
            category=self.category,
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.slug, "test-post")
        self.assertEqual(self.post.content, "This is a test post.")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.category.name, "Test Category")


class PostListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Test Category", slug='test-category')
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            author=self.user,
            category=self.category,
        )

    def test_post_list_view(self):
        response = self.client.get(reverse("posts:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "posts/post_list.html")


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Test Category", slug='test-category')
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post.",
            author=self.user,
            category=self.category,
        )

    def test_post_detail_view(self):
        response = self.client.get(reverse("posts:post_detail", kwargs={"post_slug": self.post.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertContains(response, "This is a test post.")
        self.assertTemplateUsed(response, "posts/post_detail.html")


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login(self):
        response = self.client.post(reverse("posts:user_login"), {"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/"))

    def test_register(self):
        response = self.client.post(reverse("posts:user_register"), {
            "username": "newuser",
            "password1": "newuserpassword",
            "password2": "newuserpassword",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())