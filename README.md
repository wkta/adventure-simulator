# Adventure simulator

This is a test.

(expérimentations avec NodeJS +transcrypt)


## Project overview

```
adventure_simulator/
│
├── client/
│   ├── index.html
│   └── script.js
│
├── server/
│   ├── py-scripts/
│   │   ├── npc_adria.py
│   │   ├── npc_blacksmith.py
│   │   ├── npc_cain.py
│   │   ├── npc_robert.py
│   │   └── ...
│   ├── js-scripts/
│   │   └── ...
│   ├── server.cjs
│   └── transpilation.cjs
│
├── README.md
├── requirements.txt
└── serve_webapp
```


## Getting started

### Install requirements
`pip install -r requirements.txt`
`cd server/`
`npm i`

### Compile py scripts and launch the server
`npm run compile`
`npm run game-server`

(for unstable experiments, you can go `npm run evo-server`

### Test the client
Open a different terminal, go back to the root folder and type:
`python run_game.py`
- Firstly select the NPC you wish to talk to and press 'OK'
- Secondly type a message and press 'Send'

### Other remarks

Have fun!
