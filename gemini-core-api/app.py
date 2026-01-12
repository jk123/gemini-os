from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    txtar_content = request.data.decode('utf-8')
    home_dir = os.path.expanduser('~')
    tx_path = os.path.join(home_dir, 'bin/tx')
    
    if not txtar_content:
        return jsonify({"status": "error", "message": "Empty content"}), 400
    
    try:
        process = subprocess.Popen(
            [tx_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=home_dir
        )
        stdout, stderr = process.communicate(input=txtar_content)
        
        return jsonify({
            "status": "success",
            "output": stdout.strip(),
            "errors": stderr.strip()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
