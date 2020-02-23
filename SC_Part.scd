NetAddr.localAddr //TODO: que sempre sigui 57120
Server.killAll
s.quit
(
ServerQuit.removeAll;
ServerBoot.removeAll;
ServerTree.removeAll;
Buffer.freeAll(s);

~currentPath = PathName(thisProcess.nowExecutingPath).parentPath;
~osc_config = (~currentPath ++ "config/osc_config.json").parseYAMLFile;
~server_config = (~currentPath ++ "config/server_config.json").parseYAMLFile;
~sc_address = NetAddr(~osc_config["supercollider"]["ip"], ~osc_config["supercollider"]["port"].asInteger);
~processing_address = NetAddr(~osc_config["processing"]["ip"], ~osc_config["processing"]["port"].asInteger);
~python_address = NetAddr(~osc_config["python"]["ip"], ~osc_config["python"]["port"].asInteger);

s.options.sampleRate = ~server_config["sampleRate"].asInteger;
s.latency = ~server_config["latency"].asFloat;
s.options.numOutputBusChannels = ~server_config["numOutputBusChannels"].asInteger;
s.options.blockSize = ~server_config["blockSize"].asInteger;

s.waitForBoot{
	~loadBuffers = {
		arg paths;
		Buffer.freeAll(s);//TODO: netejar buffers de la RAM cada vega que executem aquest codi

		//s.cachedBuffersDo{arg buf; buf.free};
		~buffers = Dictionary.new;
		paths.collect({arg path; ~buffers.put(path, Buffer.readChannel(s, path, channels:[0]))});
		};
	s.sync;

	SynthDef(\granulator,{
		arg bufnum=1, posLectura=0, velocidad = 1, dur=1, pan=0;
		var senal, env;

		senal = PlayBuf.ar(1, bufnum, BufRateScale.kr(bufnum) * velocidad, 1, posLectura);
		senal = Pan2.ar(senal, pan);
		env = EnvGen.ar(Env.sine(dur, 0.1), doneAction: 2);

		OffsetOut.ar(0, senal * env)
		}).add;


	OSCdef.free(\sc_data_listener);
	OSCdef(\sc_data_listener, {
		arg msg;
		var path, start_sample, frame_dur, feature;

		path = msg[1];
		start_sample = msg[2].asInteger;
		frame_dur = msg[3].asFloat;
		feature = msg[4];
		[path, start_sample, frame_dur, feature].postln;

		Synth(\granulator,[
			\bufnum, ~buffers.at(path),
			\posLectura, start_sample,
			\velocidad, 1,
			\dur, frame_dur,
			\pan, 0])
		}, "/data").add;


	OSCdef.free(\audio_path_listener);
	OSCdef(\audio_path_listener, {
		arg msg;
		var paths;
		paths = msg;
		paths.removeAt(0);
		paths.postln;
		~loadBuffers.(paths);
		}, "/audio_paths").add;


	OSCdef.free(\sc_test_listener);
	OSCdef(\sc_test_listener, {
		arg msg;
		msg.postln
		}, "/test").add;



	OSCdef.free(\processing_listener);
	OSCdef(\processing_listener, {
		arg msg;
		msg.postln
		}, "/processing_listener").add;

	s.sync;

	~python_address.sendMsg("/audio_paths")
	}
)



~python_address.sendMsg("/data", "centroid", 1700);
~python_address.sendMsg("/data", "flatness", 0.9);

//RUTINES
{SinOsc.ar}.play
(
	Routine({
		10000.do({ arg i;
			var feature, valor;
			feature = ["centroid"].choose;
			feature.postln;
			if(feature == "centroid",{
				//valor = rrand(3800,4000);
				valor = i + 4000;
				valor.postln;
			}, {
				valor = rrand(0.75, 1.0);
			});
			~python_address.sendMsg("/data", feature, valor);
			rrand(0.1,0.1).wait;
		});
	}).play
)


(
	Routine({
		1000.do({
			~processing_address.sendMsg("/test", rrand(0, 255), rrand(0, 255));
			0.1.wait;
		});
	}).play
)


Buffer.freeAll(s)
s.cachedBuffersDo(s,{arg buffer; buffer.postln});
3.do{s.cachedBuffersDo{arg buf; buf.free}}







//TEST OSC p5
OSCdef.free(\processing_test);
(
OSCdef(\processing_test, {
	arg msg;
	msg.postln
	}, "/test").add;
)
s.sync;

~processing_address.sendMsg("", 222111); //test

~sc_address.sendMsg("/test", 333333); //test SC


















~buffers.at("/Users/Sergi/Documents/SuperCollider/Proyectos/Lluis/Python_SC_Pde/sounds/Baloon_Large_31.wav").play



/// A FER

SynthDef(\playSergi, {
		arg buf=0, vel=1, pos=0, cutFreqLow = 20000, cutFreqHigh = 0, atk=0.001, sus=0.2, rel=0.05, amp=1, pan=0, out=0;
		var senal, env;
		env = Env([0,1,1,0],[atk,sus,rel],[1,0,-1]).kr(2, Impulse.ar(2));
		senal = PlayBuf.ar(1, buf, vel * BufRateScale.kr(buf), startPos:pos, loop: 1);
		senal = senal * env;
		//senal = LPF.ar(senal, cutFreqLow);
		//senal = HPF.ar(senal, cutFreqHigh);
		senal = Pan2.ar(senal, pan, amp);
		OffsetOut.ar(out, senal);
		}).add;

/*
OSCdef(\crear, {
	arg msg;

	Synth(\play, [\buf, ,\vel, 1, \pos, ])

	if (~synths[msg[1]] == nil,
		//{~synths[msg[1]] = Synth(\sine1, [\freq, rrand(2,1000)]).register;}
		{~synths[msg[1]] = Synth(\playSergi, [\buf, rrand(0,0)]).register; ~encendidos = ~encendidos + 1;}

	)

	}, "/data").add;
*/


Pbindef(\bomboProcessing,
		\instrument, \default,
		\search, Pfunc({
			var feature, valor;

		}
		\dur, Prand([1, 0.25, 0.5], inf) / 2,
		\pfunc, Ptime.new,
		\amp, Pwhite(0.25, 1, inf),
		\pan, Pwhite(-0.75, 0.75, inf),
		\prova, Pfunc({
			arg event;
			var ampCercle, posCercle;
			ampCercle = event[\amp].linlin(0.25, 1, 25, 150).asInteger;
			posCercle = event[\pan].linlin(-0.75, 0.75, 100, 500).asInteger;
			~processing.sendMsg("/", posCercle, 180, ampCercle, ampCercle);
			}));

Pbindef.freeAll

Pbindef(\prova_python,
		//\instrument, \default,
		//\search, Pfunc({
		//	var feature, valor;

		//}

		\dur, Pseq([0.5, 0.25, 025], inf) / 2,
		\hola, Pwhite(0.1, 1).trace
		//\pfunc, Ptime.new,
		//\amp, Pwhite(0.25, 1, inf),
		//\pan, Pwhite(-0.75, 0.75, inf),
		\prova, Pfunc({
			//arg event;
			//var ampCercle, posCercle;
			//ampCercle = event[\amp].linlin(0.25, 1, 25, 150).asInteger;
			//posCercle = event[\pan].linlin(-0.75, 0.75, 100, 500).asInteger;
			~python_address.sendMsg("/data", "centroid", rrand(3000, 4000));
			}));

Pbindef(\prova_python).play
