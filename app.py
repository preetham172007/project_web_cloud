#Importing Libraries

from flask import Flask, render_template, request
import os
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

#Loading Environment Variables
load_dotenv()

#Making flask app variable
app =Flask(__name__)

#Making Connection Variable
conn=psycopg2.connect(host=os.getenv("DB_HOST"),database=os.getenv("DB_NAME"),user=os.getenv("DB_USER"),password=os.getenv("DB_PASSWORD"),port=os.getenv("DB_PORT"))

#Make AI Client
client=OpenAI(api_key = os.getenv("GROQ_API_KEY"),base_url="https://api.groq.com/openai/v1")

#Make Generate function
def generate():
	response=client.chat.completions.create(model="llama-3.3-70B-versatile", messages=[{"role":"user","content":"Hello"}])
	return response.choices[0].message.content
#Making route for home page
@app.route("/")

def home():
	return render_template("index.html")

#Making route for Submit:
@app.route("/submit", methods=["POST"])

def submit():
	name=request.form["name"]
	email=request.form["email"]
	age=request.form["age"]
	course=request.form["course"]
	city=request.form["city"]
	response=generate()
	cur = conn.cursor()
	
	cur.execute("""INSERT into student(name, email, age, course, city, response) VALUES(%s,%s,%s,%s,%s,%s)""",(name,email,age,course,city,response))

	conn.commit()
	cur.close()

	return response

if __name__=="__main__":
	app.run(debug=True)	

