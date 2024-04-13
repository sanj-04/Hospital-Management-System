function showPatientDetails(name, age) {
    let patientDetails = document.getElementById('patientDetails');
    let cardElement = document.getElementById('cd');
    patientDetails.innerHTML = `
        <center>
            <p>Name: ${name}</p>
            <p>Age: ${age}</p>
        </center>
    `;
    cardElement.style.display = '';
}
function toggleOptions() {
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.style.display = optionsContainer.style.display === 'block' ? 'none' : 'block';
}

function openAppointments() {
    // Add functionality to open appointments page
   // alert('Opening Appointments...');
}

function logout() {
    // Add functionality to logout
   // alert('Logging out...');
}


 function filterNames() {
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const patientList = document.getElementById('patientList');
            const patientButtons = patientList.getElementsByTagName('li');

            for (let i = 0; i < patientButtons.length; i++) {
                const patientName = patientButtons[i].textContent.toLowerCase();
                if (patientName.includes(searchInput)) {
                    patientButtons[i].style.display = '';
                } else {
                    patientButtons[i].style.display = 'none';
                }
    }
}

function display(){
  const searchInput = document.getElementById('searchInput').value.trim();
  const card = document.getElementById('cd');
//   const cds = document.getElementById('cds');

  if (searchInput == '') {
    card.style.display = 'none';
  }
//   else{
//     card.style.display = 'flex';
//   }
}