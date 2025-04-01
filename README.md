# Snowflake Cortex Summarizer

## Project Overview
This project leverages Snowflake Snowpark and Snowflake Cortex to summarize patent-related information such as title, abstract, and claims. It demonstrates how to combine text fields, generate summaries using Cortex's LLM capabilities, and export the output to Excel.

## Table of Contents
- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Setup Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/chitrakumarsai-inv/3pp-summary-sf-nonprod.git
    ```
2. Navigate to the project directory:
    ```bash
    cd 3pp-summary-sf-nonprod
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file with your Snowflake connection details:
    ```
    account=<your_account>
    email=<your_email>
    authenticator=externalbrowser
    database=<your_database>
    schema=<your_schema>
    warehouse=<your_warehouse>
    role=<your_role>
    ```

5. Make sure Cortex is enabled for your role with `SNOWFLAKE.CORTEX_USER` privileges.

## Usage
- Load and preprocess your Excel data.
- Write the data to a Snowflake table using Snowpark.
- Combine relevant text columns and generate a summary using:
  ```python
  SNOWFLAKE.CORTEX.COMPLETE(
      'snowflake-arctic',
      'Instructions: Summarize the following patent information concisely in no more than 300 words, keeping all key points. Context: The patent information includes title, abstract, and claims. Prompt: ...'
  )
