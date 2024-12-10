// delete everything else except the target element
function stripPage(element) {
  document.body.innerHTML = "";
  document.body.appendChild(element);
}
