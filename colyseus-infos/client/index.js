
//import Colyseus from "./colyseus.js";

 console.log('hi');
// custom scene class
class GameScene extends Phaser.Scene {
    constructor() {
        super({ key: 'main' });
        this.client = new Colyseus.Client("ws://localhost:2567");
        this.playerEntities = {};
        this.inputPayload = {
            left: false,
            right: false,
            up: false,
            down: false,
        };
        this.elapsedTime = 0;
        this.fixedTimeStep = 1000 / 60;
    }

    preload() {
        // preload scene
        this.load.image('ship_0001', 'https://cdn.glitch.global/3e033dcd-d5be-4db4-99e8-086ae90969ec/ship_0001.png');
        this.cursorKeys = this.input.keyboard.createCursorKeys();
    }

    async create() {
        console.log("Joining room...");

        try {
            this.room = await this.client.joinOrCreate("my_room");
            console.log("Joined successfully!");

            this.room.state.players.onAdd((player, sessionId) => {
                const entity = this.physics.add.image(player.x, player.y, 'ship_0001');
                this.playerEntities[sessionId] = entity;

                if (sessionId === this.room.sessionId) {
                    // this is the current player!
                    // (we are going to treat it differently during the update loop)
                    this.currentPlayer = entity;

                    // remoteRef is being used for debug only
                    this.remoteRef = this.add.rectangle(0, 0, entity.width, entity.height);
                    this.remoteRef.setStrokeStyle(1, 0xff0000);

                    player.onChange(() => {
                        this.remoteRef.x = player.x;
                        this.remoteRef.y = player.y;
                    });

                } else {
                    // all remote players are here!
                    player.onChange(() => {
                        const { x, y } = player;
                        entity.data = { serverX: x, serverY: y };
                    });
                }
            });

            this.room.state.players.onRemove((player, sessionId) => {
                if (this.playerEntities[sessionId]) {
                    this.playerEntities[sessionId].destroy();
                    delete this.playerEntities[sessionId];
                }
            });

        } catch (e) {
            console.error("Join error", e);
        }
    }

    fixedTick(time, delta) {
        // handle input
        const velocity = 5;
        this.inputPayload.left = this.cursorKeys.left.isDown;
        this.inputPayload.right = this.cursorKeys.right.isDown;
        this.inputPayload.up = this.cursorKeys.up.isDown;
        this.inputPayload.down = this.cursorKeys.down.isDown;
        this.room.send(0, this.inputPayload);

        if (this.inputPayload.left) {
            this.currentPlayer.x -= velocity;

        } else if (this.inputPayload.right) {
            this.currentPlayer.x += velocity;
        }

        if (this.inputPayload.up) {
            this.currentPlayer.y -= velocity;

        } else if (this.inputPayload.down) {
            this.currentPlayer.y += velocity;
        }

        for (let sessionId in this.playerEntities) {
            // do not interpolate the current player
            if (sessionId === this.room.sessionId) {
                continue;
            }

            // interpolate all other player entities
            const entity = this.playerEntities[sessionId];
            const { serverX, serverY } = entity.data;

            entity.x = Phaser.Math.Linear(entity.x, serverX, 0.2);
            entity.y = Phaser.Math.Linear(entity.y, serverY, 0.2);
        }
    }

    update(time, delta) {
        // skip loop if not connected yet.
        if (!this.currentPlayer) { return; }

        this.elapsedTime += delta;
        while (this.elapsedTime >= this.fixedTimeStep) {
            this.elapsedTime -= this.fixedTimeStep;
            this.fixedTick(time, this.fixedTimeStep);
        }
    }
}

// game config
const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#b6d53c',
    parent: 'phaser-example',
    physics: { default: "arcade" },
    pixelArt: true,
    scene: [GameScene],
};

// instantiate the game
const game = new Phaser.Game(config);
