import os

from flask import Flask

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "facebook_insights.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import views
from . import filters
from . import login

import signal
import traceback
def where_are_we(sig, frm):
        print("Signal %s received!" % sig)
        traceback.print_stack(frm)
        print("---> We are here <---")
signal.signal(signal.SIGUSR1, where_are_we)
import os
print("I am process", os.getpid())