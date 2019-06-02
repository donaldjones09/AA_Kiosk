var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab
var currentProgress = 33;

function showTab(n) {
	// This function will display the specified tab of the form ...
	var tabs = document.getElementsByClassName("tab");
	tabs[n].style.display = "block";
}

function nextPrev(n) {
	//verify all fields are filled out
	if (!verifyForm() && n==1) {
		return false;
	}

	// This function will figure out which tab to display
	var tabs = document.getElementsByClassName("tab");
	// Hide the current tab:
	tabs[currentTab].style.display = "none";
	// Increase or decrease the current tab by 1:
	currentTab = currentTab + n;

	// if you have reached the end of the form... :
	if (currentTab >= tabs.length) {
		//...the form gets submitted:
		document.getElementById("regForm").submit();
		return false;
	}
	// Otherwise, display the correct tab:
	showTab(currentTab);

	$(function() {
		currentProgress = Math.round(((currentTab+1)/3)*100);
		$("#signup-progress")
		.css("width", currentProgress + "%")
		.attr("aria-valuenow", currentProgress);
	});
}

function verifyForm(){
	var tabs = document.getElementsByClassName("tab");
	var inputs = tabs[currentTab].getElementsByTagName("input");
	var i;
	var validity = true;

	//check every input
	for(i=0;i<inputs.length;i++) {
		if (inputs[i].value == "") {
			inputs[i].className += " is-invalid";
			validity = false;;
		}
		else {
			var str = inputs[i].className;
			if (str.search("is-invalid") > 0) {
				inputs[i].className = str.replace("is-invalid", "is-valid");
			}
			else {
				inputs[i].className += " is-valid";
			}
		}
	}
	return validity;
}