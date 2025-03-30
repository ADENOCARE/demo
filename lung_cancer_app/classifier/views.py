from django.shortcuts import render
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import ImageUploadForm
import tensorflow as tf
import numpy as np
import cv2
import os

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

