# Databricks notebook source
import gc
import torch
from transformers import pipeline
import os

gc.collect()
torch.cuda.empty_cache()
persist = False

if os.path.exists("/dbfs/starchat"):

    tokenizer = "/dbfs/starchat/tokenizer"
    model = "/dbfs/starchat/model"
else:
    tokenizer = "HuggingFaceH4/starchat-beta"
    model = "HuggingFaceH4/starchat-beta"
    persist = True

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

if persist:
    pipe.tokenizer.save_pretrained("/dbfs/starchat/tokenizer")
    pipe.model.save_pretrained("/dbfs/starchat/model")

# COMMAND ----------

from utils.starchat import StarChatHelper

generate = StarChatHelper(pipeline = pipe)

# COMMAND ----------

# DBTITLE 1,Sample 1: PL/SQL to SparkSQL
plsql = """
-- Calculate salary for employees by taking commission and bonus into account
set serveroutput on
declare 
  cursor empcur is 
    select first_name, salary, commission_pct
    from employees;
    
  v_salary employees.salary%type;   
begin 
   for emprec in empcur
   loop 
       -- Calculate salary + commission 
       v_salary := emprec.salary +  emprec.salary * nvl(emprec.commission_pct,0);
       -- Add bonus of 10% or 5% based on commission pct                   
       if emprec.commission_pct is not null then
           v_salary := v_salary  + emprec.salary * 0.10;
       else
           v_salary := v_salary  + emprec.salary * 0.05;
       end if;
       
       dbms_output.put_line( rpad(emprec.first_name,20) ||  to_char(v_salary,'99,999.00'));
   end loop;
end;
"""

# COMMAND ----------

# Define the instruction and the code here
instruction = "Assume your job is to convert this piece of code from PL/SQL language to PySpark. Consider the code below:"

# Generate output
pyspark_output = generate.generate_response(instruction, plsql)

# COMMAND ----------

from IPython.display import Markdown

display(Markdown(pyspark_output))

# COMMAND ----------

# DBTITLE 1,Sample 2: Explain PL/SQL
# Define the instruction and the code here
instruction = "Assume your job is to explain the piece of PL/SQL code below to a junior developer. Please generate a detailed explanation. Consider the code below:"

# Generate output
plsql_explanation_output = generate.generate_response(instruction, plsql)

# COMMAND ----------

print(plsql_explanation_output)

# COMMAND ----------

pyspark_code = pyspark_output.split("```python")[1].split("```")[0]
print(pyspark_code)

# COMMAND ----------

# DBTITLE 1,Sample 3: Explain PySpark
# Define the instruction and the code here
instruction = "Assume your job is to explain the piece of PySpark code below to a junior developer. Please generate a detailed explanation. Consider the code below:"

# Generate output
pyspark_explanation_output = generate.generate_response(
    instruction,
    pyspark_code
)

# COMMAND ----------

print(pyspark_explanation_output)

# COMMAND ----------


