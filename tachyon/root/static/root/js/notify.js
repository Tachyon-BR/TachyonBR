// Función que crea y muestra alerta
function showNotification(from, align, msg){
	color = Math.floor((Math.random() * 4) + 1);
	$.notify({
		icon: "nc-icon nc-app",
		message: msg
	},{
		timer: 4000,
		placement: {
			from: from,
			align: align
		}
	});
}

// Función que crea y muestra alerta
function showNotificationSuccess(from, align, msg){
	color = Math.floor((Math.random() * 4) + 1);
	$.notify({
		icon: "fas fa-check-circle",
		message: msg
	},{
		type: 'success',
		timer: 100000,
		placement: {
			from: from,
			align: align
		}
	});
}

// Función que crea y muestra alerta
function showNotificationInfo(from, align, msg){
	color = Math.floor((Math.random() * 4) + 1);
	$.notify({
		icon: "fas fa-info-circle",
		message: msg
	},{
		type: 'info',
		timer: 4000,
		placement: {
			from: from,
			align: align
		}
	});
}

// Función que crea y muestra alerta
function showNotificationWarning(from, align, msg){
	color = Math.floor((Math.random() * 4) + 1);
	$.notify({
		icon: "fas fa-exclamation-triangle",
		message: msg
	},{
		type: 'warning',
		timer: 4000,
		placement: {
			from: from,
			align: align
		}
	});
}

// Función que crea y muestra alerta
function showNotificationDanger(from, align, msg){
	color = Math.floor((Math.random() * 4) + 1);
	$.notify({
		icon: "fas fa-bug",
		message: msg
	},{
		type: 'danger',
		timer: 4000,
		placement: {
			from: from,
			align: align
		}
	});
}

// Función que crea y muestra alerta
function showNotificationModal(from, align, msg, type){
	color = Math.floor((Math.random() * 4) + 1);
	$.notify({
		icon: "fas fa-check-circle",
		message: msg
	},{
		z_index: 3000,
		type: type,
		timer: 4000,
		placement: {
			from: from,
			align: align
		}
	});
}
