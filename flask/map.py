from flask import Flask, render_template, request
import os
import io
import json
import numpy as np
app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')
 
