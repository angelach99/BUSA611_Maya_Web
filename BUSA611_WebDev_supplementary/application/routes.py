from application import app
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_marshmallow import Marshmallow
import json
import os

@app.route("/")
@app.route("index")
def index():
    return "<h1>Hello Earth!!</h1>"

# # Routes
# @app.route('/testing_route')
# def testing_route():
#     return jsonify(message='Hello! This is an example to test the route!'), 200
    

# @app.route('/testing_route_2/<string:keyword>/<int:number>')
# def testing_route_2(keyword: str, number: int):
#     if number > 5:
#         return jsonify(message="Too much keyword, " + keyword + ", sorry."), 401
#     else:
#         return jsonify(message="It is acceptable, " + keyword)


# @app.route('/show_maya_waypoint', methods=['GET'])
# def show_maya_waypoint():
#     waypoint_list = maya_waypoint.query.all()
#     result = waypoints_schema.dump(waypoint_list)
#     return jsonify(result)


# @app.route('/show_maya_attribute', methods=['GET'])
# def show_maya_attribute():
#     attribute_list = maya_attribute.query.all()
#     result = attributes_schema.dump(attribute_list)
#     return jsonify(result)


# @app.route('/show_maya_command', methods=['GET'])
# def shiw_maya_command():
#     command_list = maya_commands.query.all()
#     result = commands_schema.dump(command_list)
#     return jsonify(result)