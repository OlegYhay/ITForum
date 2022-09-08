from datetime import datetime

from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from forumBase.models import Topic, Forum, Category, CommentTopic
from user.models import CustomUser


class TestHomePage(TestCase):
    def setUp(self):
        self.Category = Category.objects.create(
            name='Python',
            forum=Forum.objects.create(
                name='Программирование'
            )
        )
        self.User = CustomUser.objects.create(
            email='jadk.fre@mail.ru',
            username='OlegYhay',
            password='123',
        )

        self.Topic1 = Topic.objects.create(
            name='Как вывести данные python в командную строку?',
            CategoryId=self.Category,
            Creator=self.User,
            DateOfCreation=datetime.now(),
            Description='Как вывести то?',
            status=1,
        )

        self.comment1 = CommentTopic(
            Topic=self.Topic1,
            User=self.User,
            CommentText='Ну я даже не знаю!',
            DateOfComment=datetime.now(),
        )

    def test_home(self):
        client = self.client
        result = client.get(reverse('home'))
        self.assertEqual(result.status_code, 200)

    def test_get_category_topics(self):
        client = self.client
        url = reverse('category', kwargs={'pk': self.Category.pk, })
        result = client.get(url)
        self.assertEqual(result.status_code, 200)
        self.assertContains(result, 'Как вывести данные python в командную строку?')
        self.assertContains(result, self.Category)

    def test_get_topic_detail(self):
        client = self.client
        url = reverse('topic', kwargs={'group': self.Category.pk, 'pk': self.Topic1.id})
        result = client.get(url)
        self.assertEqual(result.status_code, 200)
        self.assertContains(result,'Как вывести данные python в командную строку?')
        self.assertTemplateUsed('pages/Topic.html')
        print(result)