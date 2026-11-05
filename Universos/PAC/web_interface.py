from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import threading
import os
from datetime import datetime

app = Flask(__name__)

# Estado de los scrapings
scraping_status = {}

def run_scraping(script_name, script_id):
    """Ejecuta un scraping en segundo plano"""
    try:
        scraping_status[script_id] = {"status": "running", "start_time": datetime.now()}
        result = subprocess.run(['python', script_name], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            scraping_status[script_id] = {
                "status": "completed", 
                "end_time": datetime.now(),
                "output": result.stdout
            }
        else:
            scraping_status[script_id] = {
                "status": "error", 
                "end_time": datetime.now(),
                "error": result.stderr
            }
    except Exception as e:
        scraping_status[script_id] = {
            "status": "error", 
            "end_time": datetime.now(),
            "error": str(e)
        }

@app.route('/')
def index():
    return render_template('index.html', status=scraping_status)

@app.route('/run/<script_name>')
def run_script(script_name):
    script_id = f"{script_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    thread = threading.Thread(target=run_scraping, args=(script_name, script_id))
    thread.start()
    return redirect(url_for('index'))

@app.route('/status')
def get_status():
    return jsonify(scraping_status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)