# FridaLab by Ross Marks

## Challenges
* Change class challenge_01's variable 'chall01' to: 1
* Run chall02()
* Make chall03() return True
* Send "frida" to chall04()
* Always send "frida" to chall05()
* Run chall06() after 10 seconds with correct value
* Bruteforce check07Pin() then confirm with chall07()
* Change 'CHECK' button text value to 'CONFIRM'

## Tools
Below are the tools that I used to solve the challenges given:
* [Frida](https://frida.re/) (Dynamic Instrumentation Toolkit)
* [MobSF](https://github.com/MobSF/Mobile-Security-Framework-MobSF) / [jadx-gui](https://github.com/skylot/jadx) / [jd-gui](https://github.com/java-decompiler/jd-gui)

## Walkthrough

- TBA

## Full Solutions

```js
if (Java.available){
	Java.perform(function(){
		var chall_1 = Java.use("uk.rossmarks.fridalab.challenge_01");
		chall_1.getChall01Int.overload().implementation = function(v){
			return 1;
		}
		console.log("Chall01 is finished!");
	});

	//Wait until MainActivity is set
	setTimeout(function(){
		Java.perform(function(){
			var main;
			Java.choose("uk.rossmarks.fridalab.MainActivity",{
				onMatch: function(instance){
					console.log(instance.toString());
			 		main = instance;
			 	},
			 	onComplete: function(){}
			 });
			main.chall02();
			console.log("Chall02 is finished!");

			//Hook the instance public method and change the retval to True
			main.chall03.overload().implementation = function(v){
				return true;
			}
			console.log("Chall03 is finished");

			main.chall04("frida");
			console.log("Chall04 is finished");

			var new_str = Java.use("java.lang.String");
			main.chall05.overload("java.lang.String").implementation = function(x){
				var strstr = new_str.$new("frida");
				var ret = this.chall05(strstr);
				console.log("Chall05 is finished");
				return ret;
			}
			var chall07 = Java.use("uk.rossmarks.fridalab.challenge_07");
			for (var numb = 1000; numb <= 9999; numb += 1){
				if(chall07.check07Pin(numb.toString())){
					console.log("Correct pin is : " + numb.toString());
					main.chall07(numb.toString());
					console.log("Chall07 is finished!");
					break;
				}
			}

			var buttons = Java.use("android.widget.Button");
			var findid = main.findViewById(2131165231);
			//console.log(typeof findid);
			var caster = Java.cast(findid,buttons);
			var newstr = Java.use("java.lang.String");
			caster.setText(newstr.$new("Confirm"));
			console.log("Chall08 is finished!");

		});

	},3000);

	//chall06
	setTimeout(function(){
		Java.perform(function(){
			var cha6 = Java.use("uk.rossmarks.fridalab.challenge_06");
			cha6.addChall06.overload('int').implementation = function(v){
				console.warn("Check/Confirm now!");
				Java.choose("uk.rossmarks.fridalab.MainActivity",{
				onMatch: function(instance){
					instance.chall06(cha6.chall06.value);
			 	},
			 	onComplete: function(){}
			 });
			}
			console.log("Chall06 is finished!");
		});
	 },10000);

}else{
	console.log("Java is not available yet");
}
```
## CLI Command
`frida -U --no-pause -l fridascript.js -f uk.rossmarks.fridalab`
