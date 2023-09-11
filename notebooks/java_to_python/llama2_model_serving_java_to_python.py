# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Download Data
# MAGIC ### AVATAR: Java-Python Program Translation Dataset

# COMMAND ----------

USER = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
SCRIPT_PATH = f"/Workspace/Repos/{USER}/db-ancient-code-translation/notebooks/java_to_python/utils/download.sh"
DOWNLOAD_PATH = "/tmp"
FULL_PATH = f"{DOWNLOAD_PATH}/transcoder_evaluation_gfg/java"

!cd {DOWNLOAD_PATH} && bash {SCRIPT_PATH}

# COMMAND ----------

databricks_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
url = databricks_url + "/serving-endpoints/llama2/invocations"

# COMMAND ----------

import requests
import json
import re

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

PROMPT_TEMPLATE = """
  Assume you are an expert both in {input_language} and {output_language}. The code below is written in {input_language}. Please re-write in the {output_language} language, keeping the same logic. Replace methods and library imports from {input_language} with the equivalent in {output_language} that makes the most sense.\n
"""

def translate(
  code: str,
  input_language = "Java",
  output_language = "Python",
  prompt_template: str = PROMPT_TEMPLATE,
  max_tokens: int = 30000
):
  prompt_template = prompt_template.format(
    input_language = input_language,
    output_language = output_language
  )

  code_template = f"""
  ### Input Code:
  ```

  {code}
  
  ```

  Please re-write the code above in {output_language} language. Include your answer inside the markdown block below.

  ### Output code:
  ```

  """

  prompt = prompt_template + code_template

  headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
  }

  payload = {
    "dataframe_split": {
      "columns": [
        "prompt",
        "max_tokens"
      ],
      "data": [
        [
          prompt,
          max_tokens
        ]
      ]
    }
  }

  response = requests.post(
    url = url,
    headers = headers,
    data = json.dumps(payload)
  )

  return response.json()["predictions"][0]

def render_html(code: str, style="one-dark", linenos = False):

  python_code = code.split("```")[1].split("```")[0]
  html = highlight(
    python_code,
    PythonLexer(),
    HtmlFormatter(
      noclasses = True,
      style = style,
      linenos = linenos
    )
  )

  displayHTML(html)

# COMMAND ----------

import glob
import random

java_examples = glob.glob(f"{FULL_PATH}/*.java")
example_idx = random.randint(0, len(java_examples) - 1)
java_example = java_examples[example_idx]

with open(java_example, "r") as file:
  java_code = file.read()
  py_code = translate(code = java_code, max_tokens = 100000)

# COMMAND ----------

print(py_code)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### To be continued...

# COMMAND ----------


