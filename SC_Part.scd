s.boot
NetAddr.localAddr

(
	~currentPath = PathName(thisProcess.nowExecutingPath).parentPath;
	~osc_config = (~currentPath ++ "config/osc_config.json").parseYAMLFile;
	~sc_address = NetAddr(~osc_config["supercollider"]["ip"], ~osc_config["supercollider"]["port"]);
	~processing_address = NetAddr(~osc_config["processing"]["ip"], ~osc_config["processing"]["port"]);
	~python_address = NetAddr(~osc_config["python"]["ip"], ~osc_config["python"]["port"]);
)


~python_address = NetAddr("127.0.0.1", 12000);



OSCdef(\sc_listener, {
	arg msg;
	var path, time_pos;
	path = msg[1];
	time_pos = msg[2];
	path.postln;
	time_pos.postln;
}, "/data"
).add;


(
	Routine({
		10.do({ arg i;
			var feature, valor;
			feature = ["centroid", "flatness"].choose;
			if(feature == "centroid",{
				valor = rrand(2000,6000);
			}, {
				valor = rrand(0.00, 1.0);
			});
			~python_address.sendMsg("/data", feature, valor);
		});
	}).play
)
