from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy_txtar():
    txtar_content = request.data.decode('utf-8')
    home_dir = os.path.expanduser('~')
    
    if not txtar_content:
        return jsonify({"error": "Empty content"}), 400
    
    try:
        # Suoritetaan tx-komento kotihakemistossa
        process = subprocess.Popen(
            ['/home/ubuntu/bin/tx'], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True,
            cwd=home_dir
        )
        stdout, stderr = process.communicate(input=txtar_content)
        
        return jsonify({
            "status": "success",
            "log": stdout,
            "error_log": stderr
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
