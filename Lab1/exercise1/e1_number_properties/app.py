from flask import Flask, request, jsonify, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

@app.route('/prime-checker')
def prime_checker():
    number = int(request.args.get('number'))
    result = is_prime(number)
    return jsonify(result=f"{number} is {'a prime' if result else 'not a prime'} number.")

@app.route('/gcd-calculator')
def gcd_calculator():
    number1 = int(request.args.get('number1'))
    number2 = int(request.args.get('number2'))
    result = gcd(number1, number2)
    return jsonify(result=f"The GCD of {number1} and {number2} is {result}.")

if __name__ == '__main__':
    app.run(debug=True)
