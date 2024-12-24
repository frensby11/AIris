import os
import hashlib
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response, send_file
from functools import wraps
from datetime import datetime
import json
import psutil
import csv
from io import StringIO
from collections import defaultdict

# export API_KEY="apikey"
# Configurar la API de Google Generative AI
genai.configure(api_key=os.getenv("API_KEY"))

# Configuración de generación
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Variables globales
current_model_name = 'gemini-1.0-pro'
chat_sessions = {}
user_models = {}
session_messages = defaultdict(list)

# Configuración de autenticación para el panel admin
#export AIRISU="user"
ADMIN_USERNAME = os.getenv("AIRISU")

# export AIRISP="password"
ADMIN_PASSWORD = os.getenv("AIRISP") 

# Configuración de la aplicación
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuraciones de modelos disponibles
AVAILABLE_MODELS = {
    'gemini-pro': 'gemini-pro',
    'gemini-1.5-pro': 'gemini-1.5-pro',
    'gemini-1.0-pro': 'gemini-1.0-pro',
    'tunedModels/aion-xghgsg5gdv5b': 'aion-1.0',
    'gemini-1.5-flash': 'gemini-1.5-flash',
    'gemini-1.5-flash-8b': 'gemini-1.5-flash-8b',
    'gemini-2.0-flash-exp': 'gemini-2.0-flash-exp',
    'gemini-exp-1121': 'gemini-exp-1121',
    'learnml-1.5-pro-experimental': 'learnml-1.5-pro-experimental'
}

# Decorator para autenticación
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != ADMIN_USERNAME or auth.password != ADMIN_PASSWORD:
            return Response(
                'Acceso denegado', 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            )
        return f(*args, **kwargs)
    return decorated

def get_user_identifier():
    user_agent = request.headers.get('User-Agent', '')
    return hashlib.md5(user_agent.encode()).hexdigest()

def create_new_session(user_id):
    if user_id not in chat_sessions:
        model = genai.GenerativeModel(
            model_name=current_model_name,
            generation_config=generation_config
        )
        chat_sessions[user_id] = model.start_chat(history=[])
        user_models[user_id] = current_model_name
        session_messages[user_id] = []

def load_question_count():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as file:
            data = json.load(file)
            return data.get('question_count', 0)
    return 0

def save_question_count(count):
    with open('user_data.json', 'w') as file:
        json.dump({'question_count': count}, file)

# Rutas de la aplicación principal
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent', '').lower()
    if 'Airis' not in user_agent:
        return render_template('403.html', message="Acceso restringido al Samsung A71."), 403
    
    user_id = get_user_identifier()
    create_new_session(user_id)
    
    return render_template('index.html', modelos=AVAILABLE_MODELS)

@app.route('/chat', methods=['POST'])
def chat():
    user_id = get_user_identifier()
    user_message = request.json['message']
    
    try:
        if user_id not in chat_sessions:
            create_new_session(user_id)

        # Comandos especiales
        if user_message.startswith('/'):
            if '/set' in user_message:
                new_model = user_message.split(':')[1].strip()
                if new_model == 'aion-1.0':
                    new_model = 'tunedModels/aion-xghgsg5gdv5b'

                if new_model in AVAILABLE_MODELS:
                    model = genai.GenerativeModel(
                        model_name=new_model,
                        generation_config=generation_config
                    )
                    chat_sessions[user_id] = model.start_chat(history=[])
                    user_models[user_id] = new_model
                    return jsonify({
                        'response': f'Modelo cambiado a {new_model}',
                        'success': True
                    })
                return jsonify({
                    'response': 'Modelo no válido',
                    'success': False
                })

            elif '/sessions' in user_message:
                return jsonify({
                    'response': f'Sesiones activas: {len(chat_sessions)}',
                    'success': True
                })

            elif '/use' in user_message:
                question_count = load_question_count()
                return jsonify({
                    'response': f'Número de preguntas realizadas: {question_count}',
                    'success': True
                })

            elif '/show' in user_message:
                return jsonify({
                    'response': str(AVAILABLE_MODELS),
                    'success': True
                })

        # Procesar mensaje normal
        response = chat_sessions[user_id].send_message(user_message)
        
        # Guardar mensaje en el historial
        timestamp = datetime.now().timestamp() * 1000
        session_messages[user_id].append({
            'role': 'user',
            'content': user_message,
            'timestamp': timestamp
        })
        session_messages[user_id].append({
            'role': 'assistant',
            'content': response.text,
            'timestamp': timestamp
        })

        if not user_message.startswith('/'):
            question_count = load_question_count()
            question_count += 1
            save_question_count(question_count)

        return jsonify({
            'response': response.text,
            'success': True
        })

    except Exception as e:
        return jsonify({
            'response': f'Error: {str(e)}',
            'success': False
        })

# Rutas del panel de administración
@app.route('/admin')
@requires_auth
def admin_panel():
    return render_template('admin.html')

@app.route('/admin/sessions')
@requires_auth
def get_sessions():
    sessions_data = []
    total_messages = 0
    model_stats = {}
    
    for user_id in chat_sessions:
        messages = session_messages[user_id]
        current_model = user_models.get(user_id, current_model_name)
        
        # Estadísticas por modelo
        if current_model not in model_stats:
            model_stats[current_model] = {
                'sessions': 0,
                'messages': 0
            }
        model_stats[current_model]['sessions'] += 1
        model_stats[current_model]['messages'] += len(messages)
        
        last_active = max([msg['timestamp'] for msg in messages]) if messages else 0
        
        session_data = {
            'id': user_id,
            'model': current_model,
            'messageCount': len(messages),
            'lastActive': last_active,
            'messages': messages
        }
        sessions_data.append(session_data)
        total_messages += len(messages)
    
    # Estadísticas del sistema
    system_stats = {
        'cpu_usage': psutil.cpu_percent(),
        'memory_usage': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent
    }
    
    return jsonify({
        'sessions': sessions_data,
        'totalMessages': total_messages,
        'modelStats': model_stats,
        'systemStats': system_stats
    })

@app.route('/admin/session/<session_id>', methods=['DELETE'])
@requires_auth
def delete_session(session_id):
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        del user_models[session_id]
        del session_messages[session_id]
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Session not found'}), 404

@app.route('/admin/session/<session_id>/model', methods=['PUT'])
@requires_auth
def update_session_model(session_id):
    if session_id not in chat_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    data = request.json
    new_model = data.get('model')
    
    if new_model not in AVAILABLE_MODELS:
        return jsonify({'success': False, 'error': 'Invalid model'}), 400
    
    model = genai.GenerativeModel(
        model_name=new_model,
        generation_config=generation_config
    )
    chat_sessions[session_id] = model.start_chat(history=[])
    user_models[session_id] = new_model
    
    return jsonify({'success': True})

@app.route('/admin/export/sessions')
@requires_auth
def export_sessions():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Session ID', 'Model', 'Message Count', 'Last Active'])
    
    for user_id in chat_sessions:
        messages = session_messages[user_id]
        last_active = max([msg['timestamp'] for msg in messages]) if messages else 0
        writer.writerow([
            user_id,
            user_models.get(user_id, current_model_name),
            len(messages),
            datetime.fromtimestamp(last_active/1000).strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'sessions_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/admin/export/session/<session_id>')
@requires_auth
def export_session(session_id):
    if session_id not in chat_sessions:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    export_data = {
        'session_id': session_id,
        'model': user_models.get(session_id, current_model_name),
        'messages': session_messages[session_id]
    }
    
    return send_file(
        StringIO(json.dumps(export_data, indent=2)),
        mimetype='application/json',
        as_attachment=True,
        download_name=f'session_{session_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
