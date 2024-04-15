import os
from dotenv import load_dotenv

load_dotenv()

credentials = {
    "secret_key": "?fm~]V-xFOy$L;7T>06j&:r_UZluCA${?DVZ^d318}S6_i4hSM.yM-Op:xf?bf;]fCFPhy}h]iP++{!K!,oh66Lk?ELu?#?RZKv+",
    # "useSqlLite" : True,
    "useSqlLite": bool(int(os.getenv("useSqlLite", 0))),
}
