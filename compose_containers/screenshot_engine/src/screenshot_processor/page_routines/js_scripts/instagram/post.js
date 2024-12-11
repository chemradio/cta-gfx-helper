// find a div that contain these classes - .xkrivgy and .x1gryazu. it may contain other classes as well

// find the first class
let firstClass = document.querySelectorAll(".xkrivgy");

// find the second class within the first class
let target;

for (const el of firstClass) {
  let secondClass = el.querySelector(".x1gryazu");
  if (secondClass) {
    target = secondClass;
    break;
  }
}

return target;
