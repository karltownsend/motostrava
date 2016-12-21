import os, logging, datetime
import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
           
#  find the times for each lap and return a list with the index and time
def get_lap_times(data):
   laps = np.unique(data['lapindex'])
   lap_list = []
   for lap in laps:
       n = data['lapindex'] == lap
       if data[n]['time_lap'][0] != 0:    # ensure lap start time is 0
           print 'error: lap %d start time is %f, not 0' % (lap, data[n]['time_lap'][0])
           # easy enough to adjust time, but this might indicate other errors
       lap_list.append([lap, data[n]['time_lap'][-1]])  # last element is [-1], the final time
   return lap_list
      
#@app.template_filter()
def datetimefilter(value, format='%02M:%02S'):
#  convert a datetime to a different format
    return value.strftime(format)
app.jinja_env.filters['datetimefilter'] = datetimefilter
          
@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/python/')
def python():
    return render_template('python.html')
    
@app.route('/python/microblog/')
def microblog():
    return render_template('microblog.html')
    
# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))
                                
# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
#old upload example
#    return send_from_directory(app.config['UPLOAD_FOLDER'],
#                               filename)
	lines_to_skip = 1		# first line in the header is the title, not for processing
	data = np.recfromcsv(app.config['UPLOAD_FOLDER']+filename, delimiter=',', skip_header=lines_to_skip)
	lap_times = get_lap_times(data)    # list is [[lap num,time], ...]  unsorted
	lap_times_sorted = sorted(lap_times, key=lambda t: t[1])   # lap times from fastest to slowest
#	print lap_times_sorted[0]     # show the fastest [lap#, time]        
	return render_template('laptimes.html', data=data, lap_times=lap_times, lap_times_sorted=lap_times_sorted)
    
@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']
    return render_template(
    	'submitted_form.html',
    	name=name,
    	email=email,
    	site=site,
    	comments=comments)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
    
if __name__ == '__main__':
    app.run(debug=True)