function getElementByXpath(path) {
	return document.evaluate(
		path,
		document,
		null,
		XPathResult.FIRST_ORDERED_NODE_TYPE,
		null
	).singleNodeValue;
}

function cleanupTwitterPost() {
	function getElementByXpath(path) {
		return document.evaluate(
			path,
			document,
			null,
			XPathResult.FIRST_ORDERED_NODE_TYPE,
			null
		).singleNodeValue;
	}
	let badPost = getElementByXpath("//article[@tabindex='0']");
	badPost.parentElement.removeChild(badPost);
}
