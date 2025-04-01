# Snowpark Libs
from snowflake.snowpark.version import VERSION
from snowflake.snowpark.session import Session
import snowflake.snowpark.functions as F
import snowflake.snowpark.types as T
from snowflake.snowpark.functions import col,to_date, udf, concat_ws, call_function, lit, concat
# Data Science Libs
import pandas as pd
import os
import dotenv
from pathlib import Path
from datetime import datetime
import numpy as np
import datetime
import pandas as pd
import re
#Snowflake Cortext
from snowflake.cortex import Complete, Summarize
# If there are any certificates issues, run the command: /Applications/Python\ 3.9/Install\ Certificates.command


# Read config parser .ini file with your connection information

Path = ".env"

# SSO - KochID
connection_parms = {
    "account": os.getenv('account'),
    "user": os.getenv('email'),
    "authenticator": os.getenv('authenticator'),
    "database": os.getenv('database'),
    "schema": os.getenv('schema'),
    "warehouse": os.getenv('warehouse'),"role": os.getenv('role')
} 

# Create Snowflake Session object
session = Session.builder.configs(connection_parms).create()
session.sql_simplifier_enabled = True

snowflake_environment = session.sql('SELECT current_user(), current_version()').collect()
snowpark_version = VERSION

nylon_recycling = pd.read_excel(r"./data/raw_data/N66 Recycle Depoly Field_010925 Test_2025-03-30.xlsx", skiprows=1)
nylon_recycling.columns = [re.sub(r'[^a-zA-Z0-9]', "_",\
                         col.replace(' ', "_")).upper() for col in nylon_recycling.columns]
session.create_dataframe(nylon_recycling).write.mode("overwrite").save_as_table("NYLON_RECYCLING_SAMPLE")

# Read the table and limit to the first two rows
df = session.table("NYLON_RECYCLING_SAMPLE").limit(2)

# Combine the title, abstract, and claims columns into a single text column
df_combined = df.with_column(
    "COMBINED_TEXT",
    concat(
        lit("TITLE: "), col("TITLE__ENGLISH_"), lit("\nABSTRACT: "), col("ABSTRACT__ENGLISH_"),
        lit("\nCLAIMS: "), col("CLAIMS__ENGLISH_")
    )
)
# Define your instructions and context for the summarization
instructions = "Summarize the following patent information concisely in no more than 300 words, keeping all key points."
context = "The patent information includes title, abstract, and claims."
# Now call the COMPLETE function using the provided pattern:
# Complete(model, f"Instructions:{instructions}, Context:{context}, Prompt:{prompt}")
df_summary = df_combined.with_column(
    "SUMMARY",
    call_function(
        "SNOWFLAKE.CORTEX.COMPLETE",
        lit("snowflake-arctic"),  # Change to your preferred model if needed
        concat(
            lit(f"Instructions: {instructions}, Context: {context}, Prompt: "),
            col("COMBINED_TEXT")
        )
    )
)

# Select the output columns and show the results
df_result = df_summary.select("PUBLICATION_NUMBER", "SUMMARY", "TITLE__ENGLISH_", "ABSTRACT__ENGLISH_", "CLAIMS__ENGLISH_")
df_result.show()