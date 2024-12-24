const AVAILABLE_MODELS = {
    'gemini-pro': 'gemini-pro',
    'gemini-1.5-pro': 'gemini-1.5-pro',
    'gemini-1.0-pro': 'gemini-1.0-pro',
    'gemini-1.5-flash': 'gemini-1.5-flash',
    'gemini-1.5-flash-8b': 'gemini-1.5-flash-8b',
    'gemini-2.0-flash-exp': 'gemini-2.0-flash-exp',
    'gemini-exp-1121': 'gemini-exp-1121',
    'learnml-1.5-pro-experimental': 'learnml-1.5-pro-experimental'
};

// Función para cargar las sesiones
async function loadSessions() {
    try {
        const response = await fetch('/admin/sessions');
        const data = await response.json();
        
        // Actualizar estadísticas
        document.getElementById('active-sessions').textContent = data.sessions.length;
        document.getElementById('total-messages').textContent = data.totalMessages;
        document.getElementById('active-models').textContent = new Set(data.sessions.map(s => s.model)).size;

        // Limpiar y recrear la lista de sesiones
        const container = document.getElementById('sessions-container');
        container.innerHTML = '';

        data.sessions.forEach(session => {
            const sessionElement = createSessionElement(session);
            container.appendChild(sessionElement);
        });
    } catch (error) {
        console.error('Error al cargar las sesiones:', error);
    }
}

// Función para crear el elemento de una sesión
function createSessionElement(session) {
    const div = document.createElement('div');
    div.className = 'session-item';
    
    const modelSelect = document.createElement('select');
    modelSelect.className = 'model-select';
    Object.entries(AVAILABLE_MODELS).forEach(([value, label]) => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = label;
        option.selected = session.model === value;
        modelSelect.appendChild(option);
    });

    modelSelect.onchange = async () => {
        try {
            await fetch(`/admin/session/${session.id}/model`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: modelSelect.value })
            });
        } catch (error) {
            console.error('Error al cambiar el modelo:', error);
        }
    };

    div.innerHTML = `
        <span>${session.id}</span>
        <span>${session.messageCount} mensajes</span>
        <span>${new Date(session.lastActive).toLocaleString()}</span>
    `;
    
    div.insertBefore(modelSelect, div.firstChild);

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'action-btn delete';
    deleteBtn.textContent = 'Eliminar';
    deleteBtn.onclick = async () => {
        if (confirm('¿Está seguro de eliminar esta sesión?')) {
            try {
                await fetch(`/admin/session/${session.id}`, {
                    method: 'DELETE'
                });
                loadSessions();
            } catch (error) {
                console.error('Error al eliminar la sesión:', error);
            }
        }
    };

    div.appendChild(deleteBtn);
    return div;
}

// Configurar el botón de actualización
document.getElementById('refresh-btn').onclick = loadSessions;

// Cargar las sesiones inicialmente
loadSessions();

// Actualizar automáticamente cada 30 segundos
setInterval(loadSessions, 5000);