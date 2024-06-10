from django.test import TestCase
from .models import Post
from django.contrib.auth import get_user_model
from django.urls import reverse
# from django.shortcuts import get_object_or_404

# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            password="secret"
        )
        
        cls.post = Post.objects.create(
            title="a good title",
            content="a good content",
            author=cls.user
        )
        
    def test_post_model(self):
        self.assertEqual(self.post.title, "a good title")
        self.assertEqual(self.post.content, "a good content")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "a good title")
        
    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get('/detail/1')
        self.assertEqual(response.status_code, 200)
        
    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "a good content")
        self.assertTemplateUsed(response, "index.html")
        
    # def test_post_detailview(self):
    #     # post = get_object_or_404(Post, id=id)
    #     response = self.client.get(reverse('detail', args=[self.post.pk]))
    #     no_response = self.client.get('/detail/10000')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(no_response.status_code, 404)
    #     self.assertContains(response, "a good title")
    #     self.assertTemplateUsed(response, "detail.html")
        
        
        
        
        
