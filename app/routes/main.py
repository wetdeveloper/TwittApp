# app/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .. import db
from ..Model import *

   
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('main.twitts'))

@main_bp.route('/home/twitts/', defaults={'start': 0})
@main_bp.route('/home/twitts/<int:start>')
def twitts(start):
    # فعلاً فقط برای تست
    return "Twitts page - Refactoring in progress"
