from flask import request, redirect, render_template
from app import app, db
from models import Blog
import cgi

def validate_entry(title, body):
    result = ""
    blog_title = title
    blog_body = body
    blog_title_error = ''
    blog_body_error = ''

    if blog_title == '':
        blog_title_error = "Plese fill in the title"
    if blog_body == '':
        blog_body_error = "Please fill in the body"

    if blog_title_error or blog_body_error: 
        return render_template('blog_new_post.html', 
            blog = blog_title, body = blog_body,
            blog_title_error = blog_title_error,
            blog_body_error = blog_body_error
            )
    return result

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect ('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def main_blog_listing(): 
    if request.method == 'POST': 
        blog_title = request.form['blog']
        blog_body = request.form['body']
        error_page = validate_entry(blog_title, blog_body)
        if error_page:
            return error_page
        #succes
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

        new_blog_id = new_blog.id
        return redirect(f'/display_blog?id={new_blog_id}')    
 
    blogs = Blog.query.all()
    return render_template('blog_listings.html',
        title="Build A Blog", 
        blogs=blogs) 

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'GET':
        return render_template('blog_new_post.html')
    return redirect('/')

@app.route('/display_blog', methods=['GET'])
def display_blog():
    blog_id = int(request.args['id'])
    blog = Blog.query.get(blog_id)
    db.session.add(blog)
    db.session.commit()

    return render_template('display_blog.html', blog=blog)  


if __name__ == '__main__':
    app.run()
