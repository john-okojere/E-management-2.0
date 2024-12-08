import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
import json
from .models import CustomUser
from .forms import UserRegistrationForm, UserUpdateForm

@login_required
def users(request):
    if not request.user.is_staff and request.user.role != 'it_manager':
        return HttpResponseForbidden("You do not have permission to create a user.")
    custom_user = CustomUser.objects.all().exclude(is_staff=True)
    form = UserRegistrationForm()
    return render(request, 'users/index.html', {'custom_user': custom_user, 'form':form})

# User registration view
@login_required
def add_user(request):
    if not request.user.is_staff and request.user.role != 'it_manager':
        return HttpResponseForbidden("You do not have permission to create a user.")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by = request.user
            form.save()
    return redirect('customusers')  # Redirect to the dashboard

def choose_section(request):
    user = request.user
    if user.role == 'Cashier':
        if user.section == 'arcade':
            return redirect('arcade_cashier')
        elif user.section.title() == 'Restaurant':
            return redirect('resturant_cashier')
        elif user.section.lower() == 'cosmetic_store':
            return redirect('beauty_cashier')
        elif user.section.lower() == 'salon':
            return redirect('salon_cashier')
        elif user.section.lower() == 'fashion':
            return redirect('fashion_cashier')
        elif user.section.lower() == 'lounge':
            return redirect('lounge_cashier')
        elif user.section.lower() == 'spa':
            return redirect('spa_cashier')
    elif user.role == "Manager":
        if user.section == 'arcade':
            return redirect('arcade_manager')
        # elif user.section.title() == 'Restaurant':
        #     return redirect('resturant_manager')
        elif user.section.lower() == 'cosmetic_store':
            return redirect('beauty_manager')
        # elif user.section.lower() == 'salon':
        #     return redirect('salon_manager')
        # elif user.section.lower() == 'fashion':
        #     return redirect('fashion_manager')
        # elif user.section.lower() == 'lounge':
        #     return redirect('lounge_manager')
        # elif user.section.lower() == 'spa':
        #     return redirect('spa_manager')

    return redirect('dashboard')

# User login view
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.section)
            
            return redirect('face-auth')  # Redirect to the dashboard
        else:
            return render(request, 'users/signin-2.html', {'error': 'Invalid credentials'})
    return render(request, 'users/signin-2.html')

# User logout view
def logout_user(request):
    logout(request)
    return redirect('login')  # Redirect to the login page

# User profile view
@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Reload the profile page
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'profile.html', {'form': form})

# Dashboard view
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

import cv2
import numpy as np
import face_recognition
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import base64

@login_required
def face_auth(request):
    if request.method == "POST":
        try:
            # Load the user's profile picture
            user = request.user
            if not user.avatar:
                return JsonResponse({'status': 'error', 'message': 'No profile picture found for the user.'})

            profile_picture_path = user.avatar.path

            # Load and preprocess the reference image
            reference_image = face_recognition.load_image_file(profile_picture_path)
            reference_encoding = face_recognition.face_encodings(reference_image)[0]

            # Decode the base64 image sent from the frontend
            data = request.POST.get('image')
            if not data:
                return JsonResponse({'status': 'error', 'message': 'No image provided.'})

            # Decode the base64 image to a numpy array
            image_data = base64.b64decode(data.split(',')[1])
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Convert the frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get encodings of the captured frame
            live_encodings = face_recognition.face_encodings(rgb_frame)
            if not live_encodings:
                return JsonResponse({'status': 'error', 'message': 'No face detected in the video frame.'})

            # Compare the reference encoding with the live encoding
            threshold = 0.4  # Stricter threshold
            match = face_recognition.compare_faces([reference_encoding], live_encodings[0], tolerance=threshold)
            distance = face_recognition.face_distance([reference_encoding], live_encodings[0])[0]

            if match[0] and distance < threshold:
                request.session['face_authenticated'] = True
                return JsonResponse({'status': 'success', 'message': 'Face verified successfully!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Face verification failed!', 'distance': distance})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'users/face-authentication.html')
