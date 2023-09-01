function getDomain() {
	return window.location.hostname;
}

function gatherElements(elementNames) {
	let elements = [];
	let elementGroup;

	for (let i = 0; i < elementNames.length; i++) {
		let elementName = elementNames[i];
		try {
			elementGroup = document.querySelectorAll(elementName);
		} catch (e) {
			console.log('Failed to find element', elementName);
			continue;
		}
		elements.push(...elementGroup);
	}
	return elements;
}

function removeAds(elements) {
	let element;
	for (let i = 0; i < elements.length; i++) {
		element = elements[i];

		try {
			element.parentElement.removeChild(element);
		} catch (e) {
			console.log('Failed to remove element:', element);
			continue;
		}
	}
}

function main() {
	let domain = getDomain();
	let elementNames = [adsDatabase['generic']];
	elementNames = [...elementNames, ...(adsDatabase[domain] || [])];
	let elements = gatherElements(elementNames);
	removeAds(elements);
}
