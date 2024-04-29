mappings = {
    
  "register": {
    "title": [
      {
        "text": "Provide your Name.",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "register_dob",
  },

  "register_dob": {
    "title": [
      {
        "text": "Provide your Date of Birth in DD-MM-YYYY format.",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "register_phone",
  },

  "register_phone": {
    "title": [
      {
        "text": "Provide your Phone Number.",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "register_check",
  },

  "register_success": {
    "title": [
      {
        "text": "Patient Registered.",
        "class_list": "",
      },
    ],
    "options": {
      "login": {
        "text": "Login",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2 float-end",
        "option_id": "login",
      },
    },
    "next_action": "login",
  },

  "register_failed": {
    "title": [
      {
        "text": "Patient Registertion Failed.",
        "class_list": "error",
      },
    ],
    "options": {
      "register": {
        "text": "Register",
        "class_list": "chat_option btn btn-sm btn-outline-success m-2 float-end",
        "option_id": "register",
      },
    },
    "next_action": "register",
  },

  "login": {
    "title": [
      {
        "text": "Provide your Name or ID.",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "check_otp",
  },

  "check_otp": {
    "title": [
      {
        "text": "OTP sent to {phone_number}.",
        "class_list": "",
      },
      {
        "text": "Enter the OTP to login.",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "otp_verify",
  },

  "login_falied": {
    "title": [
      {
        "text": "Provided Name or ID is not a Patient.",
        "class_list": "error",
      },
      {
        "text": "Provide your Name or ID.",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "check_otp",
  },

  "home": {
    "title": [
      {
        "text": "Hello {patient_name},",
        "class_list": "",
      },
      {
        "text": "How can I help you?",
        "class_list": "",
      },
    ],
    "options": {
      "book_appointment": {
        "text": "Book Appointment",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
        "option_id": "book_appointment",
      },
      "view_appointment": {
        "text": "View Appointment",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
        "option_id": "view_appointment",
      },
      "cancel_appointment": {
        "text": "Cancel Appointment",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
        "option_id": "cancel_appointment",
      },
      "reschedule_appointment": {
        "text": "Reschedule Appointment",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
        "option_id": "reschedule_appointment",
      },
      "logout": {
        "text": "Logout",
        "class_list": "chat_option btn btn-sm btn-outline-danger m-2",
        "option_id": "logout",
      },
    },
  },

  "book_appointment": {
    "title": [
      {
        "text": "Provide Appointment Date in DD-MM-YYYY format.",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "book_appointment_slots",
  },

  "book_appointment_slots": {
    "title": [
      {
        "text": "Select one from Avaliable slot(s).",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "book_appointment_with_slot",
  },

  "book_appointment_slot_error": {
    "title": [
      {
        "text": "Oops..!, Failed Book Appointment.",
        "class_list": "error",
      },
      {
        "text": "Select one from Avaliable slot(s).",
        "class_list": "",
      },
    ],
    "options": {},
    "next_action": "book_appointment_with_slot",
  },

  "book_appointment_unaviable": {
    "title": [
      {
        "text": "Oops..!, Failed Book Appointment.",
        "class_list": "error",
      },
    ],
    "options": {},
    "next_action": "book_appointment",
  },

  "book_appointment_complete": {
    "title": [
      {
        "text": "Appointment Booked.",
        "class_list": "",
      },
    ],
    "options": {
      "home": "Go to Home.",
    },
  },

  "logout": {
    "title": [
      {
        "text": "Successfully Logged Out.",
        "class_list": "",
      },
    ],
    "options": {
      "login": {
        "text": "Login",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2 float-end",
        "option_id": "login",
      },
    },
    "next_action": "login",
  },
}