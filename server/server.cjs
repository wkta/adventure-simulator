const WebSocket = require('ws');
const path = require('path');
const fs = require('fs');

const clients = [];

// ----------------------
// Expose the sendToClients function, to grant access from within transpiled code
global.sendToClients = (message) => {
    clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(message);
        }
    });
};
// ----------------------

const wss = new WebSocket.Server({ port: 8080 });
const scriptsDir = path.join(__dirname, 'js-scripts');

// Function to dynamically populate the scripts object
const getScripts = (dir) => {
    const scripts = {};
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        if (file.endsWith('.js') || file.endsWith('.cjs')) {
            scripts[file] = 'file://' + path.join(dir, file);
        }
    });

    return scripts;
};

const scripts = getScripts(scriptsDir);



// Include the transpiled Python code
import('./js-scripts/mediators.js').then((mediatorModule)=>{

console.log('all scripts:------------------');
for (const key in scripts) {
    console.log(key, ':', scripts[key]);
}

wss.on('connection', (ws, req) => {
    const gkey = req.url.slice(1);
    console.log('requested key:', gkey);
    const scriptPath = scripts[gkey];
    console.log('script:', scriptPath);

    if (!scriptPath) {
        console.log(`not a valid script path`);
        ws.close();
        return;
    }

    try {

					// Dynamically import the module
					import(scriptPath).then((module) => {
							console.log(`connect+script loading OK! Loaded script: ${gkey}:`);
							clients.push(ws);
							ws.on('message', (data) => {
									const message = data.toString();

									// play vs A.I.
									//const response = module.process_input(message);
									// ws.send(response);

									// unpack serialized events
									mediatorModule.NetworkLayer.inject_packed_ev(mediatorModule.nl_obj, message);

									// sync multi clients
									//clients.forEach(client => {
									//    if (client.readyState === WebSocket.OPEN) {
									//        client.send(message);
									//    }
									//});
							});

							ws.on('close', () => {
									console.log(`Disconnected from ${gkey}`);
									const index = clients.indexOf(ws);
									if (index !== -1) {
											clients.splice(index, 1);
									}
							});

					}).catch((error) => {
							console.error(`Failed to load script for ${gkey}:`, error);
							ws.close();
					});


    } catch (error) {
        console.error(`Failed to run script for ${gkey}:`, error);
        ws.close();
    }
});

// Game loop variables
let lastUpdateTime = Date.now();
const updateInterval = 5000; // Update every 5 sec


import('./js-scripts/gamelogic.js').then((logicmodule)=>{

	// Game loop function
	const gameLoop = () => {
			const currentTime = Date.now();
			const deltaTime = currentTime - lastUpdateTime;

			// Update the server state here
			logicmodule.ss_gamelogic_update(currentTime);
			mediatorModule.refresh_event_queue()

			// Notify all clients of the updated state
			/*
			clients.forEach(client => {
					if (client.readyState === WebSocket.OPEN) {
							client.send(JSON.stringify({
									type: 'update',
									deltaTime: deltaTime,
									message: `Update received at ${new Date().toISOString()}`
							}));
					}
			});
			*/

			lastUpdateTime = currentTime;
	};

	// Start the game loop
	setInterval(gameLoop, updateInterval);
	console.log('gameloop started');
});

});
console.log('Server is running on ws://localhost:8080');
