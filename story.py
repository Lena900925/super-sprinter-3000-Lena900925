import os
from peewee import *
from flask import Flask, render_template, request, redirect, url_for
from models import *

app = Flask(__name__)
app.config.from_object(__name__)

def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.drop_tables([Stories], safe=True)
    ConnectDatabase.db.create_tables([Stories], safe=True)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key'))

#List page [/ and /list]
@app.route('/list')
@app.route('/')
def listing(name=" "):
    stories=Stories.select()
    return render_template('list.html', stories=stories, name=name)

@app.route('/story', methods = ['GET'])
def story_display(name="- Add new Story"):
    return render_template('form.html', name=name)

#Adding page [/story]
@app.route('/story_added', methods = ['POST'])
def new_story():
    new_entry = Stories.create(story_title=request.form['story_title'],
                               user_story=request.form['user_story'],
                               acceptance_criteria= request.form['acceptance_criteria'],
                               business_value=request.form['business_value'],
                               estimation=request.form['estimation'],
                               status=request.form['status'])
    new_entry.save()
    return redirect(url_for('listing'))

@app.route('/story/<int:story_id>', methods= ['GET'])
def edit(story_id):
    user_story = Stories.select().where(Stories.id == story_id).get()
    return render_template("form.html", user_story=user_story)

#Editor page [/story/<story_id>]
@app.route('/story/<int:story_id>', methods= ['POST'])
def edit_story(story_id):
    user_story = Stories.select().where(Stories.id == story_id).get()
    user_story.story_title = request.form['story_title']
    user_story.user_story = request.form['user_story']
    user_story.acceptance_criteria = request.form['acceptance_criteria']
    user_story.business_value = request.form['business_value']
    user_story.estimation = request.form['estimation']
    user_story.status = request.form['status']
    user_story.save()
    return redirect(url_for('listing'))

@app.route('/delete/<int:story_id>', methods= ['GET'])
def delete_story(story_id):
    Stories.delete().where(Stories.id == story_id).execute()
    return redirect(url_for('listing'))

if __name__== "__main__":
    init_db()
    app.run(debug=True)