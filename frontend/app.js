const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('message-input');

let sessionId = sessionStorage.getItem('sessionId');
if (!sessionId) {
  sessionId = crypto.randomUUID();
  sessionStorage.setItem('sessionId', sessionId);
}

function addMessage(role, text) {
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return div;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  input.value = '';

  addMessage('user', message);
  const assistantDiv = addMessage('assistant', '');

  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    assistantDiv.textContent += decoder.decode(value, { stream: true });
    chat.scrollTop = chat.scrollHeight;
  }
});