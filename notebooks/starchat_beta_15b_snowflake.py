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

# DBTITLE 1,Sample 1: Snowflake SQL to PySpark
snowflake_code = """

-- Let us create the table, that contains only the first and the second column from the OrderDetails Table
CREATE OR REPLACE TABLE "OUR_FIRST_DB"."PUBLIC".ORDERS_EX (
    ORDER_ID VARCHAR(30),
    AMOUNT INT
);

-- Transforming using SELECT Statement

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS_EX
    FROM (SELECT s.$1, s.$2 FROM @MANAGE_DB.external_stages.aws_stage s)
    file_format = (type = csv field_delimiter = ',' skip_header = 1)
    files = ('OrderDetails.csv');
    
-- Let's explore the data
SELECT * FROM "OUR_FIRST_DB"."PUBLIC"."ORDERS_EX";


-- Example 2 - Table    

CREATE OR REPLACE TABLE OUR_FIRST_DB.PUBLIC.ORDERS_EX_WITH_FLAG (
    ORDER_ID VARCHAR(30),
    AMOUNT INT,
    PROFIT INT,
    PROFITABLE_FLAG VARCHAR(30) -- This column is not in the original table.. So we have to use SQL Functions to create this
);

-- Example 2 - Copy Command using a SQL function (subset of functions available)

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS_EX_WITH_FLAG
    FROM (select 
            s.$1,
            s.$2, 
            s.$3,
            CASE WHEN CAST(s.$3 as int) < 0 THEN 'not profitable' ELSE 'profitable' END -- The logic, used for creating the fourth column
          from @MANAGE_DB.external_stages.aws_stage s)
    file_format= (type = csv field_delimiter=',' skip_header=1)
    files=('OrderDetails.csv');
    
SELECT * FROM "OUR_FIRST_DB"."PUBLIC"."ORDERS_EX_WITH_FLAG";


-- Example 3 - Table

CREATE OR REPLACE TABLE OUR_FIRST_DB.PUBLIC.ORDERS_EX_TRANSFORM (
    ORDER_ID VARCHAR(30),
    AMOUNT INT,
    PROFIT INT,
    CATEGORY_SUBSTRING VARCHAR(5) -- Transformation to be used here
);


-- Example 3 - Copy Command using a SQL function (subset of functions available)

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS_EX_TRANSFORM
    FROM (select 
            s.$1,
            s.$2, 
            s.$3,
            substring(s.$5,1,5) -- Taking a specific substring only, that is taking the first 5 characters only
          from @MANAGE_DB.external_stages.aws_stage s)
    file_format= (type = csv field_delimiter=',' skip_header=1)
    files=('OrderDetails.csv');


SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS_EX_TRANSFORM;

-- Example 4 - Using subset of columns

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS_EX (ORDER_ID,PROFIT)
    FROM (select 
            s.$1,
            s.$3
          from @MANAGE_DB.external_stages.aws_stage s)
    file_format= (type = csv field_delimiter=',' skip_header=1)
    files=('OrderDetails.csv');

-- Example 5 - Table Auto increment

CREATE OR REPLACE TABLE OUR_FIRST_DB.PUBLIC.ORDERS_EX_AUTO (
    ORDER_ID number autoincrement start 1 increment 1,
    AMOUNT INT,
    PROFIT INT,
    PROFITABLE_FLAG VARCHAR(30)
);

-- Example 5 - Auto increment ID

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS_EX_AUTO (PROFIT,AMOUNT)
    FROM (select 
            s.$2,
            s.$3
          from @MANAGE_DB.external_stages.aws_stage s)
    file_format= (type = csv field_delimiter=',' skip_header=1)
    files=('OrderDetails.csv');


SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS_EX_AUTO WHERE ORDER_ID > 15;
"""

# COMMAND ----------

# Define the instruction and the code here
instruction = "Assume your job is to convert this piece of code from Snowflake SQL language to PySpark. Consider the code below:"

# Generate output
pyspark_output = generate.generate_response(instruction, snowflake_code)

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


