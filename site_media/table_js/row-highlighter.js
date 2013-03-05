function hl_row () {
	this.style.backgroundColor = "#ffe2ac";
	document.getElementById(this.id.replace("_row","_row_fix")).style.backgroundColor = "#ffe2ac";
}
function uhl_row () {
	this.style.backgroundColor = "";
	document.getElementById(this.id.replace("_row","_row_fix")).style.backgroundColor = "";
}
function hl_row_fix () {
	this.style.backgroundColor = "#ffe2ac";
	document.getElementById(this.id.replace("_fix","")).style.backgroundColor = "#ffe2ac";
}
function uhl_row_fix () {
	this.style.backgroundColor = "";
	document.getElementById(this.id.replace("_fix","")).style.backgroundColor = "";
}
jQuery(document).ready(function(){
	jQuery(".hl_row").mouseover(hl_row).mouseout(uhl_row);
});
jQuery(document).ready(function(){
	jQuery(".hl_row_fix").mouseover(hl_row_fix).mouseout(uhl_row_fix);
});