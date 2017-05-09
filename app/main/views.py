from datetime import datetime
from flask import render_template,session, redirect, url_for, current_app
from flask import request, flash, send_from_directory
from . import main
from .. import db
from ..models import User,File
from werkzeug import secure_filename
import uuid,os
from urllib.parse import quote

UPLOAD_FOLDER =  os.path.join(os.path.abspath(''),'upload')
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif','doc','docx','zip','rar','ppt'])
def allow_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@main.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userdata = request.form.to_dict()
        user = User.query.filter_by(username=userdata['username']).first()
        if user:
            print(user,'!!!')
            if user.password == userdata['password']:
                session['user'] = user.username
                print('登录成功！！！！')
                return redirect(url_for('main.index'))
        flash('账户名或者密码错误!')
        return redirect(url_for('main.login'))
    return render_template('AdminLogin.html')

@main.route('/logout')
def logout():
    if session.get('user'):
        del session['user']
    return redirect(url_for('main.index'))

@main.route('/filelist')
def filelist():
    files = File.query.order_by(File.time.desc()).all()
    print (files)
    return render_template("uploadFiel.html", files=files)

@main.route('/uploadfile', methods=['GET','POST'])
def uploadfile():
    if request.method == 'POST':
        file = request.files['file']
        if file and allow_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = file.filename
            uuidfilename = str(uuid.uuid1())+filename
            uuidpath = os.path.join(UPLOAD_FOLDER,uuidfilename)
            uuidpath = uuidpath.replace('\\','/')
            filedata = File(filename=filename,uuidpath=uuidpath)
            db.session.add(filedata)
            db.session.commit()
            file.save(uuidpath)
            return redirect(url_for('main.filelist'))
        flash('上传失败,请检查文件！！')
    return render_template('upload.html')

@main.route('/download/<int:id>')
def download(id):
    file = File.query.get_or_404(id)
    uuidname = os.path.split(file.uuidpath)[1]
    response = send_from_directory(UPLOAD_FOLDER, uuidname, as_attachment=True)
    if quote(file.filename)!=file.filename:
        response.headers['Content-Disposition'] = "attachment; filename=\"%s\"; filename*=utf-8''%s" % (quote(file.filename),quote(file.filename))
    else:
        response.headers['Content-Disposition'] = "attachment; filename=\"%s\"" % file.filename
    return response

@main.route('/delete/<int:id>')
def delete(id):
    file = File.query.get_or_404(id)
    print (file.uuidpath)
    if os.path.exists(file.uuidpath):
        os.remove(file.uuidpath)
        db.session.delete(file)
        db.session.commit()
        return redirect(url_for('main.filelist'))
    flash('删除失败，文件不存在')
    return redirect(url_for('main.filelist'))
