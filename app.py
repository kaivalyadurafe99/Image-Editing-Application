import os
import cv2
from flask import Flask,render_template,request,flash
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}
app.secret_key = 'super secret key'



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename,operation):
    print(f"The Operation is {operation} and filename is {filename}")
    img=cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            newfilename=f"static/{filename}"
            cv2.imwrite(newfilename,imgProcessed)
            return newfilename
        case "cwebp":
            newfilename=f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cjpg":
            newfilename=f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename,img)
            return newfilename
        case "cpng":
            newfilename=f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename,img)
            return newfilename
        

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="POST":
        operation=request.form.get("operation")

        if 'file' not in request.files:
            flash('No file part')
            return "Error"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "Error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new=processImage(filename,operation)
            flash(f"Your Image has been processed and is available <a href='/{new}' target='_blank'>here...</a>")
            return render_template("index.html")

    return render_template("index.html")
        
if __name__=="__main__":
    app.run(debug=True)