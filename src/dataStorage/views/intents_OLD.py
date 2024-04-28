mappings = {
    
  "register": {
    "title": [
      "Provide your Name.",
    ],
    "options": {},
    "next_action": "register_dob",
  },

  "register_dob": {
    "title": [
      "Provide your Date of Birth in DD-MM-YYYY format.",
    ],
    "options": {},
    "next_action": "register_phone",
  },

  "register_phone": {
    "title": [
      "Provide your Phone Number.",
    ],
    "options": {},
    "next_action": "register_check",
  },

  "register_success": {
    "title": [
      "Patient Registered.",
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
      "Patient Registertion Failed.",
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
      "Provide your Name or ID.",
    ],
    "options": {},
    "next_action": "home",
  },

  "login_falied": {
    "title": [
      "Provided Name or ID is not a Patient.",
      "Provide your Name or ID.",
    ],
    "options": {},
    "next_action": "home",
  },

  "home": {
    "title": [
      "Hello {patient_name},",
      "How can I help you?",
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
      "reschedule_appointment": {
        "text": "Reschedule Appointment",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
        "option_id": "reschedule_appointment",
      },
      "cancel_appointment": {
        "text": "Cancel Appointment",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2",
        "option_id": "cancel_appointment",
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
      "Provide Appointment Date in DD-MM-YYYY format.",
    ],
    "options": {},
    "next_action": "book_appointment_slots",
  },

  "book_appointment_slots": {
    "title": [
      "Select one from Avaliable slot(s).",
    ],
    "options": {},
    "next_action": "book_appointment_with_slot",
  },

  "book_appointment_slot_error": {
    "title": [
      "Oops..!, Failed Book Appointment.",
      "Select one from Avaliable slot(s).",
    ],
    "options": {},
    "next_action": "book_appointment_with_slot",
  },

  "book_appointment_unaviable": {
    "title": [
      "Oops..!, Failed Book Appointment.",
    ],
    "options": {},
    "next_action": "book_appointment",
  },

  "book_appointment_complete": {
    "title": [
      "Appointment Booked.",
    ],
    "options": {
      "home": "Go to Home.",
    },
  },

  "logout": {
    "title": [
      "Successfully Logout out.",
    ],
    "options": {
      "logout": {
        "text": "Login",
        "class_list": "chat_option btn btn-sm btn-outline-info m-2 float-end",
        "option_id": "login",
      },
    },
    "next_action": "home",
  },
}