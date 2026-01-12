from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    raw_data = request.data.decode('utf-8')
    tx_path = os.path.expanduser('~/bin/tx')
    
    if "-----BEGIN PGP SIGNED MESSAGE-----" in raw_data:
        with open('/tmp/msg.asc', 'w') as f:
            f.write(raw_data)
        
        # Tarkistetaan allekirjoitus
        verify = subprocess.run(['gpg', '--verify', '/tmp/msg.asc'], capture_output=True)
        
        if verify.returncode != 0:
            return jsonify({"status": "error", "message": "GPG-varmennus epäonnistui! Luvaton komento."}), 403
        
        # Puretaan viesti (poistetaan GPG-kääre)
        content = subprocess.run(['gpg', '--decrypt', '/tmp/msg.asc'], capture_output=True, text=True).stdout
    else:
        # Estetään allekirjoittamattomat komennot nyt kun turva on päällä
        return jsonify({"status": "error", "message": "Virhe: Allekirjoitus puuttuu. Käytä gcommand-työkalua."}), 401

    try:
        process = subprocess.Popen([tx_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(input=content)
        return jsonify({"status": "success", "output": stdout.strip(), "errors": stderr.strip()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
