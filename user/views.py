from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.views import View

from reservation.models import Comment, Reservation
from user.models import Account, Patient, OtpToken

from .forms import RegisterForm, SigninForm, ProfileForm
from .models import Doctor


class SignupView(View):
    form_class = RegisterForm
    template_name = 'user/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = Account.objects.create_user(
                cd['email'],
                cd['username'],
            )
            Patient.objects.create(account=user)
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.gender = cd['gender']
            user.set_password(cd['password1'])
            user.save()
            messages.success(
                request,
                "حساب کاربری با موفقیت ایجاد شد. پس از تأیید ایمیل، امکان ورود به سایت را خواهید داشت.",
                "success",
            )

            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            subject = '[Doctorex] رمز یکبار مصرف'
            message = f'''
                                                        {user.first_name} عزیز، سلام
                                                        رمز یکبار مصرف شما برای تأیید ایمیل: {otp.otp_code}
                                                        این رمز تا 5 دقیقه اعتبار دارد.
                                                        از طریق لینک زیر می توانید به فرم ورود رمز یکبار مصرف مراجعه کنید:
                                                        http://127.0.0.1:8000/account/verify-email/{user.username}
                                        '''
            sender = 'dctrxspprt@gmail.com'
            receiver = [user.email, ]

            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )
            return redirect('account:verify-email', username=user.username)
        return render(request, self.template_name, {"form": form})


class SigninView(View):
    form_class = SigninForm
    template_name = 'user/signin.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_email = cd['email']
            if (Account.objects.filter(email=user_email).exists()
                    and not Account.objects.get(email=user_email).is_active):
                messages.warning(
                    request,
                    'حساب کاربری فعال نیست. جهت فعالسازی، ایمیل خود را وارد کنید.',
                    'warning')
                return redirect('account:resend-otp')
            user = authenticate(request, username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید!', 'success')
                return redirect('index')
            messages.error(request, 'نام کاربری یا کلمه عبور اشتباه است.', 'warning')
        return render(request, self.template_name, {"form": form})


class SignoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'به امید دیدار مجدد', 'success')
        return redirect('index')


class VerifyEmailView(View):
    template_name = 'user/verify_token.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, username):
        if not Account.objects.filter(username=username).exists():
            return redirect('index')
        elif Account.objects.get(username=username).is_active:
            return redirect('account:signin')
        return render(request, self.template_name)

    def post(self, request, username):
        user = Account.objects.get(username=username)
        user_otp = OtpToken.objects.filter(user=user).last()
        if user_otp.otp_code == request.POST['otp_code']:
            if user_otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                messages.success(request, 'حساب کاربری با موفقیت فعالسازی شد', 'success')
                return redirect('account:signin')
            else:
                messages.warning(request, 'رمز یکبار مصرف منقضی شده است. لطفا مجدداً درخواست رمز یکبار مصرف را ارسال نمایید.', 'warning')
                return redirect('account:verify-email', username=user.username)
        else:
            messages.warning(request, 'رمز وارد شده صحیح نیست. لطفا مجدداً تلاش کنید.', 'warning')
            return redirect('account:verify-email', username=user.username)


class ResendOtpView(View):
    template_name = 'user/resend_otp.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user_email = request.POST['otp_email']

        if Account.objects.filter(email=user_email).exists():
            user = Account.objects.get(email=user_email)
            if not user.is_active:
                if not user.otp_tokens.exists() or user.otp_tokens.last().otp_expires_at < timezone.now():
                    otp = OtpToken.objects.create(
                        user=user,
                        otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)
                    )
                    subject = '[Doctorex] رمز یکبار مصرف'
                    message = f'''
                                            {user.first_name} عزیز، سلام
                                            رمز یکبار مصرف شما برای تأیید ایمیل: {otp.otp_code}
                                            این رمز تا 5 دقیقه اعتبار دارد.
                                            از طریق لینک زیر می توانید به فرم ورود رمز یکبار مصرف مراجعه کنید:
                                            http://127.0.0.1:8000/account/verify-email/{user.username}
                            '''
                    sender = 'dctrxspprt@gmail.com'
                    receiver = [user.email, ]

                    send_mail(
                        subject,
                        message,
                        sender,
                        receiver,
                        fail_silently=False,
                    )

                    messages.success(
                        request,
                        'رمز یکبار مصرف با موفقیت ارسال شد.',
                        'success'
                    )
                    return redirect('account:verify-email', username=user.username)
                else:
                    messages.warning(
                        request,
                        'رمز یکبار مصرف ارسال شده همچنان معتبر است',
                        'warning'
                    )
                    return redirect('account:verify-email', username=user.username)
            else:
                messages.success(
                    request,
                    'ایمیل شما پیش از این تأیید شده و می توانید به حساب کاربری خود وارد شوید',
                    'success'
                )
                return redirect('account:signin')
        else:
            messages.warning(
                request,
                'حساب کاربری با این ایمیل یافت نشد. لطفاً ثبت نام کنید',
                'warning'
            )
            return redirect('account:signup')


class DoctorListView(View):
    def get(self, request):
        from time import sleep

        sleep(2)
        doctors = Doctor.objects.all().select_related("account", "specialty")
        context = {
            "doctors": doctors,
        }

        return render(
            request=request,
            template_name="user/partial/_doctors-list.html",
            context=context,
        )


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user = request.user
        form = ProfileForm(instance=user)
        comments = Comment.objects.filter(author=user)

        return render(request, "user/profile.html", {"form": form, "comments": comments})

    def post(self, request):
        user = request.user
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        comments = Comment.objects.filter(author=user)
        return render(request, "user/profile.html", {"form": form, "comments": comments})


class ProfileVisitHistory(View):
    def get(self, request):
        user = request.user
        try:
            patient = Patient.objects.get(account=user)
            reservations = Reservation.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            reservations = None
        return render(request, "user/visit_history.html", {"reservations":reservations})


class ProfileCommentView(View):
    def get(self, request):
        user = request.user
        comments = Comment.objects.filter(author=user)
        return render(request, "user/comments.html", {"comments": comments})


def redirect_view(request):
    response = redirect('account:profile')
    return response