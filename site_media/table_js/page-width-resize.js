function resize(pluginParameter,pcode,languageParameter,ajax){

	// Check Window Height and Width to see according to which to calculate the box size
	var winWidth = Window.getScrollWidth();
	var winHeight = (Window.getHeight()) ? Window.getHeight(): Window.getScrollHeight();

	var avWidth = ($("rightColumn")) ? setWidth(["rightColumn"]) - 40: winWidth;
	var avHeight = ($("header")) ? setHeight(["header"]) - 130 : winHeight;
	// Element to set the Dimensions
	var wrapperDiv = $("leftColumn");
	
	if (((avWidth*3)/4) <= avHeight) {
		var BaseDivPadding = wrapperDiv.getStyle('padding-left').toInt() +  wrapperDiv.getStyle('padding-right').toInt();
		var BaseDivMargin = wrapperDiv.getStyle('margin-left').toInt() +  wrapperDiv.getStyle('margin-right').toInt();
		
		divWidth = avWidth - (((BaseDivPadding) ? BaseDivPadding: 0) + ((BaseDivMargin) ? BaseDivMargin : 0));
		divHeight = setRatioHeight(divWidth);
	} else {
		var BaseDivPadding = wrapperDiv.getStyle('padding-top').toInt() +  wrapperDiv.getStyle('padding-bottom').toInt();
		var BaseDivMargin = wrapperDiv.getStyle('margin-top').toInt() +  wrapperDiv.getStyle('margin-bottom').toInt();
		
		divHeight = avHeight - (((BaseDivPadding) ? BaseDivPadding: 0) + ((BaseDivMargin) ? BaseDivMargin : 0));
		divWidth = setRatioWidth(divHeight);
	}
	
	if ((divWidth < 432) || (divHeight < 332)){
		divWidth = 432;
		divHeight = 332;
	}
	
	wrapperDiv.setStyles({width: divWidth + 'px', height: divHeight + 'px'});
		
	resizeWidth=(divWidth-4); // margin of SVGImport element
	resizeHeight=setRatioHeight(resizeWidth);//(divHeight-32);
	
	if ($('SVGimport')) {
		//var SVGmap = getSVGContainer();
		//SVGmap.setAttribute('width', resizeWidth);
		//SVGmap.setAttribute('height', resizeHeight);
		var SVGmaps = document.getElementsByName('graphic');
		for (var i = 0; i < SVGmaps.length; i++) {
			SVGmaps[i].setAttribute('width', resizeWidth);
			SVGmaps[i].setAttribute('height', resizeHeight);
		}
	}
		
		
	if(ajax=='true'){
	var today = new Date();
 	cacheStr="&r="+today;
		
	//if ($('SVGimport')) {
	//	var SVGmap = document.getElementsByName('graphic')[0];
	//	SVGmap.setAttribute('width', resizeWidth);
	//	SVGmap.setAttribute('height', resizeHeight);
	//}
	
	retrieveURLWithoutForm('./resizeNavigation.do?resizeWidth='+resizeWidth+'&resizeHeight='+resizeHeight+'&pcode='+pcode+'&language='+languageParameter+'&plugin='+pluginParameter+cacheStr);
	
	}
	 
}

function setTableHeight(){
	// Check Window Height
	var winHeight = (Window.getHeight()) ? Window.getHeight(): Window.getScrollHeight();

	var avHeight = ($('header')) ? setHeight(['header','tableheader','copyrights','legalNotice','footer','dimension']) : winHeight;
	// Element to set the Dimensions
	//var wrapperDiv = $('ScrollTableID');
	var wrapperDiv = $('container');
	//var wrapperDivBody = wrapperDiv.getElementsByTagName('table')[0].tBodies[0];
	var wrapperDivBody = $('scrollx');//.tBodies[0];
	var BaseDivPadding = wrapperDiv.getStyle('padding-top').toInt() +  wrapperDiv.getStyle('padding-bottom').toInt();
	var BaseDivMargin = wrapperDiv.getStyle('margin-top').toInt() +  wrapperDiv.getStyle('margin-bottom').toInt();
	
	divHeight = avHeight - (((BaseDivPadding) ? BaseDivPadding : 0) + ((BaseDivMargin) ? BaseDivMargin : 0));
	divHeight = ((divHeight-10) < 240) ? 240 : divHeight-10;
	wrapperDiv.setStyles({height: divHeight.toInt() + 'px'});
	wrapperDivBody.style.height = (divHeight.toInt() - ($('copyrights').offsetHeight + 7 ) - (23) )+ 'px';
}

// Graph Resize Method
function setGraphDimension(side){
	// Variable side should be 1 (width)  or 2 (height)
	var side = (side) ? side.toInt() : 1;
	// Check Window Height
	var winWidth = Window.getScrollWidth();
	var winHeight = (Window.getHeight()) ? Window.getHeight(): Window.getScrollHeight();

	var avWidth = ($("rightColumn")) ? setWidth(["rightColumn"]): winWidth;
	var avHeight = ($("header")) ? setHeight(["header"]) : winHeight;
	
	// Element to set the Dimensions
	var wrapperDiv = $('SVGimport');
	
	if (side == 2){
		var BaseDivPadding = wrapperDiv.getStyle('padding-top').toInt() +  wrapperDiv.getStyle('padding-bottom').toInt();
		var BaseDivMargin = wrapperDiv.getStyle('margin-top').toInt() +  wrapperDiv.getStyle('margin-bottom').toInt();
		
		divHeight = avHeight - (BaseDivPadding + BaseDivMargin);
		divHeight = ((divHeight-12) < 348) ? 348 : divHeight-12;
		wrapperDiv.setStyles({height: divHeight + 'px'});
	} else {
		var BaseDivPadding = wrapperDiv.getStyle('padding-left').toInt() +  wrapperDiv.getStyle('padding-right').toInt();
		var BaseDivMargin = wrapperDiv.getStyle('margin-left').toInt() +  wrapperDiv.getStyle('margin-right').toInt();
		
		var GraphObjWidth = parseInt(document.getElementsByName('graphObj')[0].width);
		
		divWidth = (avWidth - (BaseDivPadding + BaseDivMargin))-40;
		
		// If the Graph with is smaller then the result we set it to its width plus an extra 10 pixels
		divWidth = (divWidth < GraphObjWidth) ? divWidth : GraphObjWidth + 10;
		
		wrapperDiv.setStyles({width: divWidth + 'px'});
		$('leftColumn').setStyles({width: divWidth + 'px'});
	}
}

// JavaScript Document
// Calculate and Return the Height of the element in relation to the width
var setRatioHeight = function(elWidth){
	divHeight = ( elWidth * 3 ) / 4;
	return parseInt(divHeight);
}
// Calculate and Return the Height of the element in relation to the width
var setRatioWidth = function(elHeight){
	divWidth = ( elHeight * 4 ) / 3;
	return parseInt(divWidth);
}

// Calculate and Return the Height of the element
var setHeight = function(subtractedDiv){
	var divHeight = (Window.getHeight()) ? Window.getHeight(): Window.getScrollHeight();
	for (i=0; i < subtractedDiv.length; i++) {
		var ToolBox = $(subtractedDiv[i]);
		if (ToolBox){
			var ToolboxStylesWidth = ToolBox.offsetHeight.toInt();
			var ToolboxStylesMargin = ToolBox.getStyle('margin-top').toInt() + ToolBox.getStyle('margin-bottom').toInt();
			var divHeight = (divHeight - (((ToolboxStylesWidth) ? ToolboxStylesWidth : 0) + ((ToolboxStylesMargin) ? ToolboxStylesMargin : 0)));
		}
	}
	return divHeight.toInt();
}
// Calculate and return the width of the element
var setWidth = function(subtractedDiv){
	var divWidth = Window.getScrollWidth();
	for (i=0; i < subtractedDiv.length; i++) {
		var ToolBox = $(subtractedDiv[i]);
		if (ToolBox){
			var ToolboxStylesWidth = ToolBox.offsetWidth.toInt();
			var ToolboxStylesMargin = ToolBox.getStyle('margin-left').toInt() + ToolBox.getStyle('margin-right').toInt();
			var divWidth = divWidth - (ToolboxStylesWidth + ((ToolboxStylesMargin) ? ToolboxStylesMargin : 0));
		}
	}
	return divWidth.toInt();
}


