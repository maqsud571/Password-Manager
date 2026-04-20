from flask import Flask, render_template, request, redirect, session, jsonify
import json
import hashlib
from models import (
    init_db, is_first_run, set_initialized, save_credential, get_all_credentials,
    get_credential_by_id, update_credential, delete_credential, check_password_reuse
)
from crypto_utils import encrypt_data, decrypt_data
from password_generator import generate_password
from password_strength import check_password_strength

app = Flask(__name__)
app.secret_key = "super_secret_change_me_production"

init_db()

# Master password hashini saqlash uchun (real appda boshqacha)
MASTER_PASSWORD_HASH = None

def hash_master_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    if is_first_run():
        return redirect('/setup')
    if 'unlocked' not in session:
        return redirect('/lock')
    return redirect('/vault')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    global MASTER_PASSWORD_HASH
    if not is_first_run():
        return redirect('/')
    if request.method == 'POST':
        master_pw = request.form['master_password']
        MASTER_PASSWORD_HASH = hash_master_password(master_pw)
        session['master_password'] = master_pw
        session['unlocked'] = True
        set_initialized()
        return redirect('/vault')
    return render_template('setup.html')

@app.route('/lock', methods=['GET', 'POST'])
def lock():
    global MASTER_PASSWORD_HASH
    if request.method == 'POST':
        master_pw = request.form['master_password']
        if hash_master_password(master_pw) == MASTER_PASSWORD_HASH:
            session['master_password'] = master_pw
            session['unlocked'] = True
            return redirect('/vault')
        else:
            return render_template('lock.html', error="Wrong master password")
    return render_template('lock.html')

@app.route('/logout')
def logout():
    session.pop('unlocked', None)
    session.pop('master_password', None)
    return redirect('/lock')

@app.route('/vault')
def vault():
    if 'unlocked' not in session:
        return redirect('/lock')
    credentials = get_all_credentials()
    decrypted_list = []
    for cred in credentials:
        try:
            decrypted_list.append({
                'id': cred[0],
                'service': cred[1],
                'url': cred[2],
                'username': decrypt_data(cred[3], session['master_password']),
                'password': decrypt_data(cred[4], session['master_password']),
                'notes': cred[5],
                'tags': cred[6],
                'created_at': cred[7]
            })
        except:
            pass
    return render_template('vault.html', credentials=decrypted_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'unlocked' not in session:
        return redirect('/lock')
    if request.method == 'POST':
        service = request.form['service']
        url = request.form['url']
        username = request.form['username']
        password = request.form['password']
        notes = request.form['notes']
        tags = request.form['tags']

        username_enc = encrypt_data(username, session['master_password'])
        password_enc = encrypt_data(password, session['master_password'])

        # Password reuseni tekshirish
        reused = check_password_reuse(password_enc, session['master_password'])
        reuse_warning = None
        if len(reused) > 1:
            reuse_warning = f"Warning: This password is used in {len(reused)} other entries!"

        cred_id = save_credential(service, url, username_enc, password_enc, notes, tags)
        
        if reuse_warning:
            return render_template('add_edit.html', warning=reuse_warning, success=True)
        return redirect('/vault')
    
    return render_template('add_edit.html')

@app.route('/edit/<int:cred_id>', methods=['GET', 'POST'])
def edit(cred_id):
    if 'unlocked' not in session:
        return redirect('/lock')
    
    cred = get_credential_by_id(cred_id)
    if not cred:
        return redirect('/vault')
    
    if request.method == 'POST':
        service = request.form['service']
        url = request.form['url']
        username = request.form['username']
        password = request.form['password']
        notes = request.form['notes']
        tags = request.form['tags']
        
        username_enc = encrypt_data(username, session['master_password'])
        password_enc = encrypt_data(password, session['master_password'])
        
        update_credential(cred_id, service, url, username_enc, password_enc, notes, tags)
        return redirect('/vault')
    
    decrypted_cred = {
        'id': cred[0],
        'service': cred[1],
        'url': cred[2],
        'username': decrypt_data(cred[3], session['master_password']),
        'password': decrypt_data(cred[4], session['master_password']),
        'notes': cred[5],
        'tags': cred[6]
    }
    return render_template('add_edit.html', credential=decrypted_cred, edit_mode=True)

@app.route('/delete/<int:cred_id>')
def delete(cred_id):
    if 'unlocked' not in session:
        return redirect('/lock')
    delete_credential(cred_id)
    return redirect('/vault')

@app.route('/export')
def export():
    if 'unlocked' not in session:
        return redirect('/lock')
    
    credentials = get_all_credentials()
    export_data = []
    for cred in credentials:
        try:
            export_data.append({
                'service': cred[1],
                'url': cred[2],
                'username': decrypt_data(cred[3], session['master_password']),
                'password': decrypt_data(cred[4], session['master_password']),
                'notes': cred[5],
                'tags': cred[6],
                'created_at': cred[7]
            })
        except:
            pass
    
    return jsonify(export_data)

@app.route('/settings')
def settings():
    if 'unlocked' not in session:
        return redirect('/lock')
    return render_template('settings.html')

@app.route('/generate-password', methods=['POST'])
def api_generate():
    data = request.json
    length = data.get('length', 12)
    use_upper = data.get('use_upper', True)
    use_lower = data.get('use_lower', True)
    use_digits = data.get('use_digits', True)
    use_symbols = data.get('use_symbols', True)
    pw = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
    strength = check_password_strength(pw)
    return jsonify({'password': pw, 'strength': strength})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)