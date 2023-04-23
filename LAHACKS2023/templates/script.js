
function checkForm() {
  const elements = document.querySelectorAll('.req');

  for (let i = 0; i < elements.length; i++) {
    if (elements[i].value === "") {
      alert("Enter a value into every field!");
      return false;
    }
  }

  return checkQuarters();
}

function checkQuarters() {
  var num = document.getElementById("quarter-select").value;
    if (isNaN(num) || num < 9 || num > 15) {
      alert("Enter a number of quarters!");
      return false;
    }
  return true;
}