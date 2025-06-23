document.addEventListener("keyup", function(event) {
	if (event.keyCode === 13) {
		event.preventDefault();
		calculateSolution();
	}
})

function addOption (parent, val) {
	let newOption = parent.appendChild(document.createElement("option"));
	newOption.value = val;
	newOption.innerHTML = val.toUpperCase();
}

function createSelect (values) {
	let container = document.createElement("td");
	let selectElement = container.appendChild(document.createElement("select"));
	for (let i = 0;i < values.length;i++) {
		addOption(selectElement, values[i]);
	}
	return container;
}

function createHeader (row, values) {
	for (let i = 0;i < values.length;i++) {
		let header = document.createElement("th");
		if (values[i] == "Value") {
			header.setAttribute("colspan", "2");
		}
		header.innerHTML = values[i];
		row.appendChild(header);
	}
}

function addStep (ability) {
	let table = ability.parentElement.parentElement.parentElement;
	let newRow = document.createElement("tr");

	let teamInput = createSelect(["me", "opponent"]);
	let targetInput = createSelect(["broadcast", "player_unicast", "target_unicast", "random_unicast", "self_unicast"]);
	let commandInput = createSelect(["set", "increase", "decrease"]);
	let variableInput = createSelect(["damage", "hp", "mp", "attack", "defense", "speed"]);
	let valueInput = createSelect(["default", "current", "other"]);

	let otherValueInput = document.createElement("td");
	otherValueInput.appendChild(document.createElement("input"));

	let removeContainer = document.createElement("td");
	let removeButton = document.createElement("button");
	removeButton.innerHTML = "-";
	removeButton.setAttribute("onclick", "deleteRow(this)");
	removeContainer.appendChild(removeButton);

	newRow.appendChild(teamInput);
	newRow.appendChild(targetInput);
	newRow.appendChild(commandInput);
	newRow.appendChild(variableInput);
	newRow.appendChild(valueInput);
	newRow.appendChild(otherValueInput);
	newRow.appendChild(removeContainer);

	table.children[table.children.length - 1].before(newRow);
}

function addAbility (ability) {
	let table = ability.parentElement.parentElement.parentElement;
	let newRow = document.createElement("tr");

	let nameInput = document.createElement("td");
	nameInput.appendChild(document.createElement("input"));

	let costInput = document.createElement("td");
	costInput.appendChild(document.createElement("input"));

	let triggerInput = document.createElement("td");
	let triggerCheckbox = triggerInput.appendChild(document.createElement("input"));
	triggerCheckbox.type = "checkbox";
	triggerCheckbox.style = "width: 24px; height: 24px;";

	let commandInput = createSelect(["set", "increase", "decrease", "null"]);
	let variableInput = createSelect(["damage", "hp", "mp", "attack", "defense", "speed", "null"]);

	let stepsInput = document.createElement("td");
	let stepsTable = stepsInput.appendChild(document.createElement("table"));
	stepsTable = stepsTable.appendChild(document.createElement("tbody"));
	let stepsHeader = stepsTable.appendChild(document.createElement("tr"));
	createHeader(stepsHeader, ["Team", "Target", "Command", "Variable", "Value"]);
	let stepsNewRow = stepsTable.appendChild(document.createElement("tr"));
	let stepsAddButtonContainer = stepsNewRow.appendChild(document.createElement("td"));
	stepsAddButtonContainer.setAttribute("colspan", "7");
	let stepsAddButton = stepsAddButtonContainer.appendChild(document.createElement("button"));
	stepsAddButton.style = "width: 100%";
	stepsAddButton.innerHTML = '+';
	stepsAddButton.setAttribute("onclick", "addStep(this)");

	let removeContainer = document.createElement("td");
	let removeButton = document.createElement("button");
	removeButton.innerHTML = "-";
	removeButton.setAttribute("onclick", "deleteRow(this)");
	removeContainer.appendChild(removeButton);

	newRow.appendChild(nameInput);
	newRow.appendChild(costInput);
	newRow.appendChild(triggerInput);
	newRow.appendChild(commandInput);
	newRow.appendChild(variableInput);
	newRow.appendChild(stepsInput);
	newRow.appendChild(removeContainer);

	table.children[table.children.length - 1].before(newRow);
}

function deleteRow (rowToDelete) {
	rowToDelete.parentElement.parentElement.remove();
}

function parseStep (elements) {
	return [elements[0].value, elements[1].value, elements[2].value, elements[3].value, elements[4].value == "other" ? elements[5].value : elements[4].value];
}

function parseSteps (table) {
	let result = [];
	let rows = table.children[0].children;
	for (let i = 1;i < rows.length - 1;i++) {
		let parsed = [];
		for (let element of rows[i].children) {
			parsed.push(element.children[0]);
		}
		result.push(parseStep(parsed));
	}
	return result;
}

function parseAbility (elements) {
	let baseAbility = {
		"name": elements[0].value,
		"cost": elements[1].value,
		"trigger": elements[2].checked ? [elements[3].value == "null" ? null : elements[3].value, elements[4].value == "null" ? null : elements[4].value] : null,
		"packets": parseSteps(elements[5])
	};
	return baseAbility;
}

function parseAbilities () {
	let result = [];
	let table = document.getElementById("abilities").children[0].children;
	for (let i = 1;i < table.length - 1;i++) {
		let parsed = [];
		for (let element of table[i].children) {
			parsed.push(element.children[0]);
		}
		result.push(parseAbility(parsed));
	}
	return result;
}

let hashCode = s => s.split('').reduce((a,b)=>{a=((a<<5)-a)+b.charCodeAt(0);return a&a},0)

function generateJSON () {
	let resultElement = document.getElementById("result");
	baseCharacter = {
		"checksum": hashCode(document.getElementById("name").value).toString(),
		"name": document.getElementById("name").value,
		"image": document.getElementById("img_link").value,
		"HP": document.getElementById("HP").value,
		"MP": document.getElementById("MP").value,
		"attack": document.getElementById("attack").value,
		"defense": document.getElementById("defense").value,
		"speed": document.getElementById("speed").value,
		"abilities": parseAbilities()
	}

	resultElement.value = JSON.stringify(baseCharacter);
	console.log(baseCharacter);
}
