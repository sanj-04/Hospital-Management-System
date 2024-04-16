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

function addRow(table_id) {
  let tableEle = document.getElementById(table_id);
  let rowCount = tableEle.rows.length;
  if (rowCount > 0) {
    return tableEle.insertRow(rowCount - 1);
  }
  return tableEle.insertRow(0);
}

function datepicker_operation(datepicker_operation) {
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

  $('.datepicker_single').on('show', function(e) {
    // $(this).find('.input-group-addon .count').text(' ' + e.dates.length);
    console.log('Calendar showing.', e);
  });

  $('.datepicker_multiple').datepicker({
    // startDate: new Date(),
    // endDate: '{{last_date}}',
    multidate: true,
    // autoclose: true,
    calendarWeeks: true,
    format: "dd-M-yyyy",
    daysOfWeekHighlighted: "0",
    daysOfWeekDisabled: datepicker_operation,
    // datesDisabled: ['16-04-2024'],
    language: 'en',
    weekStart: 0,
  });

  $('.datepicker_multiple').on('changeDate', function(e) {
    $(this).find('.input-group-addon .count').text(' ' + e.dates.length);
    console.log(e.dates.length);
  });
}

function reloadElements(data) {
  document.querySelectorAll('.patient').forEach(x => {x.remove();});
  document.querySelectorAll('.appointment').forEach(x => {x.remove();});
  document.querySelectorAll('.schedule').forEach(x => {x.remove();});
  document.getElementById('patient_info').setAttribute('hidden', '');
  document.getElementById('patient_prescription').setAttribute('hidden', '');
  document.getElementById('prescription_cards').innerHTML = "";
  let medicine_listEle = document.getElementById('id_medicine_list');
  let patients_listEle = document.getElementById('id_patients_list');
  medicine_listEle.innerHTML = "";
  patients_listEle.innerHTML = "";

  let patients_ulEle = document.querySelector('#patients ul');
  data.patients.forEach(patient => {
    let liEle = document.createElement('li');
    liEle.setAttribute('style', 'cursor: pointer;');
    liEle.classList.add('card-body', 'list-group-item', 'list-group-item-action', 'border', 'border-dark', 'patient', 'text-left');
    liEle.setAttribute('id', 'patient_'+patient.id);
    liEle.setAttribute('data-patient_id', patient.id);
    liEle.setAttribute('data-patient_name', patient.name);
    liEle.setAttribute('data-patient_age', patient.age);
    liEle.setAttribute('onclick', 'showPatientDetails(this);');
    liEle.innerText = patient.name;
    patients_ulEle.appendChild(liEle);
  });

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
    hidden value="`+appointment.appointment_date+`"></input>`;

    let newCellEle4 = newRowEle.insertCell();
    newCellEle4.innerHTML = `<span name="span_appointment_from_time_update">`+appointment.appointment_from_time_str+`</span>
    <input type="time" name="id_appointment_from_time_update" class="form-control"
    hidden value="`+appointment.appointment_from_time+`"></input>`;

    let newCellEle5 = newRowEle.insertCell();
    newCellEle5.innerHTML = `<span name="span_appointment_to_time_update">`+appointment.appointment_to_time_str+`</span>
    <input type="time" name="id_appointment_to_time_update" class="form-control"
    hidden value="`+appointment.appointment_to_time+`"></input>`;

    let options = '';
    data.status_choices.forEach(status_choice => {
      if (status_choice[0] == appointment.appointment_status) {
        options+=`<option value="`+status_choice[0]+`" selected="selected">`+status_choice[1]+`</option>`;
      } else {
        options+=`<option value="`+status_choice[0]+`">`+status_choice[1]+`</option>`; 
      }
    });
    let newCellEle6 = newRowEle.insertCell();
    newCellEle6.innerHTML = `<span name="span_appointment_status_update">`+appointment.appointment_status+`</span>
    <select name="id_appointment_status_update" class="form-select" hidden>`+options+`</select>`;

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

  data.schedules.forEach(schedule => {
    let newRowEle = addRow('schedule_table');
    newRowEle.classList.add('schedule');
    let newCellEle1 = newRowEle.insertCell();
    newCellEle1.innerText = schedule.schedule_month_year;

    let newCellEle2 = newRowEle.insertCell();
    newCellEle2.innerHTML = `<span name="span_unavailable_count_update">`+schedule.rejected_days_count+`</span>
    <input type="text" name="id_unavailable_count_update" autocomplete="off"
    class="datepicker_multiple form-control" hidden value="`+schedule.rejected_days+`"></input>`;

    let options = '';
    data.schedule_status_choices.forEach(status_choice => {
      if (status_choice[0] == schedule.status) {
        options+=`<option value="`+status_choice[0]+`" selected="selected">`+status_choice[1]+`</option>`;
      } else {
        options+=`<option value="`+status_choice[0]+`">`+status_choice[1]+`</option>`; 
      }
    });
    let newCellEle3 = newRowEle.insertCell();
    newCellEle3.innerHTML = `<span name="span_schedule_status_update">`+schedule.status+`</span>
    <select name="id_schedule_status_update" class="form-select" hidden>`+options+`</select>`;   

    let newCellEle4 = newRowEle.insertCell();
    newCellEle4.innerHTML = `<button onclick="showScheduleUpdateForm(this);" class="btn btn-sm btn-primary">Update</button>
    <button onclick="scheduleConfirmDelete(this);" data-schedule_id="`+schedule.schedule_id+`" class="btn btn-sm btn-danger">Delete</button>
    <button onclick="scheduleUpdateRow(this);" data-schedule_id="`+schedule.schedule_id+`" class="btn btn-sm btn-success" hidden>Done</button>
    <button onclick="scheduleCancelUpdate(this);" class="btn btn-sm btn-secondary" hidden>Cancel</button>`;
  });

  let medicine_options = '';
  let patients_options = '';
  data.medicines.forEach(medicine => {
    medicine_options+=`<option value="`+medicine.name+`">`+medicine.name+`</option>`; 
  });

  data.patients.forEach(patient => {
    patients_options+=`<option value="`+patient.id+`">`+patient.name+`</option>`; 
  });
  medicine_listEle.innerHTML = medicine_options;
  patients_listEle.innerHTML = patients_options;

  datepicker_operation(data.unavailable);
}