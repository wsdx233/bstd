from flask import Flask

app = Flask(__name__, template_folder='../templates')

# 导入路由，必须在 app 创建之后
from app import routes