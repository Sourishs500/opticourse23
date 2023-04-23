
function deptDropdown() {

  var schoolDropdown = document.getElementById("school-select");
  var selected = schoolDropdown.options[schoolDropdown.selectedIndex].value;
  var newDropdown = document.getElementById("dept-dropdown");

  if (selected === "") {
    newDropdown.innerHTML = "";
  } else if (selected === "Engineering") {
    newDropdown.innerHTML = `
      <label for="dept-select">Department:</label>
      <select id="dept-select" onchange="majorDropdown()">
        <option value="">Select an option</option>
        <option value="Chem/Bio">Department of Chemical/Biomolecular Engineering</option>
        <option value="Civil/Envr">Department of Civil/Environmental Engineering</option>
        <option value="Mech/Aero">Department of Mechanical/Aerospace Engineering</option>
        <option value="ECE">Department of Electrical/Computer Engineering</option>
      </select>
    `;
  }
}

function majorDropdown() {

  var deptDropdown = document.getElementById("dept-select");
  var selected = deptDropdown.options[deptDropdown.selectedIndex].value;
  var newDropdown = document.getElementById("major-dropdown");

  if (selected === "") {
    newDropdown.innerHTML = "";
  } else if (selected === "Chem/Bio") {
    newDropdown.innerHTML = `
      <label for="major-select">Choose a major from the Chem/Bio Engr Dept:</label>
      <select id="major-select" onchange="minorDropdown()">
        <option value="">Select an option</option>
        <option value="Chem">Chemistry</option>
        <option value="Gen chem">General Chemistry</option>
        <option value="Biochem">Biochemistry</option>
        <option value="Materials">Materials</option>
      </select>
    `;
  } else if (selected === "Civil/Envr") {
    newDropdown.innerHTML = `
      <label for="major-select">Choose a major from the Civil/Environmental Engr Dept:</label>
      <select id="major-select" onchange="minorDropdown()">
        <option value="">Select an option</option>
        <option value="Civil">Civil Engineering</option>
        <option value="Enviro">Environmental Engineering</option>
      </select>
    `;
  } else if (selected === "ECE") {
    newDropdown.innerHTML = `
      <label for="major-select">Choose a major from the Electrical/Comp Engr Dept:</label>
      <select id="major-select" onchange="minorDropdown()">
        <option value="">Select an option</option>
        <option value="EE">Electrical Engineering</option>
        <option value="CE">Computer Engineering</option>
      </select>
    `;
  } else if (selected === "Mech/Aero") {
    newDropdown.innerHTML = `
      <label for="major-select">Choose a major from the Mech/Aerospace Engr Dept:</label>
      <select id="major-select" onchange="minorDropdown()">
        <option value="">Select an option</option>
        <option value="MechE">Mechanical Engineering</option>
        <option value="AeroE">Aerospace Engineering</option>
      </select>
    `;
  }
}

function minorDropdown() {

  var newDropdown = document.getElementById("minor-dropdown");

  newDropdown.innerHTML = `
  <label for="minor-select">Choose a minor:</label>
  <select id="minor-select" onchange="techBreadthDropdown()">
    <option value="">Select a minor</option>
    <option value="None">No minor</option>
    <option value="Chem">Bioinformatics</option>
    <option value="Gen chem">Data Science</option>
    <option value="Biochem">Environmental Engineering</option>
  </select>
  `;
}

function techBreadthDropdown() {
  
  var newDropdown = document.getElementById("techBreadth-dropdown");

  newDropdown.innerHTML = `
  <label for="techBreadth-select">Choose a technical breadth area:</label>
  <select id="techBreadth-select" onchange="quarters()">
    <option value="">Select a tech breadth</option>
    <option value="CS">Computer Science</option>
    <option value="EE">Electrical Engineering</option>
    <option value="MechE">Mechanical Engineering</option>
    <option value="Materials">Materials Science/Engineering</option>
    <option value="Biomed">Biomedical Engineering/Engineering</option>
    <option value="Civil/Enviro">Civil/Environmental Engineering</option>
  </select>
  `;
}

function quarters() {

  var newField = document.getElementById("quarters-amount");

  newField.innerHTML = `
    <label for="quantity">Quarters:</label>
    <input type="number" id="quarter-select" min="9" max="15" required>
  `;

}

function sendToFlask() {
  var num = document.getElementById("quarter-select").value;
    if (isNaN(num) || num < 9 || num > 15) {
      alert("The number is " + num);
      alert("Enter a number of quarters!");
      return;
    }
  alert("Success x2!");

  //  fetch API call

}