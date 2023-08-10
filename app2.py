from flask import Flask

app2 = Flask(__name__)

@app2.route('/')
def hello_app2():
    return 'Hello from App 2!'

if __name__ == '__main__':
    app2.run()
