from flask import Flask

app2 = Flask(__name__)

@app2.route('/')
def hello_app2():
    return 'Hello from KNUE!'


@app2.route('/greeting')
def greeting():
    return 'Welcome to the python world.'


if __name__ == '__main__':
    app2.run()
