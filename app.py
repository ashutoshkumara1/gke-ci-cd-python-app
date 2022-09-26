from flask import Flask
app = Flask('hello-world')
@app.route('/')
def hello():
 return "The Container Deployed On Kubernetes Cluster\n and Running it On Server!"
if __name__ == '__main__':
 app.run(host = '0.0.0.0', port = 8080)
