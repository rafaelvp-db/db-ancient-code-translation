# Databricks notebook source
databricks_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
url = databricks_url + "/serving-endpoints/llama2/invocations"

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Simple Example: C++ to Python

# COMMAND ----------

cpp_code = """
int i = 0;
while (i < 5) {
  cout << i << "\n";
  i++;
}
"""

# COMMAND ----------

import requests
import json
import re

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

PROMPT_TEMPLATE = """
  Assume you are an expert both in Python and C++. The code below is in C++. Please re-write in the Python language, keeping the same logic. Replace functions from C++ with the equivalent in Python that makes the most sense.\n
"""

def translate(
  prompt_template: str = PROMPT_TEMPLATE,
  code: str = cpp_code,
  max_tokens: int = 1000
):

  code_template = f"""
  ### C++ Code:
  ```cpp
  {code}
  ```

  Please re-write the code above in Python language.

  ### Python code:
  ```python
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

def post_process(code: str, format_: str = "markdown", style="one-dark", linenos = False):

  python_code = code.split("```python")[1].split("```")[0]
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

py_code = translate()
post_process(py_code)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### To be continued...

# COMMAND ----------


