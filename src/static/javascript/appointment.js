function loadData() {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    const patientData = JSON.parse(localStorage.getItem('patientData')) || [];

    patientData.forEach((patient) => {
        const newRow = tableBody.insertRow();

        const idCell = newRow.insertCell(0);
        const nameCell = newRow.insertCell(1);
        const dateCell = newRow.insertCell(2);
        const timeCell = newRow.insertCell(3);
        const actionsCell = newRow.insertCell(4);

        idCell.textContent = patient.patientID;
        nameCell.textContent = patient.patientName;
        dateCell.textContent = patient.date;
        timeCell.textContent = patient.time;

        const updateButton = document.createElement('button');
        updateButton.textContent = 'Update';
        updateButton.onclick = function() {
            showUpdateForm(updateButton);
        };

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = function() {
            confirmDelete(deleteButton);
        };

        actionsCell.appendChild(updateButton);
        actionsCell.appendChild(deleteButton);
    });
}

function saveData(patientData) {
    localStorage.setItem('patientData', JSON.stringify(patientData));
}

let insertBtn = document.getElementById('insertBtn');
insertBtn.addEventListener('click', showInsertForm);
let confirmDeleteButton;

function showUpdateForm(button) {
    let from_date_time = button.getAttribute('data-from_date_time');
    let to_date_time = button.getAttribute('data-to_date_time');
    let patient_id = button.getAttribute('data-patient_id');
    let appointment_id = button.getAttribute('data-appointment_id');
    let row = button.parentNode.parentNode;
    let patient_name = row.cells[1].textContent;

    document.getElementById('id_patient_update').value = patient_name;
    document.getElementById('id_from_date_time_update').value = from_date_time;
    document.getElementById('id_to_date_time_update').value = to_date_time;
    document.getElementById('id_appointment_id_update').value = appointment_id;
    document.getElementById('id_patient_id_update').value = patient_id;
    updateForm.style.display = 'block';
}

function confirmDelete(button) {
    showAlert("Are you sure you want to delete this patient?", button);
}

function showInsertForm() {
    let insertForm = document.getElementById('insertForm');
    insertForm.reset();
    insertForm.style.display = 'block';
}

function hideInsertForm() {
    let insertForm = document.getElementById('insertForm');
    insertForm.style.display = 'none';
}

function hideUpdateForm() {
    let updateForm = document.getElementById('updateForm');
    updateForm.style.display = 'none';
}

function showAlert(message, buttonElement) {
    let modal = document.getElementById("alertModal");
    let alertMessage = document.getElementById("alertMessage");
    let confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

    alertMessage.textContent = message;
    modal.style.display = "block";
    confirmDeleteButton = buttonElement;

    confirmDeleteBtn.onclick = function() {
        deleteRow(confirmDeleteButton);
    }
}

function closeModal() {
    let modal = document.getElementById("alertModal");
    modal.style.display = "none";
}