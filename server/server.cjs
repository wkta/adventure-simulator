// Enable Babel transpilation for runtime
//require('@babel/register')({
//    presets: ['@babel/preset-env']
//});

const WebSocket = require('ws');
const path = require('path');
const fs = require('fs');


const wss = new WebSocket.Server({ port: 8080 });
const scriptsDir = path.join(__dirname, 'js-scripts');

// Function to dynamically populate the scripts object
const getScripts = (dir) => {
    const scripts = {};
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        if (file.startsWith('npc_') && file.endsWith('.js')) {
            const npcName = file.replace('npc_', '').replace('.js', '');
            scripts[npcName] = 'file://' + path.join(dir, file);
        }
    });

    return scripts;
};

const scripts = getScripts(scriptsDir);

wss.on('connection', (ws, req) => {
    const npc = req.url.slice(1);
    const scriptPath = scripts[npc];

    if (!scriptPath) {
        ws.close();
        return;
    }

    try {
        // Dynamically import the module
        import(scriptPath).then((module) => {
            ws.on('message', (data) => {
			    const message= data.toString();
                const response = module.process_input(message);
                ws.send(response);
            });

            ws.on('close', () => {
                console.log(`Disconnected from ${npc}`);
            });
        }).catch((error) => {
            console.error(`Failed to load script for ${npc}:`, error);
            ws.close();
        });
    } catch (error) {
        console.error(`Failed to run script for ${npc}:`, error);
        ws.close();
    }
});

console.log('Server is running on ws://localhost:8080');
