

NetAddr.localAddr

~sc_address = NetAddr("127.0.0.1", 57120);
~processing_address = NetAddr("127.0.0.1", 13000);
~python_address = NetAddr("127.0.0.1", 12000);



SynthDef(\sin, {
	arg freq;
	var senal;
	senal = SinOsc.ar(freq: freq, phase: 0, mul: 1, add: 0 );
	Out.ar(0, senal);
}).add;

~so1 = Synth(\sin, [\freq, 400]);



OSCdef(\sc_listener, {
	arg msg;
	msg.postln;
    ~so1.set(\freq,msg[1].linlin(0,1,200,1000));
	~processing_address.sendMsg("/", msg[1].linlin(0,1, 0, 255).asInteger, 100, 100);
}, '/control1'
).add;




/// Enviar a Python

~python_address.sendMsg("/print", 123456789, 23) //OK
~python_address.sendMsg("/print", [123456789,11,2]) // ?


(
	Routine({
		(0..10000).do({

			arg i;

			~python_address.sendMsg("/filter", i);

			~python_address.sendMsg("/volume", i + 100);

			~python_address.sendMsg("/logvolume", i + 1000);

			0.001.wait;
		});
	}).play
)
