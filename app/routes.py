from app import app
from flask import render_template,url_for,redirect
from app.forms import LoginForm
from flask_login import current_user, login_user,logout_user
from app.models import User

@app.route('/')
@app.route('/index')
def index():
	user = {'username':'duke'}
	posts = [
		{
			'author':{'username':'刘'},
			'body':'这是模板模块中的循环例子～1'

		},
		{
			'author': {'username': '忠强'},
			'body': '这是模板模块中的循环例子～2'
		}
	]
	return render_template('index.html',title='我的',user=user,posts=posts)

@app.route('/login',methods=['GET','POST'])
def login():
    #判断当前用户是否验证，如果通过的话返回首页
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = LoginForm()
    #对表格数据进行验证
	if form.validate_on_submit():
        #根据表格里的数据进行查询，如果查询到数据返回User对象，否则返回None
		user = User.query.filter_by(username=form.username.data).first()
        #判断用户不存在或者密码不正确
		if user is None or not user.check_password(form.password.data):
            #如果用户不存在或者密码不正确就会闪现这条信息
			
            #然后重定向到登录页面
			return redirect(url_for('login'))
        #这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
		login_user(user,remember=form.remember_me.data)
		return redirect(url_for('index'))
	return render_template('login.html',title='登录',form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))
