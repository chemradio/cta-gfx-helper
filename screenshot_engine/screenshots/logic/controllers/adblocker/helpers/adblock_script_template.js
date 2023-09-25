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

function removeAdsMedium() {
	// Get all 'span' elements on the page
	let spans = document.getElementsByTagName('span');

	for (let i = 0; i < spans.length; ++i) {
		// Check if they contain the text 'Promoted'
		if (spans[i].innerHTML === 'Promoted') {
			// Get the div that wraps around the entire ad
			let card = spans[i].closest('.feed-shared-update-v2');

			// If the class changed and we can't find it with closest(), get the 6th parent
			if (card === null) {
				// Could also be card.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode :D
				let j = 0;
				card = spans[i];
				while (j < 6) {
					card = card.parentNode;
					++j;
				}
			}

			// Make the ad disappear!
			card.setAttribute('style', 'display: none !important;');
		}
	}
}
