function showAppointmentUpdateForm(button) {
  let tableRow = button.parentNode.parentNode;
  tableRow.querySelector('[name="span_appointment_date_update"]').setAttribute('hidden', '');
  tableRow.querySelector('[name="span_appointment_from_time_update"]').setAttribute('hidden', '');
  tableRow.querySelector('[name="span_appointment_to_time_update"]').setAttribute('hidden', '');
  // tableRow.querySelector('[name="span_appointment_status_update"]').setAttribute('hidden', '');
  tableRow.querySelector('.btn-danger').setAttribute('hidden', '');
  button.setAttribute('hidden', '');

  tableRow.querySelector('[name="id_appointment_date_update"]').removeAttribute('hidden');
  tableRow.querySelector('[name="id_appointment_from_time_update"]').removeAttribute('hidden');
  tableRow.querySelector('[name="id_appointment_to_time_update"]').removeAttribute('hidden');

  tableRow.querySelector('.btn-success').removeAttribute('hidden');
  tableRow.querySelector('.btn-secondary').removeAttribute('hidden');
}

function cancelAppointmentUpdate(button) {
  let tableRow = button.parentNode.parentNode;
  tableRow.querySelector('[name="span_appointment_date_update"]').removeAttribute('hidden');
  tableRow.querySelector('[name="span_appointment_from_time_update"]').removeAttribute('hidden');
  tableRow.querySelector('[name="span_appointment_to_time_update"]').removeAttribute('hidden');
  // tableRow.querySelector('[name="span_appointment_status_update"]').removeAttribute('hidden');
  tableRow.querySelector('.btn-danger').removeAttribute('hidden');
  tableRow.querySelector('.btn-primary').removeAttribute('hidden');
  button.setAttribute('hidden', '');

  tableRow.querySelector('[name="id_appointment_date_update"]').setAttribute('hidden', '');
  tableRow.querySelector('[name="id_appointment_from_time_update"]').setAttribute('hidden', '');
  tableRow.querySelector('[name="id_appointment_to_time_update"]').setAttribute('hidden', '');

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
      }
    });
}

function confirmAppointmentDelete(button) {
  showAlert("Are you sure you want to delete this patient's Appointment?", button, "appointment");
}


function addRow(table_id) {
  let tableEle = document.getElementById(table_id);
  let rowCount = tableEle.rows.length;
  if (rowCount > 0) {
    return tableEle.insertRow(rowCount - 1);
  }
  return tableEle.insertRow(0);
}

function datepicker_operation(datepicker_operation) {
  $('.datepicker_dob').datepicker({
    format: 'dd-M-yyyy',
    autoclose: true,
    monthNames: ['January','February','March','April','May','June','July','August','September','October','November','December'],
    monthNamesShort: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    weekStart: 0,
    calendarWeeks: true,
  });

  $('.datepicker_single').datepicker({
    // startDate: '{{start_date}}',
    // endDate: '{{last_date}}',
    format: 'dd-M-yyyy',
    autoclose: true,
    monthNames: ['January','February','March','April','May','June','July','August','September','October','November','December'],
    monthNamesShort: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    daysOfWeekDisabled: datepicker_operation,// [0,6],
    weekStart: 0,
    calendarWeeks: true,
  });

  // $('.datepicker_single').on('show', function(e) {
  //   // $(this).find('.input-group-addon .count').text(' ' + e.dates.length);
  //   console.log('Calendar showing.', e);
  // });
}

function reloadElements(data) {
  document.querySelectorAll('.appointment').forEach(x => {x.remove();});
  document.getElementById('prescription_cards').innerHTML = "";
  populatePrescriptions(data.prescriptions);

  document.getElementById('id_patient').value = data.patient.name;
  document.getElementById('id_date_of_birth').value = data.patient.date_of_birth;
  document.getElementById('id_phone_number').value = data.patient.phone_number;
  document.getElementById('patient_info_name').innerText = data.patient.name;
  document.getElementById('patient_info_age').innerText = data.patient.age;
  document.getElementById('patient_info_id').innerText = data.patient.id;

  data.appointments.forEach(appointment => {
    let newRowEle = addRow('appointment_table');
    newRowEle.classList.add('appointment');

    let newCellEle1 = newRowEle.insertCell();
    newCellEle1.innerText = appointment.patient_id;

    let newCellEle2 = newRowEle.insertCell();
    newCellEle2.innerText = appointment.patient_name;

    let newCellEle3 = newRowEle.insertCell();
    newCellEle3.innerHTML = `<span name="span_appointment_date_update">`+appointment.appointment_date+`</span>
    <input type="text" name="id_appointment_date_update" class="datepicker_single form-control"
    hidden value="`+appointment.appointment_date+`" autocomplete="off"></input>`;

    let newCellEle4 = newRowEle.insertCell();
    newCellEle4.innerHTML = `<span name="span_appointment_from_time_update">`+appointment.appointment_from_time_str+`</span>
    <input type="time" name="id_appointment_from_time_update" class="form-control"
    hidden value="`+appointment.appointment_from_time+`"></input>`;

    let newCellEle5 = newRowEle.insertCell();
    newCellEle5.innerHTML = `<span name="span_appointment_to_time_update">`+appointment.appointment_to_time_str+`</span>
    <input type="time" name="id_appointment_to_time_update" class="form-control"
    hidden value="`+appointment.appointment_to_time+`"></input>`;

    let newCellEle6 = newRowEle.insertCell();
    newCellEle6.innerHTML = `<span name="span_appointment_status_update">`+appointment.appointment_status+`</span>`;

    let newCellEle7 = newRowEle.insertCell();
    newCellEle7.setAttribute('hidden', '');
    newCellEle7.setAttribute('name', 'id_appointment_id_update');
    newCellEle7.innerText = appointment.appointment_id;  

    let newCellEle8 = newRowEle.insertCell();
    newCellEle8.innerHTML = `<button onclick="showAppointmentUpdateForm(this);" class="btn btn-sm btn-primary"
    data-from_date_time="`+appointment.appointment_from_date_time+`"
    data-to_date_time="`+appointment.appointment_to_date_time+`"
    data-patient_id="`+appointment.patient_id+`"
    data-appointment_id="`+appointment.appointment_id+`">Update</button>
    <button onclick="confirmAppointmentDelete(this);" data-appointment_id="`+appointment.appointment_id+`" class="btn btn-sm btn-danger">Delete</button>
    <button onclick="updateAppointmentRow(this);" class="btn btn-sm btn-success" hidden>Done</button>
    <button onclick="cancelAppointmentUpdate(this);" class="btn btn-sm btn-secondary" hidden>Cancel</button>`;
  });
  
  datepicker_operation(data.unavailable);
}