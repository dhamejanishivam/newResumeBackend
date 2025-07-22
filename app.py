from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, Response
from flask_cors import CORS
import os
import maker  # Ensure maker.py is in the same directory
import send_details
import save_data
import json
import requests

telegram_send_url = "https://api.telegram.org/bot8113534372:AAF2DahT2CQYToSvG7Z_VMZ_-0BmweybX5I/sendMessage"
chat_id = "1293804795"

dataPassword = 'Basketball <3'
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_DIR = os.path.join(BASE_DIR, "resumeFiles")
RESUME_JSON = os.path.join(BASE_DIR, "resumeData.json")

# Ensure resumeFiles directory exists
os.makedirs(RESUME_DIR, exist_ok=True)



class TelegramBot:
    def __init__(self,message) -> None:
        global message1
        message1 = message
        url = "https://api.telegram.org/bot8113534372:AAF2DahT2CQYToSvG7Z_VMZ_-0BmweybX5I/sendMessage"
        chat_id = "1293804795"
        message = message1
        self.response = requests.post(
            url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "chat_id": chat_id,
                "text": message1
            }
        )


    def check(self):
        if self.response.status_code == 200:
            return True
        else:
            return False

            
@app.route('/')
def index():
    return "<br><h1>It's working!</h1>"


@app.route('/resumeFiles/<path:filename>')
def serve_resume(filename):
    return send_from_directory(RESUME_DIR, filename)


@app.route('/all')
def all():
    content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Access Resumes</title>
        <style>
            body {
                background-color: #1a1a1a; /* Dark background */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                color: #e0e0e0;
            }
            .container {
                background-color: #2c2c2c;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                text-align: center;
            }
            h1 {
                color: #00bcd4; /* A vibrant teal for headings */
                margin-bottom: 25px;
                font-size: 2.5em;
            }
            input[type="password"] {
                padding: 12px 20px;
                margin-bottom: 25px;
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #3a3a3a;
                color: #e0e0e0;
                font-size: 1.1em;
                width: 250px;
                box-sizing: border-box;
            }
            button[type="submit"] {
                background-color: #00bcd4; /* Same vibrant teal for button */
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1.1em;
                transition: background-color 0.3s ease;
            }
            button[type="submit"]:hover {
                background-color: #00aabf;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Enter Password for Resume Access</h1>
            <form action="/passwordCheck" method="post">
                <input type="password" id="password" name="password" placeholder="Enter password" required>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """
    return content


@app.route('/passwordCheck', methods=['POST'])
def checker():
    password = request.form.get("password")
    if password == dataPassword:
        # Authorized Page HTML
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Authorization Granted</title>
            <style>
                body {
                    background-color: #1a1a1a; /* Dark background */
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                    color: #e0e0e0;
                }
                .container {
                    background-color: #2c2c2c;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                    text-align: center;
                    max-width: 600px;
                }
                h1 {
                    color: #00e676; /* Vibrant green for success */
                    margin-bottom: 30px;
                    font-size: 2.5em;
                }
                p {
                    font-size: 1.1em;
                    color: #ccc;
                    margin-bottom: 30px;
                }
                .resume-links {
                    margin-top: 20px;
                    display: flex;
                    flex-direction: column;
                    gap: 15px; /* Space between links */
                }
                .resume-links a {
                    background-color: #4CAF50; /* Green button style for links */
                    color: white;
                    padding: 12px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                    font-size: 1.1em;
                    display: inline-block; /* To allow padding and margin */
                    width: fit-content; /* Adjust width to content */
                    margin: 0 auto; /* Center the links */
                }
                .resume-links a:hover {
                    background-color: #45a049;
                    transform: translateY(-2px); /* Slight lift on hover */
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Authorization Granted!</h1>
                <p>Welcome. Here are the resumes:</p>
                <div class="resume-links">
        """
        # List resume files and add links
        if not os.path.exists(RESUME_DIR):
            os.makedirs(RESUME_DIR) # Ensure directory exists
        
        resume_files = os.listdir(RESUME_DIR)
        if not resume_files:
            html_content += "<p>No resumes found in the directory.</p>"
        else:
            for i in resume_files:
                html_content += f"<a href='/resumeFiles/{i}' target='_blank'>{i}</a>" # target='_blank' to open in new tab

        html_content += """
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    else:
        # Wrong Password Page HTML
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Access Denied</title>
            <style>
                body {
                    background-color: #1a1a1a; /* Dark background */
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                    color: #e0e0e0;
                }
                .container {
                    background-color: #2c2c2c;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                    text-align: center;
                }
                h1 {
                    color: #ff5252; /* Vibrant red for error */
                    margin-bottom: 25px;
                    font-size: 2.5em;
                }
                p {
                    font-size: 1.1em;
                    color: #ccc;
                    margin-bottom: 30px;
                }
                .back-button {
                    background-color: #00bcd4; /* A vibrant teal for the button */
                    color: white;
                    padding: 12px 25px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1.1em;
                    text-decoration: none; /* For the <a> tag */
                    transition: background-color 0.3s ease;
                    display: inline-block; /* To allow padding and margin */
                }
                .back-button:hover {
                    background-color: #00aabf;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Access Denied!</h1>
                <p>The password you entered is incorrect. Please try again.</p>
                <a href="/all" class="back-button">Go Back to Password Entry</a>
            </div>
        </body>
        </html>
        """
        return html_content


@app.route('/getData')
def getData():
    content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Access Data</title>
        <style>
            body {
                background-color: #1a1a1a; /* Dark background */
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                color: #e0e0e0;
            }
            .container {
                background-color: #2c2c2c;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                text-align: center;
            }
            h1 {
                color: #00bcd4; /* A vibrant teal for headings */
                margin-bottom: 25px;
                font-size: 2.5em;
            }
            input[type="password"] {
                padding: 12px 20px;
                margin-bottom: 25px;
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #3a3a3a;
                color: #e0e0e0;
                font-size: 1.1em;
                width: 250px;
                box-sizing: border-box;
            }
            button[type="submit"] {
                background-color: #00bcd4; /* Same vibrant teal for button */
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1.1em;
                transition: background-color 0.3s ease;
            }
            button[type="submit"]:hover {
                background-color: #00aabf;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Enter Password for Data Access</h1>
            <form action="/submit" method="post">
                <input type="password" id="password" name="password" placeholder="Enter password" required>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """
    return content


@app.route("/submit", methods=["POST"])
def submit():
    password = request.form.get("password")
    if password == dataPassword:
        # Data Display Page HTML (Pretty)
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume Data</title>
            <style>
                body {
                    background-color: #1a1a1a; /* Dark background */
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: flex-start; /* Align to top for longer content */
                    min-height: 100vh;
                    margin: 0;
                    color: #e0e0e0;
                    padding: 20px 0; /* Add padding for content */
                }
                .container {
                    background-color: #2c2c2c;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                    text-align: left; /* Align text left for readability */
                    max-width: 800px; /* Wider container for data */
                    width: 90%; /* Responsive width */
                    box-sizing: border-box;
                }
                h1 {
                    color: #00e676; /* Vibrant green for success */
                    margin-bottom: 30px;
                    font-size: 2.5em;
                    text-align: center;
                }
                pre { /* Use pre for displaying JSON data cleanly */
                    background-color: #3a3a3a;
                    color: #e0e0e0;
                    padding: 20px;
                    border-radius: 8px;
                    overflow-x: auto; /* Allow horizontal scrolling for long lines */
                    white-space: pre-wrap; /* Wrap long lines */
                    word-wrap: break-word; /* Break words if necessary */
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace; /* Monospaced font for code/data */
                    line-height: 1.5;
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Resume Data</h1>
        """
        try:
            with open(RESUME_JSON, "r") as f:
                data_lines = f.readlines()
            
            try:
                # Try to load as a list of JSON objects (if each line is a JSON object)
                parsed_data = [json.loads(line) for line in data_lines if line.strip()]
                pretty_data = json.dumps(parsed_data, indent=2)
            except json.JSONDecodeError:
                # If not easily parsable as a list of JSON, just show raw lines
                pretty_data = "".join(data_lines)

            html_content += f"<pre>{pretty_data}</pre>"
        except FileNotFoundError:
            html_content += "<p>No resume data found.</p>"
        except Exception as e:
            html_content += f"<p>Error reading data: {e}</p>"

        html_content += """
            </div>
        </body>
        </html>
        """
        return html_content
    else:
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Access Denied</title>
            <style>
                body {
                    background-color: #1a1a1a; /* Dark background */
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    margin: 0;
                    color: #e0e0e0;
                }
                .container {
                    background-color: #2c2c2c;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                    text-align: center;
                }
                h1 {
                    color: #ff5252; /* Vibrant red for error */
                    margin-bottom: 25px;
                    font-size: 2.5em;
                }
                p {
                    font-size: 1.1em;
                    color: #ccc;
                    margin-bottom: 30px;
                }
                .back-button {
                    background-color: #00bcd4; /* A vibrant teal for the button */
                    color: white;
                    padding: 12px 25px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 1.1em;
                    text-decoration: none; /* For the <a> tag */
                    transition: background-color 0.3s ease;
                    display: inline-block; /* To allow padding and margin */
                }
                .back-button:hover {
                    background-color: #00aabf;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Access Denied!</h1>
                <p>The password you entered is incorrect. Please try again.</p>
                <a href="/getData" class="back-button">Go Back to Password Entry</a>
            </div>
        </body>
        </html>
        """
        return html_content


def makeResume(data):
    templateId = int(str(data['selectedTemplateId']))
    obj = maker.Main(data1=data)
    pdf_name = f"{data['name']}_resume.pdf"
    pdf_path = os.path.join(RESUME_DIR, pdf_name)
    return pdf_path


def save_to_json(data):
    return None
    pdf_path = os.path.join(RESUME_DIR, f"{data['name']}_resume.pdf")
    obj = save_data.Main()
    obj.insert_data(data, pdf_path)
    #print("Data saved successfully to mysql")

    msg = f"RESUME WEBSITE \n\nNew resume created for {str(data)}"
    obj = TelegramBot(msg)
    if not (obj.check()):
        try:
            msgNew = f"================RESUME WEBSITE================ \n\nFailed to send message for {str(data['name'])} {str(data['email'])} {str(data['phone'])}"
            newObj = TelegramBot(msgNew)
        except Exception as e:
            TelegramBot("================RESUME WEBSITE================ \n\nError sending message: " + str(e))


@app.route('/api/resume', methods=['POST'])
def receive_resume():
    data = request.get_json()
    #print("\nReceived Resume Data:", data)
    # save_to_json(data)
    # #print("Data is saved successfully in resumesData.json\n")

    try:
        resumePath = makeResume(data)
        #print("Sending resume file : ", resumePath)
        return send_file(resumePath, as_attachment=True), 200
    except Exception as e:
        #print("Error generating resume:", e)
        return jsonify({"error": "Failed to generate resume"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)