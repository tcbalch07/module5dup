from flask import render_template

# Directly define the routes
def index():
    return render_template('index.html')

def top_10():
    return render_template('top10.html')
