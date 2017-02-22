from connectdatabase import ConnectDatabase
from peewee import *


class Stories(Model):
    story_title = CharField()
    user_story = CharField()
    acceptance_criteria = CharField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField()

    class Meta:
        database = ConnectDatabase.db
