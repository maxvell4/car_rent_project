from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.views import (LoginView,
                                        PasswordResetView,
                                        PasswordChangeView,
                                        PasswordResetConfirmView)
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from rent.models import Driver, Car, Manufacturer
from rent.forms import (RegistrationForm,
                        UserLoginForm,
                        UserPasswordResetForm,
                        UserSetPasswordForm,
                        UserPasswordChangeForm,
                        BookingForm)


class IndexView(View):

    def get(self, request):
        num_drivers = Driver.objects.count()
        num_cars = Car.objects.count()
        num_manufacturers = Manufacturer.objects.count()
        cars = Car.objects.all().order_by('id')

        paginator = Paginator(cars, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        num_visits = request.session.get("num_visits", 0)
        request.session["num_visits"] = num_visits + 1

        context = {
            "num_drivers": num_drivers,
            "num_cars": num_cars,
            "num_manufacturers": num_manufacturers,
            "num_visits": num_visits + 1,
            "cars": cars,
            "page_obj": page_obj,
        }

        return render(request, "pages/index.html", context=context)


class AboutUsView(View):
    def get(self, request):
        return render(request, 'pages/about-us.html')


class ContactUsView(View):
    def get(self, request):
        return render(request, 'pages/contact-us.html')


class RentCarView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        form = BookingForm()
        return render(request, 'rent/car_rent.html', {'form': form, 'car': car})

    def post(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.save()
            messages.success(request, f'Congratulations! You have booked {car.model}')
            return redirect('success')  # Adjust to your success URL

        return render(request, 'rent/car_rent.html', {'form': form, 'car': car})


class CarPhotoView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        inside_images = car.inside_images.all()
        return render(request, 'rent/car_detail.html', {'car': car, 'inside_images': inside_images})


class SuccessView(View):
    def get(self, request):
        return render(request, 'pages/index.html')


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'accounts/sign-up.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Account created successfully!")
            return redirect('/accounts/login')
        else:
            print("Registration failed!")

        context = {'form': form}
        return render(request, 'accounts/sign-up.html', context)


class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = UserLoginForm


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/accounts/login')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
