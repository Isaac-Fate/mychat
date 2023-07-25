import sys
sys.path.append("../")

from dotenv import load_dotenv
load_dotenv("../.env", override=True)

import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
