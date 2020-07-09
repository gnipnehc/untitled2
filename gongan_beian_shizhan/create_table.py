from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager  # 用命令操作的扩展包
# from flask_migrate import Migrate, MigrateCommand  # 操作数据库迁移文件的扩展包

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost/test_beian'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 显示数据库操作的原生数据就是直接在数据库操作的数据，便于查错
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
# manager = Manager(app)
# # 创建迁移对象
# migrate = Migrate(app, db)
# # 将迁移文件的命令添加到‘db’中
# manager.add_command('db', MigrateCommand)


class url_all_info(db.Model):
    __tablename__ = 'test_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    main_domain = db.Column(db.VARCHAR)
    url_name = db.Column(db.VARCHAR)
    main_body = db.Column(db.VARCHAR)
    url_type = db.Column(db.VARCHAR)
    use_name = db.Column(db.VARCHAR)
    recode_number = db.Column(db.VARCHAR)
    public_address = db.Column(db.VARCHAR)
    recode_time = db.Column(db.VARCHAR)
    is_code = db.Column(db.Boolean)


db.create_all()
