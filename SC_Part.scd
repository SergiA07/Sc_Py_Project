NetAddr.localAddr
a = NetAddr("127.0.0.1", 57122)
a.sendMsg("/control1", "autosend")


OSCdef("PythonProva", {
	arg msg;
	msg.postln;
}, '/control1'
).add;

// m.sendMsg("/chat", 84)
OSCFunc.trace(true)

m = NetAddr("127.0.0.1", 12000)
m.sendMsg("/print", 123456789) //OK
m.sendMsg("/print", "123456789") //OK
m.sendMsg("/print", [123456789,11,2])
m.sendMsg("/print", [1002222,3,4])
