from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from unittest.mock import patch
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from .forms import RegisterForm, SigninForm
from .models import Patient, Account, OtpToken, Doctor, Specialty, VisitTime
from reservation.models import Reservation, Comment
from django.utils import timezone


class SignupViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('account:signup')
        self.User = get_user_model()

    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_signup_post_valid(self):
        valid_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password123',
            'gender': 'M'
        }
        response = self.client.post(self.signup_url, data=valid_data)
        self.assertEqual(response.status_code,  302)
        user = self.User.objects.get(email='testuser@example.com')
        self.assertTrue(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.gender, 'M')
        self.assertTrue(Patient.objects.filter(account=user).exists())
        self.assertRedirects(response, reverse('account:verify-email', kwargs={'username': user.username}))

        # Test email sending
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('رمز یکبار مصرف', mail.outbox[0].subject)

    def test_signup_post_invalid(self):
        invalid_data = {
            'email': 'invalidemail',
            'username': '',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'password123',
            'password2': 'password1234',  # Passwords do not match
            'gender': 'M'
        }
        response = self.client.post(self.signup_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')
        self.assertFalse(self.User.objects.filter(email='invalidemail').exists())
        self.assertIsInstance(response.context['form'], RegisterForm)
        self.assertTrue(response.context['form'].errors)

    def test_authenticated_user_redirects(self):
        user = self.User.objects.create_user(
            username='authuser',
            email='authuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            is_active=True,
        )
        self.client.login(username='authuser@example.com', password='password123')
        response = self.client.get(self.signup_url)
        self.assertRedirects(response, reverse('reservation:index'))


class SigninViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signin_url = reverse('account:signin')
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            is_active=True,
        )

    def test_signin_get(self):
        response = self.client.get(self.signin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signin.html')
        self.assertIsInstance(response.context['form'], SigninForm)

    def test_signin_post_valid(self):
        valid_data = {
            'email': 'testuser@example.com',
            'password': 'password123',
        }
        response = self.client.post(self.signin_url, data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('reservation:index'))
    def test_signin_post_invalid(self):
        invalid_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.signin_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signin.html')
        self.assertIn('نام کاربری یا کلمه عبور اشتباه است.', response.content.decode())



class SignoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.signout_url = reverse('account:signout')
        self.index_url = reverse('reservation:index')
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            is_active=True,
        )
        self.client.login(username='testuser@example.com', password='password123')

    def test_signout(self):
        response = self.client.get(self.signout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        self.assertFalse('_auth_user_id' in self.client.session)


class VerifyEmailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            is_active=False
        )
        self.otp = OtpToken.objects.create(
            user=self.user,
            otp_code='123456',
            otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
        )
        self.verify_email_url = reverse('account:verify-email', kwargs={'username': self.user.username})

    def test_verify_email_get(self):
        response = self.client.get(self.verify_email_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/verify_token.html')

    def test_verify_email_post_valid(self):
        valid_data = {
            'otp_code': '123456',
        }
        response = self.client.post(self.verify_email_url, data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:signin'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_verify_email_post_invalid(self):
        invalid_data = {
            'otp_code': '654321',
        }
        response = self.client.post(self.verify_email_url, data=invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.verify_email_url)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)


class DoctorListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.doctor_list_url = reverse('account:doctors-list')
        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, format='JPEG')
        image.seek(0)

        self.specialty = Specialty.objects.create(
            specialty='Cardiology',
            slug='cardiology',
            image=SimpleUploadedFile('test_image.jpg', image.getvalue())
        )

        self.account = Account.objects.create_user(
            email='doctor@example.com',
            username='doctor',
            first_name='Doc',
            last_name='Tor',
            password='password123',
            is_active=True,
            is_doctor=True,
        )

        self.doctor = Doctor.objects.create(
            account=self.account,
            specialty=self.specialty
        )

    def test_doctor_list_view(self):
        response = self.client.get(self.doctor_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/partial/_doctors-list.html')
        self.assertContains(response, 'Doc Tor')


class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.profile_url = reverse('account:profile')
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            username='user',
            first_name='First',
            last_name='Last',
            password='password123',
            is_active=True,
        )
        self.client.login(username='user@example.com', password='password123')

    def test_profile_view_get(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertContains(response, 'First Last')

    def test_profile_view_post(self):
        response = self.client.post(self.profile_url, {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'gender': 'M',
            'phone_number': '1234567890'
        })
        self.assertRedirects(response, self.profile_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_profile_view_post_invalid(self):
        invalid_data = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': 'testuser@example.com',
            'gender': 'M',
            'phone_number': '1234567890'
        }
        response = self.client.post(self.profile_url, data=invalid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertContains(response, 'This field is required.')


class ProfileVisitHistoryTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.visit_history_url = reverse('account:visit_history')
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            username='user',
            first_name='First',
            last_name='Last',
            password='password123',
            is_active=True,
        )
        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, format='JPEG')
        image.seek(0)
        self.patient = Patient.objects.create(account=self.user)
        self.visit_time = VisitTime.objects.create(
            doctor=Doctor.objects.create(
                account=Account.objects.create_user(
                    email='doctor@example.com',
                    username='doctor',
                    first_name='Doc',
                    last_name='Tor',
                    password='password123',
                    is_active=True,
                    is_doctor=True,
                ),
                specialty=Specialty.objects.create(
                    specialty='Cardiology',
                    slug='cardiology',
                    image=SimpleUploadedFile('test_image.jpg', image.getvalue())
            ),
            date='2024-07-20',
            start_time="09:00:00",
            end_time="10:00:00",
            is_reserved=True,
        ))
        self.reservation = Reservation.objects.create(
            patient=self.patient,
            visit_time=self.visit_time
        )
        self.client.login(username='user@example.com', password='password123')

    def test_profile_visit_history_view(self):
        response = self.client.get(self.visit_history_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/visit_history.html')
        self.assertContains(response, '9:00 AM - 10:00 AM')


class ProfileCommentViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.comments_url = reverse('account:comments')
        self.user = Account.objects.create_user(
            email='user@example.com',
            username='user',
            first_name='First',
            last_name='Last',
            password='Kia6382568668',
            gender="M",
            is_active=True,
        )

        image = BytesIO()
        Image.new('RGB', (100, 100)).save(image, format='JPEG')
        image.seek(0)

        self.specialty = Specialty.objects.create(
            specialty='Cardiology',
            slug='cardiology',
            image=SimpleUploadedFile('test_image.jpg', image.getvalue())
        )
        self.doctor_account = Account.objects.create_user(
            email='doctor@example.com',
            username='doctor',
            password='Kia6382568668',
            is_doctor=True,
        )
        self.doctor = Doctor.objects.create(
            account=self.doctor_account,
            specialty=self.specialty
        )
        self.visit_time = VisitTime.objects.create(
            doctor=self.doctor,
            date='2024-07-20',
            start_time="09:00:00",
            end_time="10:00:00",
            is_reserved=True,
        )
        self.patient = Patient.objects.create(account=self.user)
        self.reservation = Reservation.objects.create(
            patient=self.patient,
            visit_time=self.visit_time
        )
        self.comment = Comment.objects.create(
            author=self.user,
            score=5,
            title='Great Doctor',
            text='Very professional and friendly.',
            doctor=self.doctor,
            reservation=self.reservation
        )

        with patch('user.models.OtpToken.objects.filter') as mock_otp_filter:
            mock_otp_filter.return_value.last.return_value = None
            logged_in = self.client.login(username='user@example.com', password='Kia6382568668')
            print("Logged in:", logged_in)

    def test_profile_comment_view(self):
        response = self.client.get(self.comments_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/comments.html')
        self.assertContains(response, 'Great Doctor')