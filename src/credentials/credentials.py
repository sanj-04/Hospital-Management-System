import os
from dotenv import load_dotenv

load_dotenv()

credentials = {
    "secret_key": "?fm~]V-xFOy$L;7T>06j&:r_UZluCA${?DVZ^d318}S6_i4hSM.yM-Op:xf?bf;]fCFPhy}h]iP++{!K!,oh66Lk?ELu?#?RZKv+",
    # "useSqlLite" : True,
    "useSqlLite": bool(int(os.getenv("useSqlLite", 0))),
    "default_setting_json" : {
        "available_days": {
            "Monday" : 1,
            "Tuesday" : 2,
            "Wednesday" : 3,
            "Thursday" : 4,
            "Friday" : 5,
            "Saturday" : 6,
        },
        "unavailable_days" : {
            "Sunday" : 0,
        },
        "available" : {
            "Monday" : {
                "from": "04:30 PM",
                "to": "07:15 PM",
                "duration": 15,
                "slot_count": 11,
            },
            "Tuesday" : {
                "from": "04:30 PM",
                "to": "07:15 PM",
                "duration": 15,
                "slot_count": 11,
            },
            "Wednesday" : {
                "from": "04:30 PM",
                "to": "07:15 PM",
                "duration": 15,
                "slot_count": 11,
            },
            "Thursday" : {
                "from": "04:30 PM",
                "to": "07:15 PM",
                "duration": 15,
                "slot_count": 11,
            },
            "Friday" : {
                "from": "04:30 PM",
                "to": "07:15 PM",
                "duration": 15,
                "slot_count": 11,
            },
            "Saturday" : {
                "from": "12:00 PM",
                "to": "01:15 PM",
                "duration": 15,
                "slot_count": 5,
            },
        },
    }
}
