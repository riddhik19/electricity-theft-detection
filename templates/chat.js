// FIXED Chat - Vanilla JS only (no ES6, IE11 compatible)
function sendChat() {
    var input = document.getElementById('chat-input');
    var messages = document.getElementById('chat-messages');
    var query = input.value;
    query = query.replace(/^\\s+|\\s+$/g, '');

    if (query.length === 0) return;

    // User message
    var userDiv = document.createElement('div');
    userDiv.className = 'd-flex justify-content-end mb-2';
    userDiv.innerHTML = '<div class=\\"bg-primary text-white p-2 rounded-pill small\\" style=\\"max-width: 75%; word-break: break-word;\\">You: ' + query + '</div>';
    messages.appendChild(userDiv);

    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    var btn = document.getElementById('chat-send-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class=\\"fas fa-spinner fa-spin\\"></i> Sending...';

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/chat', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            btn.disabled = false;
            btn.innerHTML = '<i class=\\"fas fa-paper-plane\\"></i> Send';

            var responseText = xhr.responseText;
            var data;
            try {
                data = JSON.parse(responseText);
            } catch(e) {
                data = {response: 'Server error. Try again.'};
            }

            var botDiv = document.createElement('div');
            botDiv.className = 'd-flex mb-3';
            botDiv.innerHTML = '<div class=\\"feature-icon me-2 bg-secondary\\" style=\\"width:40px;height:40px;font-size:1rem;\\"><i class=\\"fas fa-robot\\"></i></div><div class=\\"flex-grow-1\\"><div class=\\"bg-light p-3 rounded border\\" style=\\"border-left: 3px solid var(--secondary-color); white-space: pre-wrap;\\">' + (data.response || 'No response') + '</div></div>';
            messages.appendChild(botDiv);
            messages.scrollTop = messages.scrollHeight;
        }
    };
    xhr.onerror = function() {
        btn.disabled = false;
        btn.innerHTML = '<i class=\\"fas fa-paper-plane\\"></i> Send';
        var errorDiv = document.createElement('div');
        errorDiv.className = 'd-flex mb-3';
        errorDiv.innerHTML = '<div class=\\"feature-icon me-2 bg-danger\\" style=\\"width:40px;height:40px;font-size:1rem;\\"><i class=\\"fas fa-exclamation-triangle\\"></i></div><div class=\\"flex-grow-1\\"><div class=\\"bg-light p-3 rounded border text-danger\\" style=\\"border-left: 3px solid var(--danger-color);\\">Network error. Check server.</div></div>';
        messages.appendChild(errorDiv);
        messages.scrollTop = messages.scrollHeight;
    };
    xhr.send(JSON.stringify({query: query}));
}

// Event listeners
if (document.addEventListener) {
    document.addEventListener('DOMContentLoaded', function() {
        var sendBtn = document.getElementById('chat-send-btn');
        var input = document.getElementById('chat-input');
        if (sendBtn) {
            sendBtn.onclick = sendChat;
        }
        if (input) {
            input.onkeypress = function(e) {
                if (e.keyCode === 13) {
                    sendChat();
                    return false;
                }
            };
        }
    });
}

