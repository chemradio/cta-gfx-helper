// find the first class
let firstClass = document.querySelectorAll(".xvbhtw8");

// find the second class within the first class
let target;

for (const el of firstClass) {
  let secondClass = el.querySelector(".x1qughib");
  if (secondClass) {
    sidePanel = secondClass;
    break;
  }
}
sidePanel.remove();
return target;
