from flask import Flask, render_template,request


app = Flask(__name__)


######药店定位页面
# @app.route('/dingwei')
# def dingwei():
#     return render_template('dingwei.html')

######医院定位页面
# @app.route('/dingwei2')
# def dingwei2():
#     return render_template('dingwei2.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
