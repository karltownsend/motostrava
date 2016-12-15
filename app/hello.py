from flask import Flask, render_template
import numpy as np
filename = 'laptimer.csv'
lines_to_skip = 1    # first line in the header is the title, not for processing

print 'ok, does this work?' # but only prints in console

data = np.recfromcsv(filename, delimiter=',', skip_header=lines_to_skip)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/python/')
def python():
    return render_template('python.html')
    
if __name__ == '__main__':
    app.run(debug=True)