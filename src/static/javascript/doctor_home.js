function filter_patient() {
  var filter, i;
  filter = document.getElementById("id_filter_patient").value.toUpperCase();
  let cells = document.querySelectorAll('.patient');
  for (i = 0; i < cells.length; i++) {
    let patient_name = cells[i].getAttribute('data-patient_name');
    let patient_id = cells[i].getAttribute('data-patient_id');
    if ((patient_name.toUpperCase().indexOf(filter) > -1) || (patient_id.toUpperCase().indexOf(filter) > -1)) {
      cells[i].style.display = "";
    } else {
      cells[i].style.display = "none";
    }
  }
}

function showPatientDetails(ele) {
  let patient_name = ele.getAttribute('data-patient_name');
  let patient_id = ele.getAttribute('data-patient_id');
  let patient_age = ele.getAttribute('data-patient_age');
  document.getElementById('patient_info').removeAttribute('hidden');
  document.getElementById('patient_prescription').removeAttribute('hidden');
  document.getElementById('patient_info_name').innerText = patient_name;
  document.getElementById('prescriptionPatientName').innerText = patient_name;
  document.getElementById('patient_info_id').innerText = patient_id;
  document.getElementById('patient_info_age').innerText = patient_age;
  document.querySelectorAll('.patient').forEach(x => {
    x.classList.remove("active");
  });
  ele.classList.add("active");
  fetchPatientDetails(patient_id);
}

function populatePrescriptions(prescriptions) {
  let prescription_cardsEle = document.getElementById('prescription_cards');
  let row = '';
  prescription_cardsEle.innerHTML = row;
  prescriptions.forEach(prescription => {
    row = row + `<div class="col-sm-4 mb-3 mb-sm-0">
      <div class="card text-bg-primary mb-3" style="max-width: 18rem;">
        <div class="card-header">`+prescription.name+`</div>
        <div class="card-body text-center">
          <button class="btn btn-sm btn-success float-center" id="prescription_`+prescription.id+`">View</button>
          <h5 class="card-title" hidden>Primary card title</h5>
          <p class="card-text" hidden>Some quick example text to build on the card title and make up the bulk of the card's content.</p>
        </div>
      </div>
    </div>`;
  });
  prescription_cardsEle.innerHTML = row;
}

function createPrescription() {
  let medicine_name = document.querySelectorAll('[name="medicine_name"]');
  let before_breakfast = document.querySelectorAll('[name="before_breakfast"]');
  let after_breakfast = document.querySelectorAll('[name="after_breakfast"]');
  let before_lunch = document.querySelectorAll('[name="before_lunch"]');
  let after_lunch = document.querySelectorAll('[name="after_lunch"]');
  let before_dinner = document.querySelectorAll('[name="before_dinner"]');
  let after_dinner = document.querySelectorAll('[name="after_dinner"]');

  let prescription_list = [];
  for (let index = 0; index < medicine_name.length; index++) {
    if (medicine_name[index].value != '') {
      var obj = new Object();
      obj.medicine_name = medicine_name[index].value;
      obj.before_breakfast = Number(before_breakfast[index].value);
      obj.after_breakfast = Number(after_breakfast[index].value);
      obj.before_lunch = Number(before_lunch[index].value);
      obj.after_lunch = Number(after_lunch[index].value);
      obj.before_dinner = Number(before_dinner[index].value);
      obj.after_dinner = Number(after_dinner[index].value);
      prescription_list.push(obj);
    }
  }
  if (prescription_list != []) {
    return JSON.stringify(prescription_list);
  } else {
    alert('Please fill in all fields.');
  }
}

function showAppointmentUpdateForm(button) {
    let tableRow = button.parentNode.parentNode;
    tableRow.querySelector('[name="span_appointment_date_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="span_appointment_from_time_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="span_appointment_to_time_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="span_appointment_status_update"]').setAttribute('hidden', '');
    tableRow.querySelector('.btn-danger').setAttribute('hidden', '');
    button.setAttribute('hidden', '');

    tableRow.querySelector('[name="id_appointment_date_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="id_appointment_from_time_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="id_appointment_to_time_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="id_appointment_status_update"]').removeAttribute('hidden');

    tableRow.querySelector('.btn-success').removeAttribute('hidden');
    tableRow.querySelector('.btn-secondary').removeAttribute('hidden');
}

function showScheduleUpdateForm(button) {
    let tableRow = button.parentNode.parentNode;
    tableRow.querySelector('[name="span_unavailable_count_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="span_schedule_status_update"]').setAttribute('hidden', '');
    tableRow.querySelector('.btn-danger').setAttribute('hidden', '');
    button.setAttribute('hidden', '');

    tableRow.querySelector('[name="id_unavailable_count_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="id_schedule_status_update"]').removeAttribute('hidden');

    tableRow.querySelector('.btn-success').removeAttribute('hidden');
    tableRow.querySelector('.btn-secondary').removeAttribute('hidden');
}

function cancelAppointmentUpdate(button) {
    let tableRow = button.parentNode.parentNode;
    tableRow.querySelector('[name="span_appointment_date_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="span_appointment_from_time_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="span_appointment_to_time_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="span_appointment_status_update"]').removeAttribute('hidden');
    tableRow.querySelector('.btn-danger').removeAttribute('hidden');
    tableRow.querySelector('.btn-primary').removeAttribute('hidden');
    button.setAttribute('hidden', '');

    tableRow.querySelector('[name="id_appointment_date_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="id_appointment_from_time_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="id_appointment_to_time_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="id_appointment_status_update"]').setAttribute('hidden', '');

    tableRow.querySelector('.btn-success').setAttribute('hidden', '');
    tableRow.querySelector('.btn-secondary').setAttribute('hidden', '');
}

function scheduleCancelUpdate(button) {
    let tableRow = button.parentNode.parentNode;
    tableRow.querySelector('[name="span_unavailable_count_update"]').removeAttribute('hidden');
    tableRow.querySelector('[name="span_schedule_status_update"]').removeAttribute('hidden');
    tableRow.querySelector('.btn-danger').removeAttribute('hidden');
    tableRow.querySelector('.btn-primary').removeAttribute('hidden');
    button.setAttribute('hidden', '');

    tableRow.querySelector('[name="id_unavailable_count_update"]').setAttribute('hidden', '');
    tableRow.querySelector('[name="id_schedule_status_update"]').setAttribute('hidden', '');

    tableRow.querySelector('.btn-success').setAttribute('hidden', '');
    tableRow.querySelector('.btn-secondary').setAttribute('hidden', '');
}

function showAlert(message, buttonElement, type) {
    $('#alertModal').modal('show');
    let alertMessage = document.getElementById("alertMessage");
    let confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

    alertMessage.textContent = message;
    confirmDeleteBtn.addEventListener('click', event => {
        if (type == "appointment") {
            deleteAppointmentRow(buttonElement);
        } else if (type == "schedule") {
            scheduleDeleteRow(buttonElement);
        }
    });
}

function confirmAppointmentDelete(button) {
    showAlert("Are you sure you want to delete this patient's Appointment?", button, "appointment");
}

function scheduleConfirmDelete(button) {
    showAlert("Are you sure you want to delete this Schedule?", button, "schedule");
}