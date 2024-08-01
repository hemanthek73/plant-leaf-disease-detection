
# import os
# import numpy as np
# from flask import Flask, request, render_template,render_template_string
# from werkzeug.utils import secure_filename
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array

# app = Flask(__name__)

# # Load the pre-trained model
# model = load_model('model.h5')
# print('Model loaded. Check http://127.0.0.1:5000/')

# # Define the labels
# # labels = {0: 'Healthy', 1: 'Powdery(order Erysiphales)', 2: 'Rust(Puccinia triticina)'}
# labels = {
#     0: {'label': 'Healthy', 'description': 'The plant is healthy.', 'prevention': ''},
#     1: {'label': 'Powdery mildew (order Erysiphales)', 'description': 'Powdery mildew is a fungal disease that affects a wide range of plants. It is characterized by white powdery spots on the leaves and stems.', 'prevention': 'Ensure good air circulation, avoid overhead watering, and use fungicides if necessary.'},
#     2: {'label': 'Rust (Puccinia triticina)', 'description': 'Rust is a fungal disease that causes rust-colored spots on the leaves and stems of plants. It can significantly reduce crop yields.', 'prevention': 'Remove and destroy infected leaves, avoid overhead watering, and apply appropriate fungicides.'}
# }



# # Function to get predictions from the model
# def get_result(image_path):
#     img = load_img(image_path, target_size=(225, 225))
#     x = img_to_array(img)
#     x = x.astype('float32') / 255.
#     x = np.expand_dims(x, axis=0)
#     predictions = model.predict(x)[0]
#     return predictions

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         return "No file part"
#     f = request.files['file']
#     if f.filename == '':
#         return "No selected file"

#     # Ensure uploads directory exists
#     uploads_dir = os.path.join(app.instance_path, 'uploads')
#     if not os.path.exists(uploads_dir):
#         os.makedirs(uploads_dir)

#     # Save the file
#     file_path = os.path.join(uploads_dir, secure_filename(f.filename))
#     try:
#         f.save(file_path)
#     except Exception as e:
#         return f"An error occurred while saving the file: {str(e)}"

#     # Get predictions
#     try:
#         predictions = get_result(file_path)
#         # predicted_label = labels[np.argmax(predictions)]
#         predicted_label_index = np.argmax(predictions)
#         predicted_label = labels[predicted_label_index]['label']
#         description = labels[predicted_label_index]['description']
#         prevention = labels[predicted_label_index]['prevention']
#         # return render_template('result.html', label=predicted_label, description=description, video_link=video_link)
#         # return str(predicted_label,description,video_link)
#         return render_template_string('''
#         <!doctype html>
#         <html lang="en">
#         <head>
#             <meta charset="UTF-8">
#             <meta name="viewport" content="width=device-width, initial-scale=1.0">
#             <title>Prediction Result</title>
#             <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
#         </head>
#         <body>
#             <div class="container">
#                 <h1 class="text-center my-4">Prediction Result</h1>
#                 <div class="card">
#                     <div class="card-body">
#                         <h4 class="card-title text-center">{{ label }}</h4>
#                         <p class="card-text text-center">Description: {{ description }}</p>
#                         {% if prevention %}
#                             <div class="text-center">
#                                 <p><strong>Prevention:</strong> {{ prevention }}</p>
#                             </div>
#                         {% endif %}
#                     </div>
#                 </div>
#                 <div class="text-center mt-4">
#                     <a href="/" class="btn btn-primary">Upload Another Image</a>
#                 </div>
#             </div>
#         </body>
#         </html>
#         ''', label=predicted_label, description=description, prevention=prevention)
#     except Exception as e:
#         return f"An error occurred during prediction: {str(e)}"

# if __name__ == '__main__':
#     # Ensure instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     app.run(debug=True)



import os
import numpy as np
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

app = Flask(__name__)

# Load the pre-trained model
model = load_model('model.h5')
print('Model loaded. Check http://127.0.0.1:5000/')

# Define the labels with prevention methods
labels = {
    0: {'label': 'Healthy', 'description': 'The plant is healthy.', 'prevention': ''},
    1: {'label': 'Powdery mildew (order Erysiphales)', 'description': 'Powdery mildew is a fungal disease that affects a wide range of plants. It is characterized by white powdery spots on the leaves and stems.', 'prevention': 'Ensure good air circulation, avoid overhead watering, and use fungicides if necessary.'},
    2: {'label': 'Rust (Puccinia triticina)', 'description': 'Rust is a fungal disease that causes rust-colored spots on the leaves and stems of plants. It can significantly reduce crop yields.', 'prevention': 'Remove and destroy infected leaves, avoid overhead watering, and apply appropriate fungicides.'}
}

# Function to get predictions from the model
def get_result(image_path):
    img = load_img(image_path, target_size=(225, 225))
    x = img_to_array(img)
    x = x.astype('float32') / 255.
    x = np.expand_dims(x, axis=0)
    predictions = model.predict(x)[0]
    return predictions

@app.route('/', methods=['GET'])
def index():
    return render_template_string('''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload Image</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="text-center my-4">Upload Image for Prediction</h1>
            <form method="post" action="/predict" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="file">Select image file:</label>
                    <input type="file" class="form-control" id="file" name="file" onchange="previewImage(event)">
                </div>
                <img id="imagePreview" src="" alt="Image preview" style="display: none; max-width:40%; height: auto;" class="my-4">
                <button type="submit" class="btn btn-primary">Predict</button>
            </form>
        </div>
        <script>
            function previewImage(event) {
                var input = event.target;
                var reader = new FileReader();
                reader.onload = function () {
                    var imagePreview = document.getElementById('imagePreview');
                    imagePreview.src = reader.result;
                    imagePreview.style.display = 'block';
                                  imagePreview.style.alignItem='center';
                }
                reader.readAsDataURL(input.files[0]);
            }
        </script>
       
    </body>
    </html>
    ''')

@app.route('/predict', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    f = request.files['file']
    if f.filename == '':
        return "No selected file"

    # Ensure uploads directory exists
    uploads_dir = os.path.join(app.instance_path, 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)

    # Save the file
    file_path = os.path.join(uploads_dir, secure_filename(f.filename))
    try:
        f.save(file_path)
    except Exception as e:
        return f"An error occurred while saving the file: {str(e)}"

    # Get predictions
    try:
        predictions = get_result(file_path)
        predicted_label_index = np.argmax(predictions)
        predicted_label = labels[predicted_label_index]['label']
        description = labels[predicted_label_index]['description']
        prevention = labels[predicted_label_index]['prevention']
        return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prediction Result</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h1 class="text-center my-4">Prediction Result</h1>
                <div class="card">
                    <div class="card-body">
                        <h4 class="card-title text-center"><strong>Disease Name:</strong>{{ label }}</h4>
                        <p class="card-text text-center"><strong>Description:</strong>  {{ description }}</p>
                        {% if prevention %}
                            <p class="text-center"><strong>Prevention:</strong> {{ prevention }}</p>
                        {% endif %}
                    </div>
                </div>
                <div class="text-center mt-4">
                    <a href="/" class="btn btn-primary">Upload Another Image</a>
                </div>
            </div>
        </body>
        </html>
        ''', label=predicted_label, description=description, prevention=prevention)
    except Exception as e:
        return f"An error occurred during prediction: {str(e)}"

if __name__ == '__main__':
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.run(debug=True)
