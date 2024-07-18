let socket;
let npc = 'adria';

function connectToNPC() {
    const form = document.getElementById('npc-form');
    const data = new FormData(form);
    npc = data.get('npc');

    socket = new WebSocket(`ws://localhost:8080/${npc}`);

    socket.onopen = function () {
        document.getElementById('output').textContent += `Connected to ${npc}\n`;
    };

    socket.onmessage = function (event) {
        document.getElementById('output').textContent += `${npc}: ${event.data}\n`;
    };

    socket.onclose = function () {
        document.getElementById('output').textContent += `Disconnected from ${npc}\n`;
    };
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value;
    socket.send(message);
    document.getElementById('output').textContent += `You: ${message}\n`;
    input.value = '';
}
