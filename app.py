from flask import Flask, app,jsonify,request
import time

app = Flask(__name__)
@app.route("/scrap",method=["POST"])
def response():
    query=dict(request.from)['query']
    result=query+" "+time.ctime()
    return jsonify({"response":result})
if __name__=="__main__":
    app.run(host="0.0.0.0",)