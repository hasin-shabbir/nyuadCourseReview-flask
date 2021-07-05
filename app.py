#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, make_response,flash
from markupsafe import escape
import pymongo
import datetime
from bson.objectid import ObjectId
import os
import subprocess

# instantiate the app
app = Flask(__name__)
app.secret_key="foo"

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
import credentials
config = credentials.get()

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode

# make one persistent connection to the database
connection = pymongo.MongoClient(config['MONGO_HOST'], 27017, 
                                username=config['MONGO_USER'],
                                password=config['MONGO_PASSWORD'],
                                authSource=config['MONGO_DBNAME'])
db = connection[config['MONGO_DBNAME']] # store a reference to the database

################################
#courses
#get different collection
#mycol = mydb["customers"]
courseCollection=db["courses"]
# set up the routes

@app.route('/')
def home():
    """
    Route for the home page
    Route for GET requests to the home page.
    Displays some information for the user with links to other pages.
    """
    #course=details = db.courses.find_one({})
    courses = db.courses.find({})
    return render_template('index.html',courses=courses)

@app.route('/reviewPage')
def revPage():
    """
    Route for the review page
    """
    return render_template('review.html')

@app.route('/reviewPage/<coursename>',defaults={'message': None})
@app.route('/reviewPage/<coursename>/<message>')
def reviewPage(coursename,message):
    """
    Route for the review page
    """
    message=message
    course = db.courses.find_one({"title": coursename})
    sort =  [('timestamp', -1)]
    myreviews=db.revs.find({"course_title": coursename}).sort(sort)
    reviews=db.revs.find({"course_title": coursename})

    q=0
    d=0
    w=0
    g=0
    count=0
    for rev in reviews:
        q+=int(rev['quality'])
        d+=int(rev['difficulty'])
        w+=int(rev['workload'])
        g+=int(rev['grading'])
        count+=1
        
    if count!=0:
        q=round(q/count)
        d=round(d/count)
        w=round(w/count)
        g=round(g/count)

    qc="p"+str(q)
    dc="p"+str(d)
    wc="p"+str(w)
    gc="p"+str(g)
    
    return render_template('review.html', course=course, myreviews=myreviews,qc=qc,dc=dc,wc=wc,gc=gc,q=q,d=d,w=w,g=g,message=message)

@app.route('/create_review', methods=['POST'])
def create_review():
    """
    Route for POST requests to the review page.
    Accepts the form submission data for a new review and saves the review to the reviews database.
    """
    name = request.form['r-name']
    password = request.form['r-password']
    quality = request.form['r-quality']
    difficulty = request.form['r-difficulty']
    grading = request.form['r-grading']
    workload = request.form['r-workload']
    comment = request.form['r-message']
    ctitle = request.form['r-title']

    try:
        int(quality)
        int(difficulty)
        int(grading)
        int(workload)
    except ValueError:
        message="invalid values entered in metric ranges"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(quality)>100 or int(quality)<0:
        message="values entered in quality metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(difficulty)>100 or int(difficulty)<0:
        message="values entered in difficulty metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(grading)>100 or int(grading)<0:
        message="values entered in grading metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(workload)>100 or int(workload)<0:
        message="values entered in workload metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))
    
    existing=db.users.count_documents({
        "name":name,
        "password":password,
    }, limit=1)

    

    if(existing):
        email=db.users.find_one({
            "name":name,
            "password":password,
        },
        {"_id":0, "email":1})

        existingReview=db.revs.count_documents({
            "course_title":ctitle,
            "email":email['email'],
        }, limit=1)

        if (existingReview==0):
            review = {
                "name": name,
                "email": email['email'],
                "course_title": ctitle,
                "quality": quality,
                "difficulty": difficulty,
                "grading": grading,
                "workload": workload,
                "comment": comment
            }
            db.revs.insert_one(review)
            return redirect(url_for('reviewPage',coursename=ctitle))
        else:
            message="You already have a review, try editing your previous review"
            return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    else:
        message="Incorrect username or password"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))


@app.route('/register', methods=['POST'])
def register():
    """
    Route for POST requests to the register user.
    Accepts the form submission data for a new user and saves the data to the users database.
    """
    name = request.form['r-name']
    email = request.form['r-email']
    password = request.form['r-password']
    ctitle = request.form['r-title']


    existingAccount=db.users.count_documents({
        "email":email,
    }, limit=1)

    existingName=db.users.count_documents({
        "name":name,
    }, limit=1)

    if(existingAccount==0 and existingName==0):
        user = {
            "name": name,
            "email": email,
            "password": password,
        }
        db.users.insert_one(user)
        return redirect(url_for('reviewPage', coursename=ctitle))
    else:
        message="the user already exists, please change email and or username"
        return redirect(url_for('reviewPage', coursename=ctitle,message=message))


@app.route('/edit', methods=['POST'])
def edit_review():
    """
    Route for POST requests to the edit page.
    Accepts the form submission data for the specified document and updates the document in the database.
    """
    name = request.form['r-name']
    password = request.form['r-password']
    quality = request.form['r-quality']
    difficulty = request.form['r-difficulty']
    grading = request.form['r-grading']
    workload = request.form['r-workload']
    comment = request.form['r-message']
    ctitle = request.form['r-title']

    try:
        int(quality)
        int(difficulty)
        int(grading)
        int(workload)
    except ValueError:
        message="invalid values entered in metric ranges"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(quality)>100 or int(quality)<0:
        message="values entered in quality metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(difficulty)>100 or int(difficulty)<0:
        message="values entered in difficulty metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(grading)>100 or int(grading)<0:
        message="values entered in grading metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    if int(workload)>100 or int(workload)<0:
        message="values entered in workload metric out of range"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))

    existing=db.users.count_documents({
        "name":name,
        "password":password,
    }, limit=1)

    if(existing):
        email=db.users.find_one({
            "name":name,
            "password":password,
        },
        {"_id":0, "email":1})
        review = {
            "name": name,
            "email": email['email'],
            "course_title": ctitle,
            "quality": quality,
            "difficulty": difficulty,
            "grading": grading,
            "workload": workload,
            "comment": comment
        }
        db.revs.update_one(
            {
                "name": name,
                "course_title": ctitle,
            },
            { "$set": review }
        )
        return redirect(url_for('reviewPage',coursename=ctitle))
    else:
        message="Incorrect password"
        return redirect(url_for('reviewPage',coursename=ctitle,message=message))



@app.route('/delete',methods=['POST'])
def delete():
    """
    Route for GET requests to the delete page.
    Deletes the specified record from the database, and then redirects the browser to the read page.
    """
    name = request.form['r-name']
    password = request.form['r-password']
    ctitle = request.form['r-title']
    

    existing=db.users.count_documents({
        "name":name,
        "password":password,
    }, limit=1)

    if(existing):
        existingReview=db.revs.count_documents({
            "course_title":ctitle,
            "name":name,
        }, limit=1)
        if (existingReview):
            db.revs.delete_one({"course_title":ctitle,"name":name})
            return redirect(url_for('reviewPage',coursename=ctitle))
        else:
            message="No existing review posted by you"
            return redirect(url_for('reviewPage',coursename=ctitle,message=message))
    else:
            message="Incorrect password"
            return redirect(url_for('reviewPage',coursename=ctitle,message=message))


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    GitHub can be configured such that each time a push is made to a repository, GitHub will make a request to a particular web URL... this is called a webhook.
    This function is set up such that if the /webhook route is requested, Python will execute a git pull command from the command line to update this app's codebase.
    You will need to configure your own repository to have a webhook that requests this route in GitHub's settings.
    Note that this webhook does do any verification that the request is coming from GitHub... this should be added in a production environment.
    """
    # run a git pull command
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    pull_output = process.communicate()[0]
    # pull_output = str(pull_output).strip() # remove whitespace
    process = subprocess.Popen(["chmod", "a+x", "flask.cgi"], stdout=subprocess.PIPE)
    chmod_output = process.communicate()[0]
    # send a success response
    response = make_response('output: {}'.format(pull_output), 200)
    response.mimetype = "text/plain"
    return response

@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e) # render the edit template


if __name__ == "__main__":
    #import logging
    #logging.basicConfig(filename='/home/ak8257/error.log',level=logging.DEBUG)
    app.run(debug = True)
