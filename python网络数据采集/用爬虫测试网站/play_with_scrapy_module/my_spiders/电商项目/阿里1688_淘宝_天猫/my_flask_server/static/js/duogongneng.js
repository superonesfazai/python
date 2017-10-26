		function getstyle(obj,name){
			if (obj.currentStyle) {
				return obj.currentStyle[name];
			} else{
				return getComputedStyle(obj,false)[name];
			}
		}
		
		function startMove(obj,json,fnEnd){
			
				clearInterval(obj.timer);
			obj.timer=setInterval(function (){
				var oStop=true;
				for(var attr in json){
				var cur=0;
				
				if (attr=='opacity') {
					cur=Math.round(parseFloat(getstyle(obj,attr))*100);
				} else{
					cur=parseInt(getstyle(obj,attr));
				}
				
				var speed=(json[attr]-cur)/6;
			speed=speed>0?Math.ceil(speed):Math.floor(speed);
			
			if (cur!=json[attr])
				oStop=false;
			
				if (attr=='opacity') {
					obj.style.filter='alpha(opacity:'+(cur+speed)+')';
					obj.style.opacity=(cur+speed)/100;
				} else{
					obj.style[attr]=cur+speed+'px';
				}
				
			}
				if (oStop) {
					clearInterval(obj.timer);
				if(fnEnd)fnEnd();
				}
			}
			,30);
		}