var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 800,
    parent: 'phaser-example',
    pixelArt: true,
    backgroundColor: '#1a1a2d',
    scene: {
        preload: preload,
        create: create
    }
};

var game = new Phaser.Game(config);
/* If the main page is served via https, the WebSocket must be served via
 "wss" (WebSocket Secure) */
var scheme = window.location.protocol == "https:" ? 'wss://' : 'ws://';
var webSocketUri = scheme
    + window.location.hostname
    + (location.port ? ':' + location.port : '')
    + "/game";

// var websocket = new WebSocket(webSocketUri);
var websocket = io.connect(webSocketUri);

websocket.on('my response', function(msg) {
    console.log(msg.data);
});

websocket.on('disconnect', function(event){
    console.log('closed');
});
// websocket.onopen = function () {
//     console.log('Connected');
//     websocket.send("My name is John");
// };
// websocket.onmessage = function (event) {
//     alert(`[message] Data received from server: ${event.data}`);
// };

// websocket.onclose = function (event) {
//     if (event.wasClean) {
//         alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
//     } else {
//         // e.g. server process killed or network down
//         // event.code is usually 1006 in this case
//         alert('[close] Connection died');
//     }
// };
// websocket.onerror = function (e) {
//     console.log('Error (see console)');
//     console.log(e);
// };

function preload() {
    this.load.image('tiles', 'static/assets/tiles-with-esa.png');
    this.load.image('car', 'static/assets/car90.png');
    this.load.tilemapCSV('map', 'static/assets/grid.csv');
    this.load.spritesheet('button', 'static/assets/button.png', { frameWidth: 128, frameHeight: 64 });
}

function create() {
    // Making Button
    var button = this.add.sprite(100, 650, 'button').setFrame(0).setInteractive();
    var disconnect_button = this.add.sprite(100, 750, 'button').setFrame(0).setInteractive();

    // Making Map
    var map = this.make.tilemap({ key: 'map', tileWidth: 32, tileHeight: 32 });
    var tileset = map.addTilesetImage('tiles', null, 32, 32, 1, 2);
    var layer = map.createStaticLayer(0, tileset, 0, 0);

    var player = this.add.image(32 + 16, 32 + 16, 'car');

    //  Left
    this.input.keyboard.on('keydown_A', function (event) {

        var tile = layer.getTileAtWorldXY(player.x - 32, player.y, true);

        if (tile.index === 2) {
            //  Blocked, we can't move
        }
        else {
            player.x -= 32;
            player.angle = 180;
        }

    });

    //  Right
    this.input.keyboard.on('keydown_D', function (event) {

        var tile = layer.getTileAtWorldXY(player.x + 32, player.y, true);

        if (tile.index === 2) {
            //  Blocked, we can't move
        }
        else {
            player.x += 32;
            player.angle = 0;
        }

    });

    //  Up
    this.input.keyboard.on('keydown_W', function (event) {

        var tile = layer.getTileAtWorldXY(player.x, player.y - 32, true);

        if (tile.index === 2) {
            //  Blocked, we can't move
        }
        else {
            player.y -= 32;
            player.angle = -90;
        }

    });

    //  Down
    this.input.keyboard.on('keydown_S', function (event) {

        var tile = layer.getTileAtWorldXY(player.x, player.y + 32, true);

        if (tile.index === 2) {
            //  Blocked, we can't move
        }
        else {
            player.y += 32;
            player.angle = 90;
        }

    });

    // When hovering
    button.on('pointerover', function (e) {
        this.setFrame(1);
    });

    // When moves away
    button.on('pointerout', function (e) {
        this.setFrame(0);
    });

    // When on click
    button.on('pointerdown', function (e) {
        this.setFrame(2);
        websocket.emit('learn_start', { data: 'pointerdown' })
    });

    // When off click
    button.on('pointerup', function (e) {
        this.setFrame(1);
    });
    // When hovering
    disconnect_button.on('pointerover', function (e) {
        this.setFrame(1);
    });

    // When moves away
    disconnect_button.on('pointerout', function (e) {
        this.setFrame(0);
    });

    // When on click
    disconnect_button.on('pointerdown', function (e) {
        this.setFrame(2);
        websocket.emit('my event', {data: 'discon'});
        websocket.close();
    });

    // When off click
    disconnect_button.on('pointerup', function (e) {
        this.setFrame(1);
    });
}
