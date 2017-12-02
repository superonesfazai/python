/*function move(obj,iTarget){
			clearInterval(obj.timer);
			obj.timer=setInterval(function (){
				var speed=(iTarget-obj.alpha)/6;
				speed=speed>0?Math.ceil(speed):Math.floor(speed);
				if (obj.alpha==iTarget) {
					clearInterval(obj.timer);
				} else{
					obj.alpha+=speed;
					obj.style.filter='alpha(opacity:'+obj.alpha+')';
					obj.style.opacity=obj.alpha/100;
				}
			},30);
		}*/
		function getstyle(obj,name){
			if (obj.currentStyle) {
				return obj.currentStyle[name];
			} else{
				return getComputedStyle(obj,false)[name];
			}
		}
		function startmove(obj,json,fnEnd){
			
			clearInterval(obj.timer);
			
			obj.timer=setInterval(function (){
				for (var attr in json) {
				var cur=0;
				var oStop=true;
				if (attr=='opacity') {
					cur=parseFloat(getstyle(obj,attr))*100;
				} else{
					cur=parseInt(getstyle(obj,attr));
				}
				var speed=(json[attr]-cur)/6;
				speed=speed>0?Math.ceil(speed):Math.floor(speed);
				if (json[attr]!=cur) {
					oStop=false;
				}
				if (oStop) {
					clearInterval(obj.timer);
					if(fnEnd)fnEnd();
				} else{
					if (attr=='opacity') {
						obj.style[attr]=(cur+speed)/100;
						obj.style.filter='alpha(opacity:'+(cur+speed)+')';
					} else{
						obj.style[attr]=cur+speed+'px';
					}
					
				}
			
			}
				},30)
		}
