function validateParametersForm(fields) {
	for (var i = 0; i < fields.length; i++) {
		console.log("hit");
		var val_in_field = document.forms["evaluate_inputs"][fields[i].name].value;
		if (val_in_field == null ||| val_in_field == "") {
			alert("Please fill all required data fields!");
      		return;
		}
	}
  }