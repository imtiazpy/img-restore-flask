import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from img_restorer import predict_image

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


# routes
@app.route("/")
def home():
  return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_filename = "." + url_for("static", filename="images/" + filename)
            file.save(full_filename)

            predicted_image_url = predict_image(full_filename)

            return render_template("index.html", filename=filename, restored_img_url=predicted_image_url)
        





# Run the app
if __name__ == "__main__":
  app.run(debug=True)