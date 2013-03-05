function printpreview()
{
if (navigator.appName == "Microsoft Internet Explorer")

{
var OLECMDID = 7;
/* OLECMDID values:
* 6 - print
* 7 - print preview
* 1 - open window
* 4 - Save As
*/
var PROMPT = 1; // 2 DONTPROMPTUSER
var WebBrowser = '<OBJECT ID="WebBrowser1" WIDTH=0 HEIGHT=0 CLASSID="CLSID:8856F961-340A-11D0-A96B-00C04FD705A2"></OBJECT>';
document.body.insertAdjacentHTML('beforeEnd', WebBrowser);
WebBrowser1.ExecWB(OLECMDID, PROMPT);
WebBrowser1.outerHTML = "";
}
else {
window.print();
}
}


function disableHref(enabledId){

 try{
	var input = document.getElementsByTagName("a");
	var reserveObj = document.getElementById(enabledId);
	var count = input.length;
	
	for(var i =0; i < count; i++){
		var obj = input[i];
		
		if (obj.id != reserveObj.id) {
			obj.removeAttribute("href"); 
			obj.removeAttribute("onclick");
		}
		obj.style.cursor='wait';
	}
  
 	
	} catch(Exc){
	}
	
	change('progressBar','show');
	
	return true;
}

 function change(id, newClass) {
	var identity=document.getElementById(id);
	identity.className = newClass;
	
	/*
	if(identity.className == "hide") {
		identity.className ="show"; 
	
	} else {
		identity.className = "hide";
	}
	*/
}

