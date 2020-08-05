from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Text, String, Boolean
# from flask_script import Manager  # 用命令操作的扩展包
# from flask_migrate import Migrate, MigrateCommand  # 操作数据库迁移文件的扩展包

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost/vulnerability'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 显示数据库操作的原生数据就是直接在数据库操作的数据，便于查错
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
# manager = Manager(app)
# # 创建迁移对象
# migrate = Migrate(app, db)
# # 将迁移文件的命令添加到‘db’中
# manager.add_command('db', MigrateCommand)


class add_cnvd(db.Model):
    __tablename__ = 'one_cnvd_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(Text, server_default="")
    cnvd_id = db.Column(String(100), server_default="")
    cve_id = db.Column(String(100), server_default="")
    cve_url = db.Column(String(288), server_default="")
    levle = db.Column(String(100), server_default="")
    affect_product = db.Column(Text, server_default="")
    vul_type = db.Column(String(288), server_default="")
    posted_time = db.Column(String(100), server_default="")
    openTime = db.Column(String(100), server_default="")
    company_name = db.Column(String(288), server_default="")
    refer_link = db.Column(Text, server_default="")
    solve_way = db.Column(Text, server_default="")
    describe = db.Column(Text, server_default="")
    patch = db.Column(String(288), server_default="")
    patch_describe = db.Column(Text, server_default="")


db.create_all()
