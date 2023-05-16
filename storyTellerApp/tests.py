import datetime
from urllib.parse import unquote
import uuid
from django.db import IntegrityError
from django.test import TestCase, Client
from django.urls import reverse
from .models import Follower, Like, Story, Tag, Location, Comment
from .models import Profile
from .forms import StoryForm
from django.contrib.auth.models import User
# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username= 'testuser',
            email ='testuser@gmail.com',
            password = "1234",
        )

    def test_userprofile_string_representation(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_account_creation(self):
        self.assertIsInstance(self.user, User)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(self.user.is_active, True)

    
    def test_user_username_uniqueness(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username= 'testuser',
                email ='regular@gmail.com',
                password = "1234",
            )

#home_page
class HomePageTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Create test profiles
        self.profile1 = Profile.objects.create(user=self.user1, id_user=105, username='user1', email='user1@gmail.com' )
        self.profile2 = Profile.objects.create(user=self.user2, id_user=106, username='user2',  email='user2@gmail.com')

        # Create test followers
        Follower.objects.create(user=self.user1.username, follower=self.user2.username)

        # Create test stories
        self.story1 = Story.objects.create(user=self.user1, content='Story 1')
        self.story2 = Story.objects.create(user=self.user2, content='Story 2')

        self.client.login(username='user1', password='password1')

    def test_home_page(self):
        
        response = self.client.get(reverse('home_page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'storyTellerApp/home.html')

        # Check if latest stories are present in the context
        self.assertIn('stories', response.context)
        latest_stories = response.context['stories']
        self.assertListEqual(list(latest_stories), [self.story2, self.story1])  # Ensure correct ordering

        # Check if followed stories are present in the context
        self.assertIn('followed_stories', response.context)
        followed_stories = response.context['followed_stories']
        self.assertListEqual(list(followed_stories), [])  # Only user2's story should be present

    def tearDown(self):
        # Clean up created objects
        User.objects.all().delete()
        Profile.objects.all().delete()
        Story.objects.all().delete()
        Follower.objects.all().delete()

#stories
class StoriesPageTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user5', password='password1')
        self.profile1 = Profile.objects.create(user=self.user1, id_user=105, username='user5', email='user5@gmail.com')
        # Create test stories
        self.story=Story.objects.create(content='Story 1', user=self.user1)
        self.client.login(username='user5', password='password1')

    def test_stories_page(self):
        
        # Convert the UUID to a string
        response = self.client.get(reverse('stories_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'storyTellerApp/stories.html')
        
        all_stories = response.context['all_stories']
        
        self.assertEqual(list(all_stories), list(Story.objects.all().order_by("-created_at")))

#my_stories
class MyStoriesViewTest(TestCase):
    def setUp(self):
        # Create a user and profile for testing
        self.username = 'testuser6'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
    def test_mystories_view(self):
        # Log in the user
        self.client.login(username=self.username, password=self.password)
         # Create a test story associated with the user's profile
        self.story = Story.objects.create(user=self.user, content='This is a test story')
        # Make a GET request to the mystories view
        response = self.client.get(reverse('mystories'))
        
        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the rendered context contains the test story
        self.assertTemplateUsed(response, 'storyTellerApp/mystories.html')
        
        # Assert that the rendered context contains only the user's stories
        self.assertEqual(list(response.context['my_stories']), [self.story])

#view_story
class ViewStoryViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        
    def test_view_story_view(self):
        self.client.login(username=self.username, password=self.password)
        story = Story.objects.create(user=self.user, title='Test Story', content='This is a test story')
        tag = Tag.objects.create(name='Test Tag')
        location = Location.objects.create(name='Test Location')
        story.tags.add(tag)
        story.locations.add(location)
        
        response = self.client.get(reverse('view_story', args=[story.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'storyTellerApp/story.html')
        self.assertEqual(response.context['story'], story)
        self.assertEqual(list(response.context['story_tags']), [tag])
        self.assertEqual(list(response.context['story_locations']), [location])
        
        self.assertContains(response, story.title)
        self.assertContains(response, story.content)
        self.assertContains(response, tag.name)
        self.assertContains(response, location.name)

#delete_story
class DeleteStoryViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        self.story = Story.objects.create(user=self.user, title='Test Story', content='This is a test story 2')
        
    def test_delete_story_view_post(self):
        self.client.login(username=self.username, password=self.password)
        initial_story_count = Story.objects.count()
        
        response = self.client.post(reverse('deletestory'), {'story': self.story.id})
        
        self.assertRedirects(response, reverse('home_page'))
        self.assertEqual(Story.objects.count(), initial_story_count - 1)
        self.assertFalse(Story.objects.filter(id=self.story.id).exists())
        
    def test_delete_story_view_get(self):
        self.client.login(username=self.username, password=self.password)
        initial_story_count = Story.objects.count()
        
        response = self.client.get(reverse('deletestory'))
        
        self.assertRedirects(response, reverse('home_page'))
        self.assertEqual(Story.objects.count(), initial_story_count)

#add comment
class AddCommentViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser9'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        self.story = Story.objects.create(user=self.user, title='Test Story', content='This is a test story 5')
        self.client = Client()

    def test_add_comment_view_post(self):
        self.client.login(username=self.username, password=self.password)
        
        initial_comment_count = Comment.objects.count()

        response = self.client.post(reverse('addcomment'), {
            'story': self.story,
            'storyid':self.story.id,
            'user': self.user.username,
            'comment': 'This is a test comment'
        })

        self.assertRedirects(response, reverse('view_story', args=[self.story.id]))
        self.assertEqual(Comment.objects.count(), initial_comment_count + 1)
        self.assertTrue(Comment.objects.filter(content='This is a test comment').exists())

    def test_add_comment_view_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('view_story', args=[self.story.id]))
        self.assertEqual(response.status_code, 200)

#add_story
class AddStoryTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('addstory')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
    
    def test_add_story(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'storyTellerApp/addstory.html')
        self.assertIsInstance(response.context['form'], StoryForm)
        
        data = {
            'title': 'Test Story',
            'content': 'This is a test story',
            'tags': 'tag1, tag2',
            'coordinatessearch': '40.7128, -74.0060',
            'address': 'New York City',
            'exact_date': '2023-05-16',
            'session': 'fall',
            'decade': "2020's",
            'year': '2023',
            'month': 'May',
            'date-range-start': '2023-05-01',
            'date-range-end': '2023-05-31',
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        
        # Verify the story was created
        self.assertEqual(Story.objects.count(), 1)
        story = Story.objects.first()
        self.assertEqual(story.user, self.user)
        self.assertEqual(story.title, 'Test Story')
        self.assertEqual(story.content, 'This is a test story')
        self.assertEqual(story.date_format, 1)
        self.assertEqual(story.session, 'fall')
        self.assertEqual(story.decade, "2020's")
        self.assertEqual(story.year, '2023')
        self.assertEqual(story.month, 'May')
        self.assertEqual(story.date_range_start, '2023-05-01')
        self.assertEqual(story.date_range_end, '2023-05-31')

        expected_date = datetime.datetime.strptime('2023-05-16', '%Y-%m-%d').date()
        self.assertEqual(story.date_exact, expected_date)
        
        # Verify the tags were created and associated with the story
        self.assertEqual(Tag.objects.count(), 2)
        self.assertListEqual(list(story.tags.values_list('name', flat=True)), ['tag1', 'tag2'])
        
        # Verify the locations were created and associated with the story
        self.assertEqual(Location.objects.count(), 1)
        self.assertListEqual(list(story.locations.values_list('name', flat=True)), ['New York City'])


#search
class SearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search')  # Replace 'search' with your actual URL name
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, id_user= 100)
    
    def test_search(self):
        # Create test data
        story = Story.objects.create(user=self.user, title='Test Story')
        
        data = {
            'search': 'Test Story',
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'storyTellerApp/search.html')
        
        # Verify the context data
        self.assertEqual(response.context['user_profile'], self.profile)
        self.assertListEqual(list(response.context['story_title_object']), [story])
        self.assertListEqual(list(response.context['story_tag_object']), [])
        self.assertListEqual(list(response.context['story_location_object']), [])
        self.assertListEqual(list(response.context['story_user_object']), [])
        self.assertListEqual(list(response.context['story_session_object']), [])
        self.assertListEqual(list(response.context['story_decade_object']), [])
        self.assertListEqual(list(response.context['story_exact_date_object']), [])
        self.assertListEqual(list(response.context['story_month_object']), [])
        self.assertListEqual(list(response.context['story_year_object']), [])

#like_story

class LikeStoryViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser9'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user, id_user=self.user.id)
        self.story = Story.objects.create(user=self.user, title='Test Story', content='This is a test story')
        self.client = Client()

    def test_like_story_authenticated_user(self):
        self.client.login(username=self.username, password=self.password)
        initial_like_count = Like.objects.count()

        response = self.client.get(reverse('like_story'), {'story_id': self.story.id})

        self.assertRedirects(response, reverse('view_story', args=[self.story.id]))
        self.assertEqual(Like.objects.count(), initial_like_count + 1)
        self.assertTrue(Like.objects.filter(story_id=self.story.id, username=self.username).exists())


     
