from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def app_home():
    return 'Emerging Technologies!'


@app.route('/input')
def input_digit():
    return render_template('mnist-input.html')


if __name__ == '__main__':
    app.run()
