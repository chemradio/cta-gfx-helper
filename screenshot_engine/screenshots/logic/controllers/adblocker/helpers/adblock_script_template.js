function getDomain() {
	return window.location.hostname;

	let url = window.location.href;
	let parsedUrl = url
		.replace('https://', '')
		.replace('http://', '')
		.replace('www.', '');
	let domain = parsedUrl
		.slice(
			0,
			parsedUrl.indexOf('/') == -1
				? parsedUrl.length
				: parsedUrl.indexOf('/')
		)
		.slice(
			0,
			parsedUrl.indexOf('?') == -1
				? parsedUrl.length
				: parsedUrl.indexOf('?')
		);
	return domain;
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
	// get domain
	let domain = getDomain();

	// get ads dom names, classes, ids, etc.
	let elementNames = adsDatabase[domain];

	// get elements
	let elements = gatherElements(elementNames);

	// disable elements
	removeAds(elements);
}

// main()
