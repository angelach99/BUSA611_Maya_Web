from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_marshmallow import Marshmallow
import json
import os

# from application import app
app = Flask(__name__)
__file__ = 'main.py'
db_name = 'maya.db'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_name)

db = SQLAlchemy(app)
ma = Marshmallow(app)

# db
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')

# Seed data from file
with open('data\Maya_CompleteCommandList_2023.json') as f:
   data = json.load(f)

maya_data = data['filtering']['reference_list']

@app.cli.command('db_add_data')
def db_add_data():
    for k in range(len(maya_data['attributes'])):
        data_point = maya_attribute(attribute = maya_data['attributes'][k])
        db.session.add(data_point)
        db.session.commit()
        print(str(k) + ' attribute data added!')  
    for i in range(len(maya_data['waypoints'])):
        data_point = maya_waypoint(waypoint = maya_data['waypoints'][i])
        db.session.add(data_point)
        db.session.commit()
        print(str(i) + ' waypoint data added!')  
    for j in range(len(maya_data['commands'])):
        data_commands = maya_commands(command = maya_data['commands'][j])
        db.session.add(data_commands)
        db.session.commit()
        print(str(j) + ' command data added!')
    
       
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


# Routes
@app.route('/testing_route')
def testing_route():
    return jsonify(message='Hello! This is an example to test the route!'), 200
    

@app.route('/testing_route_2/<string:keyword>/<int:number>')
def testing_route_2(keyword: str, number: int):
    if number > 5:
        return jsonify(message="Too much keyword, " + keyword + ", sorry."), 401
    else:
        return jsonify(message="It is acceptable, " + keyword)


@app.route('/show_maya_waypoint', methods=['GET'])
def show_maya_waypoint():
    waypoint_list = maya_waypoint.query.all()
    result = waypoints_schema.dump(waypoint_list)
    return jsonify(result)


@app.route('/show_maya_attribute', methods=['GET'])
def show_maya_attribute():
    attribute_list = maya_attribute.query.all()
    result = attributes_schema.dump(attribute_list)
    return jsonify(result)


@app.route('/show_maya_command', methods=['GET'])
def show_maya_command():
    command_list = maya_commands.query.all()
    result = commands_schema.dump(command_list)
    arr = [x['command'] for x in result]
    return jsonify(arr)


# database models
class maya_waypoint(db.Model):
    __tablename__ = 'maya_waypoint'
    waypoint = Column(String, primary_key=True)
    

class maya_attribute(db.Model):
    __tablename__ = 'maya_attribute'
    attribute = Column(String, primary_key=True)


class maya_commands(db.Model):
    __tablename__ = 'maya_commands'
    command = Column(String, primary_key=True)


# Schema
class WaypointSchema(ma.Schema):
    class Meta:
        fields = ['waypoint']


class AttributeSchema(ma.Schema):
    class Meta:
        fields = ['attribute']


class CommandSchema(ma.Schema):
    class Meta:
        fields = ['command']


waypoint_schema = WaypointSchema()
waypoints_schema = WaypointSchema(many=True) # Multiple records back

attribute_schema = AttributeSchema()
attributes_schema = AttributeSchema(many=True)

command_schema = CommandSchema()
commands_schema = CommandSchema(many=True)


if __name__ == '__main__':
    app.run(debug=True)