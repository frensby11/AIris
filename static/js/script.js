// Configuración de partículas
particlesJS('particles-js',
    {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": "#ffffff"
            },
            "shape": {
                "type": "circle"
            },
            "opacity": {
                "value": 0.1,
                "random": true
            },
            "size": {
                "value": 3,
                "random": true
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#ffffff",
                "opacity": 0.1,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 1,
                "direction": "none",
                "random": true,
                "straight": false,
                "out_mode": "out",
                "bounce": false
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": true
                },
                "resize": true
            }
        },
        "retina_detect": true
    }
);

document.getElementById('modelo-select').addEventListener('change', function() {
    const selectedModel = this.value;
    axios.post('/cambiar_modelo', { modelo: selectedModel })
        .then(response => {
            if (response.data.success) {
                alert(response.data.mensaje);
            }
        })
        .catch(error => {
            console.error('Error al cambiar modelo:', error);
        });
});

function addMessage(messageText, isUser, container) {
    const messageDiv = document.createElement('div');
    messageDiv.innerHTML = marked.parse(messageText);

    messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
    
    const copyButton = document.createElement('button');
    copyButton.textContent = 'Copiar';
    copyButton.classList.add('copy-button');
    copyButton.onclick = function() {
        try {
            const tempTextArea = document.createElement('textarea');
            tempTextArea.value = messageText;
            document.body.appendChild(tempTextArea);
            tempTextArea.select();
            tempTextArea.setSelectionRange(0, 99999);

            const successful = document.execCommand('copy');
            document.body.removeChild(tempTextArea);

            if (successful) {
                copyButton.textContent = '¡Copiado!';
                copyButton.classList.add('copied');
                setTimeout(() => {
                    copyButton.textContent = 'Copiar';
                    copyButton.classList.remove('copied');
                }, 1500);
            } else {
                throw new Error('Copia fallida');
            }
        } catch (err) {
            navigator.clipboard.writeText(messageText).then(() => {
                copyButton.textContent = '¡Copiado!';
                copyButton.classList.add('copied');
                setTimeout(() => {
                    copyButton.textContent = 'Copiar';
                    copyButton.classList.remove('copied');
                }, 1500);
            }).catch(() => {
                alert('No se pudo copiar el texto. Por favor, cópielo manualmente.');
            });
        }
    };

    messageDiv.appendChild(copyButton);
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatContainer = document.getElementById('chat-container');
    const typingIndicator = document.querySelector('.typing-indicator');
    const message = userInput.value.trim();

    if (message === '') return;

    addMessage(message, true, chatContainer);
    userInput.value = '';
    typingIndicator.style.display = 'block';

    axios.post('/chat', { message: message })
        .then(response => {
            typingIndicator.style.display = 'none';

                if (response.data.success) {
                    addMessage(response.data.response, false, chatContainer)
                } else {
                    console.error('Error en la respuesta del chatbot');
                }
            })
            .catch(error => {
                typingIndicator.style.display = 'none';
                console.error('Error al enviar mensaje:', error);
            });
    }

    document.getElementById('user-input').addEventListener('keyup', function(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });