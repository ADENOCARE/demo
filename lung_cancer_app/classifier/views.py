from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Story
from .forms import StoryForm
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import ImageUploadForm
import tensorflow as tf
import numpy as np
import cv2
import os

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username:
            messages.error(request, "Username is required.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name.split()[0]  # Set first name
        user.last_name = " ".join(name.split()[1:])  # Set last name
        user.save()

        messages.success(request, "Registration successful. You can now log in.")
        return redirect("index")

    return render(request, "classifier/register.html")

def index(request):
    if request.method == "POST":
        username= request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")  # Redirect to a protected page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("index")

    return render(request, "classifier/index.html")

@login_required
def account_view(request):
    # Render the account management page
    return render(request, "classifier/account.html")

def logout_view(request):
    # Log out the user
    logout(request)
    return redirect("index")

@login_required
def home(request):
    return render(request, 'classifier/home.html')

def symptom_checker(request):
    return render(request, 'classifier/symptom_checker.html')


def community(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'classifier/community.html', {'stories': stories})

def share_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community')
    else:
        form = StoryForm()
    return render(request, 'classifier/share_story.html', {'form': form})


def classify_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            file_path = default_storage.save('temp_image.jpg', image)
            img_path = os.path.join(settings.MEDIA_ROOT, file_path)

            # Load and preprocess the image
            IMG_SIZE = 224
            img_array = cv2.imread(img_path)
            new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
            img_array = np.expand_dims(new_array, axis=0)  # Add batch dimension

            # Load the model
            model_path = os.path.join(settings.BASE_DIR, 'classifier/models/lung_cancer_vgg16.keras')
            model = tf.keras.models.load_model(model_path)

            # Make prediction
            prediction = np.argmax(model.predict(img_array), axis=-1)
            categories = ['lung_adenocarcinomas', 'lung_normal', 'lung_squamous_cell_carcinomas']
            result = categories[prediction[0]]

            os.remove(img_path) #remove the image after prediction

            return render(request, 'classifier/result.html', {'result': result})
    else:
        form = ImageUploadForm()
    return render(request, 'classifier/upload.html', {'form': form})

