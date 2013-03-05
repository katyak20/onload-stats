
var is_safari = (document.childNodes)&&(!document.all)&&(!navigator.taintEnabled)&&(!navigator.accentColorName)?true:false; 

function initFrameSynchronization() {
	initVar = setInterval("synchronizeFrames()", 5);
}

function initFrameSizes() {
	if (is_safari || document.body.scrollWidth<900) contractframes();
}

function synchronizeFrames() {	
	if (document.all) {
		var scrollTop = window.top.frames["MASSGRID_CENTER_RIGHT"].document.body.scrollTop;
		var scrollLeft =  window.top.frames["MASSGRID_CENTER_RIGHT"].document.body.scrollLeft;
		var scrollTopB =  window.top.frames["MASSGRID_CENTER_LEFT"].document.body.scrollTop;
		var scrollLeftB = window.top.frames["MASSGRID_CENTER_LEFT"].document.body.scrollLeft;
		var scrollTopC =  window.top.frames["MASSGRID_TOP_RIGHT"].document.body.scrollTop;
		var scrollLeftC = window.top.frames["MASSGRID_TOP_RIGHT"].document.body.scrollLeft;
	}
	else {
		var scrollTop = MASSGRID_CENTER_RIGHT.pageYOffset;
		var scrollLeft = MASSGRID_CENTER_RIGHT.pageXOffset;
		var scrollTopB = MASSGRID_CENTER_LEFT.pageYOffset;
		var scrollLeftB = MASSGRID_CENTER_LEFT.pageXOffset;
		var scrollTopC = MASSGRID_TOP_RIGHT.pageYOffset;
		var scrollLeftC = MASSGRID_TOP_RIGHT.pageXOffset;
	}
	MASSGRID_CENTER_LEFT.scrollTo (scrollLeftB, scrollTop);
	MASSGRID_TOP_RIGHT.scrollTo (scrollLeft, scrollTopC);
	
}

function expandframes(thisObj) {
	if (document.all) document.getElementById('MASSGRID_CENTER_RIGHT').width="100%";
	document.getElementById('MASSGRID_TOP_RIGHT').width="100%";
	if (!document.all || is_safari) {
		document.getElementById('MASSGRID_CENTER_RIGHT').width=document.getElementById('MASSGRID_TOP_RIGHT').offsetWidth;
	}
}

function contractframes(thisObj) {
	document.getElementById('MASSGRID_CENTER_RIGHT').width="75%";
	document.getElementById('MASSGRID_TOP_RIGHT').width="75%";
	if (!document.all) {
		document.getElementById('MASSGRID_CENTER_RIGHT').width=document.getElementById('MASSGRID_TOP_RIGHT').offsetWidth;
	}
}	

function adjustFrame(frame) {
	if (document.all || is_safari) {
		var w = frame.document.body.scrollWidth;
		if (document.all) document.all[frame.name].width = w;
		if (!document.all) document.getElementById(frame.name).width = w;
	}
	else if (document.getElementById) {
		var w = frame.document.documentElement.offsetWidth;
		document.getElementById(frame.name).width = w;
	}
}

function adjustData() {
	intS= document.f.s.options[document.f.s.selectedIndex].value;
	intR= document.f.r.options[document.f.r.selectedIndex].value;
	intC= document.f.c.options[document.f.c.selectedIndex].value;
	location.href="../grid1/?s="+intS+"&r="+intR+"&c="+intC;
}