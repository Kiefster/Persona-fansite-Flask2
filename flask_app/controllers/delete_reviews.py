from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.game_valid import games
import datetime


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    games = games.get_all()
    
    return render_template("GameRating.html", user=user, games=games)

@app.route('/new/review')
def new_review():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)

    return render_template("new_comments.html", user=user)

@app.route('/new/sighting/submit', methods=['POST'])
def sighting_insert():
    if 'user_id' not in session:
        return redirect('/logout')
    if not new_review.validate_review(request.form):
        return redirect('/new/review')
    
    review_data = { 
        "posted_by": session['user_id'],
        "location": request.form['location'],
        "description": request.form['review'],
        "sighted_at": datetime.datetime.strptime(request.form['sighted_at'], '%Y-%m-%d'),
        "sasquatch_count": request.form['sasquatch_count'],  
    }
    review_data = review_data.save_review(review_data)
    

    return redirect('/GameRating')

@app.route('/show/<int:player_review>')
def sighting_show(game_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    sighting_data = {
        'id': sighting_id
    }
    user = User.get_by_id(user_data)
    sighting = games.get_games(game_id)
    if not sighting:
        return redirect('/dashboard')
    return render_template("GameRating.html", user=user, games=games)

@app.route('/EditComment/<int:game_id>')
def review_edit(game_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    sighting_data = {
        'id': sighting_id
    }

    user = User.get_by_id(user_data)
    reviews = review_edit.get_reviews(review_edit)
    if not sighting:
        return redirect('/dashboard')
    return render_template("edit_sighting.html", user=user, games=games)

@app.route('/edit/<int:sighting_id>/submit', methods=['POST'])
def sighting_update(sighting_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not new_review.validate_reviews(request.form):
        return redirect('/sightings/edit/{}'.format(sighting_id))
    
    data = { 
        "id": sighting_id,
        "posted_by": session['user_id'],
        "location": request.form['location'],
        "description": request.form['description'],
        "sighted_at": datetime.datetime.strptime(request.form['sighted_at'], '%Y-%m-%d'),
        "sasquatch_count": request.form['sasquatch_count'] 
    }
    
    reviews = Reviews.update_reviews(data)
    
    return redirect('/GameRating')

@app.route('/delete/<text:review_id>')
def delete_sighting(sighting_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = { 
        "id": sighting_id,
        "posted_by": session['user_id']
    }
    comments = comments.delete_comments(data)
    return redirect('/GameRating')