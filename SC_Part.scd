s.boot
NetAddr.localAddr

(
	~currentPath = PathName(thisProcess.nowExecutingPath).parentPath;
	~osc_config = (~currentPath ++ "osc_config.json").parseYAMLFile;
	~sc_address = NetAddr(~osc_config["supercollider"]["ip"], ~osc_config["supercollider"]["port"]);
	~processing_address = NetAddr(~osc_config["processing"]["ip"], ~osc_config["processing"]["port"]);
	~python_address = NetAddr(~osc_config["python"]["ip"], ~osc_config["python"]["port"]);
)

SynthDef(\sin, {
	arg freq;
	var senal;
	senal = SinOsc.ar(freq: freq, phase: 0, mul: 1, add: 0 );
	Out.ar(0, senal);
}).add;

~so1 = Synth(\sin, [\freq, 400]);

OSCdef(\sc_listener, {
	arg msg;
	msg[1].postln;
    //~so1.set(\freq,msg[1].linlin(0,1,200,1000));
	//~processing_address.sendMsg("/", msg[1].linlin(0,1, 0, 255).asInteger, 100, 100);
}, '/control1'
).add;



(
	//test python server
	Routine({
		(0..1000).do({ arg i;
			~python_address.sendMsg("/filter", i);
			~python_address.sendMsg("/volume", i + 100);
			~python_address.sendMsg("/logvolume", i + 1000);
			0.001.wait;
		});
	}).play
)
