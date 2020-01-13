NetAddr.localAddr

(
ServerQuit.removeAll;
ServerBoot.removeAll;
ServerTree.removeAll;
Buffer.freeAll;

~currentPath = PathName(thisProcess.nowExecutingPath).parentPath;
~osc_config = (~currentPath ++ "config/osc_config.json").parseYAMLFile;
~analysis_config = (~currentPath ++ "config/analysis_config.json").parseYAMLFile;
~server_config = (~currentPath ++ "config/server_config.json").parseYAMLFile;
~sc_address = NetAddr(~osc_config["supercollider"]["ip"], ~osc_config["supercollider"]["port"].asInteger);
~processing_address = NetAddr(~osc_config["processing"]["ip"], ~osc_config["processing"]["port"].asInteger);
~python_address = NetAddr(~osc_config["python"]["ip"], ~osc_config["python"]["port"].asInteger);

~analysis_data = Dictionary.new;
~analysis_config.keys.asArray.collect({
	arg feature;
	~analysis_data.add(feature.asSymbol -> (fft_size:~analysis_config[feature]["fft_size"],
	 hop_size:~analysis_config[feature]["hop_size"],
	 sample_rate:~analysis_config[feature]["sample_rate"],
	 frame_duration:(~analysis_config[feature]["fft_size"]).asFloat/(~analysis_config[feature]["sample_rate"]).asFloat))
	});

s.options.sampleRate = ~server_config["sampleRate"].asInteger;
s.latency = ~server_config["latency"].asFloat;
s.options.numOutputBusChannels = ~server_config["numOutputBusChannels"].asInteger;
s.options.blockSize = ~server_config["blockSize"].asInteger;

s.waitForBoot{
	~loadBuffers = {
		arg paths;
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
		var path, time_pos, feature;

		path = msg[1];
		time_pos = msg[2];
		feature = msg[3];

		Synth(\granulator,[
			\bufnum, ~buffers.at(path),
			\posLectura, time_pos * ~analysis_data.at(feature).at(\sample_rate).asInteger,
			\velocidad, 1,
			\dur, ~analysis_data.at(feature).at(\frame_duration).asFloat,
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

	}
)

~python_address.sendMsg("/audio_paths")
~python_address.sendMsg("/data", "centroid", 3500);

(
	Routine({
		1000.do({ arg i;
			var feature, valor;
			feature = ["centroid"].choose;
			feature.postln;
			if(feature == "centroid",{
				valor = rrand(2900,4000);
			}, {
				valor = rrand(0.75, 1.0);
			});
			~python_address.sendMsg("/data", feature, valor);
			0.01.wait;
		});
	}).play
)
















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
