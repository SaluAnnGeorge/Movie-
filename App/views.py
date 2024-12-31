from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg
from django.contrib.auth.hashers import make_password, check_password
import re
from .models import Movie, Feedback1, Customer

# Index View: Display all movies with pagination
def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 3)  # Show 3 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})

# Movie Details View: Display details and handle ratings/reviews
def movie_details(request, id):
    movie = get_object_or_404(Movie, id=id)
    feedback_list = Feedback1.objects.filter(movie=movie).order_by('-created_at')
    average_rating = feedback_list.aggregate(average=Avg('rating'))['average'] if feedback_list.exists() else None

    if request.method == 'POST':
        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            review = request.POST.get('review')

            if rating and 1 <= int(rating) <= 5:
                Feedback1.objects.create(
                    movie=movie,
                    user=request.user,
                    rating=int(rating),
                    comment=review,
                )
                messages.success(request, 'Your rating and review have been submitted!')
                return redirect('movie_details', id=movie.id)
            else:
                messages.error(request, 'Invalid rating. Please select a value between 1 and 5.')
        else:
            messages.error(request, 'You must be logged in to submit a rating or review.')

    return render(request, 'movie_details.html', {
        'movie': movie,
        'feedback_list': feedback_list,
        'average_rating': average_rating,
    })
from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from .models import Customer

def register(request):
    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        contact_number = request.POST.get("contact_number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        print("Received POST request")  # Debugging line

        # Validate contact number
        if not re.fullmatch(r"^\d{10}$", contact_number):
            messages.error(request, "Contact number must be exactly 10 digits.")
            return redirect("register")

        # Validate password (ensure at least 1 uppercase letter and 1 special character)
        if not re.fullmatch(r"^(?=.*[A-Z])(?=.*[@$!%?&])[A-Za-z\d@$!%?&]{8,}$", password):
            messages.error(request, "Password must be at least 8 characters long, include 1 uppercase letter, and 1 special character.")
            return redirect("register")

        # Confirm passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect("register")

        # Create the user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password  # Django automatically hashes it
        )
        print("User created")  # Debugging line

        # Create the associated Customer instance
        Customer.objects.create(
            user=user,
            customer_name=customer_name,
            contact_number=contact_number,
            email=email,
            password=make_password(password)  # Optional; Django already hashes the password
        )
        print("Customer instance created")  # Debugging line

        # Success message and redirect to login
        messages.success(request, "Registration successful! You can now log in.")
        return redirect("login")

    return render(request, "register.html")


from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        

        # Use Django's authenticate function
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("index")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "login.html")


# Logout View
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")





# Create your views here.