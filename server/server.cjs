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
        if ( file.endsWith('.js') || file.endsWith('.cjs')) {

            scripts[file] = 'file://' + path.join(dir, file);
        }
    });

    return scripts;
};

const scripts = getScripts(scriptsDir);

console.log('all scripts:------------------');
for (const key in scripts) {

  console.log(key, ':', scripts[key] );
}

wss.on('connection', (ws, req) => {
    const gkey = req.url.slice(1);
	console.log('requested key:',gkey)
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
		    console.log(`Succesfully loaded script: ${gkey}:`);
            ws.on('message', (data) => {
			    const message= data.toString();
                const response = module.process_input(message);
                ws.send(response);
            });

            ws.on('close', () => {
                console.log(`Disconnected from ${gkey}`);
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

console.log('Server is running on ws://localhost:8080');
