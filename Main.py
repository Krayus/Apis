from flask import Flask, jsonify, request
import consume

app = Flask(__name__)
@app.route('/consulta/<RUT>',methods=["GET"])
def get_one_by_rut(RUT):
    datOne = consume.get_one(RUT)
    return jsonify(datOne)

if __name__ == '__main__':
    app.run(debug=True)
