# all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response, jsonify
from dao import DAO
import random

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development mode',
    USERNAME='admin',
    PASSWORD='13574206950'
))


dao = DAO()

session_in_memory = ""

@app.route('/', methods=['GET'])
def main_page():
    return redirect(url_for('static', filename='index.html'))




@app.route('/blog', methods=['GET'])
def blog_main():
    if session.get("secret_key") == app.config["SECRET_KEY"]:
        return render_template('blog_management.html')
    else:
        return render_template('blog_main.html')


@app.route('/blog/api/post', methods=['GET'])
def post_api():
    try:
        limit_str = request.args.get("limit")
        if limit_str:
            limit = int(limit_str)
        else:
            limit = 5
    except ValueError:
        limit = 0


    data = []
    if limit > 0:
        sql = "SELECT * FROM post ORDER BY timestamp DESC LIMIT %d" % limit
        try:
            conn  = dao.connect()
            cur = conn.cursor()
            cur.execute(sql)
            for row in cur:
                post = {}
                post["id"] = row[0]
                post["author"] = row[1]
                post["content"] = row[2]
                post["timestamp"] = row[3]
                post["cover"] = row[4]
                post["title"] = row[5]
                data.append(post)
        finally:
            conn.close()
        '''
        render data for frontend
        '''
    return jsonify(data)





@app.route('/blog/api/post', methods=['POST'])
def post_in_api():
    if session.get("secret_key") == app.config["SECRET_KEY"]:
        js = request.json
        if js and 'title' in js:
            if request.json["cover"]:
                sql = "INSERT INTO `blog`.`post` (`author`, `content`, `timestamp`, `cover`, `title`) VALUES (\'%s\', \'%s\',\'%s\',\'%s\',\'%s\');" % (js['author'], js['content'],js['timestamp'], js['cover'], js['title'])
                print sql
                dao.execute(sql)
            else:
                sql = "INSERT INTO `blog`.`post` (`author`, `content`, `timestamp`, `title`) VALUES (\'%s\', \'%s\',\'%s\',\'%s\');" % (js['author'], js['content'],js['timestamp'], js['title'])
                print sql
                dao.execute(sql)
            return jsonify({
            'status': 'success'
            })
        else:
            return jsonify({
            'status': 'failure'
            })
    else:
        return jsonify({
        'status': 'failure'
        })


@app.route('/blog/api/post/<int:id_>', methods=['PUT'])
def post_put_api(id_):
    if session.get("secret_key") == app.config["SECRET_KEY"]:
        js = request.json
        if js and 'title' in js:
            if request.json["cover"]:
                sql = "UPDATE post SET author = \'%s\', content = \'%s\', timestamp = \'%s\', cover = \'%s\', title = \'%s\' WHERE id = %d" % (js['author'], js['content'],js['timestamp'], js['cover'], js['title'], id_)
                print sql
                dao.execute(sql)
            else:
                sql = "UPDATE post SET author = \'%s\', content = \'%s\', timestamp = \'%s\', title = \'%s\' WHERE id = %d" % (js['author'], js['content'],js['timestamp'], js['title'], id_)
                print sql
                dao.execute(sql)
            return jsonify({
            'status': 'success'
            })
        else:
            return jsonify({
            'status': 'failure'
            })
    else:
        return jsonify({
        'status': 'failure'
        })

@app.route('/blog/api/post/<int:id_>', methods=['DELETE'])
def post_delete_api(id_):
    if session.get("secret_key") == app.config["SECRET_KEY"]:
        sql  = "DELETE FROM post WHERE id = %d" % id_
        dao.execute(sql)
        return jsonify({
            'status': 'success'
            })
    else:
        return jsonify({
        'status': 'failure'
        })


@app.route('/blog/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            rand = str(random.random())
            session['secret_key'] = rand
            app.config['SECRET_KEY'] = rand

            print session_in_memory
            flash('You were logged in')
            return redirect(url_for('blog_main'))
    return render_template('login.html', error=error)


@app.route("/blog/logout", methods=['GET'])
def logout():
    session.pop('secret_key', None)
    rand = str(random.random())
    app.config['SECRET_KEY'] = rand
    #Clear session
    flash("succefully log out")
    return redirect(url_for("blog_main"))
