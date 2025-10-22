import pandas as pd
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from time import sleep
from datetime import datetime
import re
import os
from tkinter import Tk, filedialog