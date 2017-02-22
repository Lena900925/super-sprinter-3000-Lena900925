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

@app.route('/story', methods = ['GET'])
def story_display(name="- Add new Story"):
    return render_template('form.html', name=name, form_action=url_for('new_story'))

@app.route('/delete/<int:story_id>')
def delete_story(story_id):
    story = Stories.get(Stories.id == story_id)
    story.delete_instance()
    return redirect(url_for('listing'))

@app.route('/editing/<int:story_id>', methods= ['POST'])
def editing_story(story_id):
    edited_story = Stories.select().where(Stories.id == story_id).get()
    title1 = edited_story.story_title
    title2 = edited_story.user_story
    title3 = edited_story.acceptance_criteria
    title4 = edited_story.business_value
    title5 = edited_story.estimation
    title6 = edited_story.status
    return render_template('form.html', title1=title1, title2=title2, title3=title3, title4=title4, title5=title5, title6=title6, form_action=url_for('listing'))

#Editor page [/story/<story_id>]
@app.route('/story/<int:story_id>', methods = ['GET'])
def edit_story(name="- Edit Story"):
    return render_template('form.html', name=name)


if __name__== "__main__":
    init_db()
    app.run(debug=True)