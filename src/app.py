import os
import flask
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import werkzeug
import numpy as np
import pandas as pd
import jobsnlp


# Set up filepath to store user submitted resume
UPLOAD_FOLDER = '/Users/bil2ab/vethacks/web/upload'
ALLOWED_EXTENSIONS = set(['docx', 'txt', 'pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load job data
jobs_list = pd.read_pickle('jobs.pkl')
                       
# Verify file extension of user resume    
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = jobsnlp.ResumeJobsRecommender()
model.fit(jobs_list['description'].values)

@app.route('/',  methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')
    
    if flask.request.method == 'POST':
        # No file in post submission
        if 'file' not in flask.request.files:
            print('No file!') #flash
            return redirect(flask.request.url)
        file = flask.request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No file selected!') #flash
            return redirect(request.url)
        if file and allowed_file(file.filename):
            resume = request.files.get(file)
            # Secure Resume
            secured_resume = werkzeug.utils.secure_filename(file.filename)
            # Store user resume in upload folder
            user_resume = os.path.join(app.config['UPLOAD_FOLDER'], secured_resume)
            file.save(user_resume)

            if user_resume.endswith('.docx'):
                resume_text = jobsnlp.read_docx(user_resume)
            elif user_resume.endswith('.pdf'):
                resume_text = jobsnlp.read_pdf(user_resume)
            else:
                resume_text = jobsnlp.read_txt(user_resume)

            # Clean Resume
            #clean_resume_text = jobsnlp.clean_resume(resume_text)
            # Model prediction
            result_index, scores = model.predict(resume_text,20)
            # Create result dataframe
            result_df = jobs_list.iloc[result_index]
            result_df['scores'] = scores
            return result_df.to_html()                      
            
        return flask.redirect(flask.request.url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)