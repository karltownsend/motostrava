from flask import Flask, render_template, flash, redirect

# from Microblog
# from app import app
# from .forms import LoginForm

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
    
@app.route('/python/microblog/')
def microblog():
    return render_template('microblog.html')
        
if __name__ == '__main__':
    app.run(debug=True)
