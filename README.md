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
│   │   ├── adria.py
│   │   ├── blacksmith.py
│   │   ├── cain.py
│   │   └── ...
│   ├── js-scripts/
│   │   └── ...
│   ├── compile_scripts.cjs
│   └── server.cjs
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
`npm run start`

### Test the client
Open a different terminal, go back to the root folder and type:
`python serve_webapp.py`
- Firstly select the NPC you wish to talk to and press 'OK'
- Secondly type a message and press 'Send'

### Other remarks

Have fun!
