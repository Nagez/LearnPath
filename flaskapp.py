from flask import Flask,render_template,redirect

app = Flask(__name__) # init app

@app.route('/') # the url /
def home():
    return render_template('LearnPathHome.html') # get the html file named LearnPathHome, must be in templates folder


@app.route('/page1', methods=["GET","POST"])
def page1():
    return render_template('page1.html')


@app.route('/page2', methods=["GET","POST"])
def page2():
    return render_template('page2.html')


@app.route('/cool') # the url /cool
def hi():
    return 'Hi cool'
