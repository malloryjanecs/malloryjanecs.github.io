from flask import Flask, render_template, request
import csv
import datetime

app = Flask(__name__)

@app.route('/')
def home_page(message =None):
	if message:
		return render_template('index.html', message=message)
	else:
		return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
	return render_template(page_name)

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
	if request.method == "POST":
		try:
			data = request.form.to_dict()
			write_to_csv(data)
			return home_page("**Thank you for your email. I will contact you shortly.**")
		except:
			error_log('submitting form')
			return home_page("**An error occured when sending your message. I will look into this immediately. Please contact me at mallory.jane.cs@gmail.com if it is urgent.**")


def write_to_csv(data):
	with open('database.csv', mode='a', newline='') as csvdb:
		email = data['email']
		subject = data['subject']
		message = data['message']
		csv_writer = csv.writer(csvdb, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([email, subject, message])

def error_log(message):
	with open('error_log.csv', mode='a', newline='') as csvdb:
		current_time = datetime.datetime.now()
		csv_writer = csv.writer(csvdb, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		csv_writer.writerow([f'Error: {message}', current_time])
