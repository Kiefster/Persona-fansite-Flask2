from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.games import Game
from flask_app.models.playerreviews import PlayerReviews

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    games = Game.get_all(session['user_id'])
    return render_template("dashboard.html", user=user, games=games)
@app.route('/GameRating')
def Rating():
    if 'user_id' not in session:
        return redirect('logout')
    data ={
        'id': session['user_id']
    }

    user = User.get_by_id(data)
    games = Game.get_all(session['user_id'])
    return render_template("GameRating.html", user=user, games=games)


@app.route('/new/review/<int:game_id>/submit', methods=['POST'])
def new_review(game_id):
    if 'user_id' not in session:
        return redirect('logout')
    data = {
        'review': request.form['review'],
        'rating': request.form['rating'],
        'author_id': session['user_id'],
        'game_id': game_id
    }

    PlayerReviews.save(data)

    return redirect('/GameRating')


@app.route('/GameSection')
def Section():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    games = Game.get_all()
    return render_template("GameSection.html", user=user, games=games)
@app.route('/review/edit/<int:gamereview_id>')
def edit_review(gamereview_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    return render_template('EditReview.html',
        user=User.get_by_id({'id':session['user_id']}),
        playerreview =PlayerReviews.get_one({'id':gamereview_id}))
@app.route('/edit/<int:gamereview_id>/submit',methods=['post'])
def process_review(gamereview_id):
    if 'user_id' not in session:
        return redirect('/logout') 
    data = {
        'review': request.form['review'],
        'rating': request.form['rating'],
        'id': gamereview_id
    }
    PlayerReviews.update_review(data)

    return redirect('/GameRating')
@app.route('/review/delete/<int:gamereview_id>')
def delete_review(gamereview_id):
    if 'user_id' not in session:
        return redirect('/logout') 
    PlayerReviews.delete_review({'id':gamereview_id})
    return redirect('/GameRating')