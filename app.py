from flask import Flask, request, jsonify, render_template
import subprocess
import uuid
import zipfile
import os
import smtplib
from email.message import EmailMessage
import threading
from dotenv import load_dotenv

load_dotenv()

jobs = {}
app = Flask(__name__, template_folder="webpage", static_folder="webpage")
script_name = "102303271.py"
mashup_file = "mashup.mp3"
sender_mail = os.getenv("SENDER_EMAIL")
mail_password = os.getenv("APP_PASSWORD")
smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", "465"))

if not sender_mail or not mail_password:
    print("WARNING: Email credentials not set")
    print("Set SENDER_EMAIL and APP_PASSWORD environment variables")

def create_zip(name, audio):
    zip_file = f"{name}.zip" 
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(audio, arcname=audio)
    return zip_file

def send_mail(recipient, zip_path):
    message = EmailMessage()
    message["Subject"] = "Your Mashup Song Files"
    message["From"] = sender_mail
    message["To"] = recipient
    message.set_content("Hello,\n\nYour mashup is ready and attached.\n\nEnjoy your music!")
    
    with open(zip_path, "rb") as file:
        message.add_attachment(
            file.read(),
            maintype="application",
            subtype="zip",
            filename=os.path.basename(zip_path)
        )
    
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
        smtp.login(sender_mail, mail_password)
        smtp.send_message(message)

def handle_request(data, job_id):
    try:
        artist = data["singer"]
        count = str(data["videos"])
        length = str(data["duration"])
        user_email = data["email"]
        zip_name = artist.replace(" ", "_") + "_mashup"

        print(f"\n{'='*50}")
        print(f"Job: {job_id}")
        print(f"Artist: {artist}, Videos: {count}, Duration: {length}s")
        print(f"{'='*50}\n")

        proc = subprocess.run(["python", script_name, artist, count, length, mashup_file])
        
        print(f"\nProcess finished with code: {proc.returncode}")
        
        if proc.returncode != 0:
            print(f"Process failed")
            jobs[job_id] = "error"
            return
            
        if not os.path.exists(mashup_file):
            print(f"Output not found")
            jobs[job_id] = "error"
            return
        
        file_mb = os.path.getsize(mashup_file) / (1024 * 1024)
        print(f"Created: {file_mb:.2f} MB")
        
        print(f"Creating ZIP: {zip_name}.zip")
        zip_path = create_zip(zip_name, mashup_file)
        
        print(f"Sending to: {user_email}")
        send_mail(user_email, zip_path)
        print(f"Email sent")
        
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        jobs[job_id] = "done"
        print(f"Job {job_id} complete\n")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        jobs[job_id] = "error"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    req_data = request.json
    task_id = str(uuid.uuid4())
    jobs[task_id] = "processing"
    worker = threading.Thread(target=handle_request, args=(req_data, task_id))
    worker.start()
    return jsonify({
        "job_id": task_id,
        "message": "Mashup generation started. Check your email for the ZIP file."
    })

@app.route("/status/<job_id>")
def status(job_id):
    return jsonify({"status": jobs.get(job_id, "unknown")})

if __name__ == "__main__":
    app.run(debug=True)
