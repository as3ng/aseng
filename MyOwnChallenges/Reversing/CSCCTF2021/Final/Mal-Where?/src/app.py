from flask import Flask,render_template,url_for,send_file

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/siskoll')
def siskoll():
	return open("siskol.png","rb").read()

@app.route('/ev1l')
def ev1l():
	return open("3v1l.vbs","r").read()

@app.route('/malamjumat')
def malamjumat():
	return send_file("asik.exe",as_attachment=True)

if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		port=42069,
		debug=False
		)
