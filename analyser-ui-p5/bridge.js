//inspired by p5js-osc package

var osc = require("node-osc");
var io = require("socket.io")(8081);

var oscServer, oscClient;

var isConnected = false;

console.log("starting osc node bridge...");

io.sockets.on("connection", function(socket) {
  console.log("connection");
  socket.on("config", function(obj) {
    console.log("port", obj.server.port);
    console.log("host", obj.server.host);
    isConnected = true;
    oscServer = new osc.Server(obj.server.port, obj.server.host);
    oscClient = new osc.Client(obj.client.host, obj.client.port);
    oscClient.send("/status", socket.sessionId + " connected");
    oscServer.on("message", function(msg, rinfo) {
      console.log("message in bridge oscServer, msg:", msg, " rinfo:", rinfo);
      socket.emit("message", msg);
    });
    socket.emit("connected", 1);
  });

  socket.on("sendOSC", function(address, value, cb = () => {}) {
    console.log("message in bridge, send to ", address, " : ", value);
    oscClient.send(address, value, cb);
  });

  socket.on("disconnect", function() {
    if (isConnected) {
      oscServer.kill();
      oscClient.kill();
    }
  });
});
