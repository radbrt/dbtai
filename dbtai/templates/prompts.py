languages = {
  "english": {
    "system_prompt": """
    You are a data analyst, and read business documentation as well as SQL to create documentation for new dbt models. 
    The audience for the documentation is business analysts, so keep the technical descriptions brief and focus instead on the business meaning of the data. 
    If the documentation is too long, people won't read it, so keeo it consise. Write all the documentation in English
    """,
    
    "create_docs_prompt": """
Create a table description for the dbt model `{model_name}`, given the following:

The code for the model:
```
{raw_code}
```

Description of the upstream models:
{model_description}

The output should be a JSON with the following structure:
{{
    "name": "{model_name}",
    "description": "The description of the model"
    "columns": [
      {{"name": "column1", "description": "The description of the column"}},
      {{"name": "column2", "description": "The description of the column"}},
      ...
      ]
}}
""",

"explain_system_prompt": """
You are a data engineer, fluent in SQL and dbt. Your task is to explain dbt/SQL code provided by data analysts. 
The analysts have a basic grasp of SQL, but are not able to follow complex logic. 
Your explanations should be clear and concise, and should help the analysts understand both the logic of the code and why it is written that way.
""",

"explain_prompt": """
Please explain the code for the following dbt model, named {model_name}, in a clear and concise manner. The code is:

```
{raw_code}
```

The upstream models referenced in the code are:
{upstream_models}

The documentation of the model itself is:
{model_description}
"""
},
  "norwegian": {
    "system_prompt": "Du er en data analytiker, og leser både faglig, domenespesifikk dokumentasjon og SQL for å lage dokumentasjon for nye dbt-modeller. Målgruppen for dokumentasjonen er forretningsanalytikere, så hold de tekniske beskrivelsene korte og fokuser heller på forretningsbetydningen av dataene. Hvis dokumentasjonen er for lang, vil folk ikke lese den, så hold den kortfattet. Skriv all dokumentasjon på norsk.",
    "create_docs_prompt": """
Opprett en tabell-beskrivelse for dbt-modellen {model_name}, gitt følgende:

Koden for modellen:

```
{raw_code}
```

Beskrivelse av oppstrømsmodellene:
{model_description}

Resultatet skal være en JSON med følgende struktur:
{{
    "name": "{model_name}",
    "description": "<Beskrivelsen av modellen>"
    "columns": [
      {{"name": "kolonne1", "description": "<Beskrivelsen av kolonnen>"}},
      {{"name": "kolonne2", "description": "<Beskrivelsen av kolonnen>"}}
      ...
      ]
}}
""",
"explain_system_prompt": """
  Du er en dataingeniør, flytende i SQL og dbt. Oppgaven din er å forklare dbt-/SQL-koden som er levert av dataanalytikerne. 
  Analytikerne har grunnleggende kunnskaper i SQL, men er ikke i stand til å følge kompleks logikk. 
  Forklaringene dine bør være klare og konsise, og de bør hjelpe analytikerne med å forstå både logikken i koden og hvorfor den er skrevet på den måten.
""",
"explain_prompt": """
Vennligst forklar koden for følgende dbt-modell, med navn {model_name}, på en klar og kortfattet måte. Koden er:

```
{raw_code}
```

De oppstrømsmodellene som refereres i koden er: 
{upstream_models}

Dokumentasjonen av selve modellen er: 
{model_description}
"""
  },
  "chinese": {
    "prompt": "你是一个数据分析师和业务分析师， 阅读商务文档以及SQL来为新的dbt模型创建文档。文档的受众是商务分析师， 因此请将技术描述保持简洁，并且更多地关注数据的业务含义。如果文档太长，人们就不会阅读，所以请保持简洁。请用中文写所有的文档。",

    "create_docs_prompt": """
为dbt模型`{model_name}`创建一个表描述，给定以下信息：

模型的代码:

```
{raw_code}
```

上游模型的描述:
{model_description}

输出应该是一个JSON，具有以下结构:
{{
    "name": "{model_name}",
    "description": "模型的描述"
    "columns": [
      {{"name": "列1", "description": "列的描述"}},
      {{"name": "列2", "description": "列的描述"}},
      ...
      ]
}}
""",

"explain_system_prompt": """
  你是一名数据工程师，精通SQL和dbt。你的任务是解释数据分析师提供的dbt/SQL代码。这些分析师对SQL有基本的了解，但无法理解复杂的逻辑。你的解释应该清晰且简洁，既要帮助他们理解代码的逻辑，也要让他们明白为什么代码会以那样的方式编写。
""",
"explain_prompt": """
请清晰且简洁地解释以下名为{model_name}的dbt模型的代码。代码如下：


```
{raw_code}
```

代码中引用的上游模型有：
{upstream_models}

模型本身的文档说明是：
{model_description}
"""
  },
  "spanish": {
    "prompt": "Eres un analista de datos y lees documentación de negocios y SQL para crear documentación para nuevos modelos de dbt. La audiencia para la documentación son analistas de negocios, por lo que mantén las descripciones técnicas breves y concéntrate en el significado comercial de los datos. Si la documentación es demasiado larga, la gente no la leerá, así que mantenla concisa. Escribe toda la documentación en español.",
    "create_docs_prompt": """
Cree una descripción de tabla para el modelo dbt `{model_name}`, dada la siguiente información:

El código para el modelo:
```
{raw_code}
```

Descripción de los modelos ascendentes:
{model_description}

La salida debe ser un JSON con la siguiente estructura:
{{
    "name": "{model_name}",
    "description": "La descripción del modelo"
    "columns": [
      {{"name": "columna1", "description": "La descripción de la columna"}},
      {{"name": "columna2", "description": "La descripción de la columna"}},
      ...
      ]
}}
""",
"explain_system_prompt": """
  Eres un ingeniero de datos, con fluidez en SQL y dbt. Tu tarea es explicar el código dbt/SQL proporcionado por los analistas de datos. 
  Los analistas tienen un conocimiento básico de SQL, pero no pueden seguir lógicas complejas. 
  Tus explicaciones deben ser claras y concisas, y deben ayudar a los analistas a comprender tanto la lógica del código como el motivo por el cual está escrito de esa manera.
""",

"explain_prompt": """
Por favor, explique el código para el siguiente modelo dbt, llamado {model_name}, de manera clara y concisa. El código es:

```
{raw_code}
```

Los modelos previos referenciados en el código son:
{upstream_models}

La documentación del propio modelo es:
{model_description}
"""
  },
  "french": {
    "prompt": "Vous êtes un analyste de données, et lisez de la documentation métier ainsi que du SQL pour créer de la documentation pour de nouveaux modèles dbt. Le public pour la documentation est composé d'analystes métier, alors gardez les descriptions techniques brèves et concentrez-vous plutôt sur la signification métier des données. Si la documentation est trop longue, les gens ne la liront pas, alors gardez-la concise. Écrivez toute la documentation en français.",
    "create_docs_prompt": """
Créez une description de table pour le modèle dbt `{model_name}`, étant donné les informations suivantes:

Le code pour le modèle:
```
{raw_code}
```

Description des modèles amont:
{model_description}

La sortie doit être un JSON avec la structure suivante:

{{
    "name": "{model_name}",
    "description": "La description du modèle"
    "columns": [
      {{"name": "colonne1", "description": "La description de la colonne"}},
      {{"name": "colonne2", "description": "La description de la colonne"}},
      ...
      ]
}}
""",
"explain_system_prompt": """
Vous êtes ingénieur de données, maîtrisant SQL et dbt. Votre tâche consiste à expliquer le code dbt/SQL fourni par les analystes de données. 
Les analystes possèdent une compréhension basique de SQL, mais ne sont pas capables de suivre une logique complexe. 
Vos explications doivent être claires et concises, et devraient aider les analystes à comprendre à la fois la logique du code et la raison pour laquelle il est écrit de cette manière.
""",

"explain_prompt": """
Veuillez expliquer le code pour le modèle dbt suivant, nommé {model_name}, de manière claire et concise. Le code est :

```
{raw_code}
```

Les modèles en amont référencés dans le code sont : 
{upstream_models}

La documentation du modèle lui-même est : 
{model_description}
"""
  },
  "german": {
    "prompt": "Sie sind ein Datenanalyst und lesen Geschäftsdokumentationen sowie SQL, um Dokumentationen für neue dbt-Modelle zu erstellen. Die Zielgruppe für die Dokumentation sind Geschäftsanalysten, daher halten Sie die technischen Beschreibungen kurz und konzentrieren Sie sich stattdessen auf die Geschäftsbedeutung der Daten. Wenn die Dokumentation zu lang ist, werden sie nicht gelesen, also halten Sie sie kurz. Schreiben Sie alle Dokumentationen auf Deutsch.",
    "create_docs_prompt": """
Erstellen Sie eine Tabellenbeschreibung für das dbt-Modell `{model_name}`, basierend auf folgenden Informationen:

Der Code für das Modell:

```
{raw_code}
```

Beschreibung der übergeordneten Modelle:
{model_description}

Die Ausgabe sollte ein JSON mit folgender Struktur sein:
{{
    "name": "{model_name}",
    "description": "Die Beschreibung des Modells"
    "columns": [
      {{"name": "Spalte1", "description": "Die Beschreibung der Spalte"}},
      {{"name": "Spalte2", "description": "Die Beschreibung der Spalte"}},
      ...
      ]
}}
""",
"explain_system_prompt": """
  Sie sind ein Daten-Ingenieur, fließend in SQL und dbt. Ihre Aufgabe ist es, den von Datenanalysten bereitgestellten dbt/SQL-Code zu erklären. 
  Die Analysten haben grundlegende Kenntnisse in SQL, sind aber nicht in der Lage, komplexe Logik nachzuvollziehen. 
  Ihre Erklärungen sollten klar und prägnant sein und den Analysten helfen, sowohl die Logik des Codes als auch die Gründe für seine spezifische Ausgestaltung zu verstehen.
  """,

"explain_prompt": """
Bitte erklären Sie den Code für das folgende dbt-Modell, mit dem Namen {model_name}, auf eine klare und prägnante Weise. Der Code lautet:

```
{raw_code}
```

Die im Code referenzierten vorgelagerten Modelle sind: 
{upstream_models}

Die Dokumentation des Modells selbst ist: 
{model_description}
"""
  }
}

UNITTEST = """
Write a dbt Unit test. A unit test mocks the inputs to a dbt model, provides csv files in their stead, and verifies that the result of the model code given the mocked input matches a provided csv file. 

An example of a dbt unit test can be the following:

The dbt model code for model named "all_customers":

```
WITH customers AS (
  SELECT * FROM {{ ref('seed_customers') }}
),
countries AS (
  SELECT * FROM {{ ref('seed_countries') }}
),
countries_customers AS (
  SELECT
    countries.name AS country_name,
    customers.name AS customer_name
  FROM countries
  JOIN customers ON countries.name = customers.country
),
country_report AS (
  SELECT country_name, 
  COUNT(*) AS customer_count 
  FROM countries_customers 
  GROUP BY country_name
)
SELECT * FROM country_report
```

The Unit test:

```
unit_tests:
  # Test both columns
  - name: unit_report # this is the unique name of the test
    model: country_report # name of the model I'm unit testing
    given: # optional: list of inputs to provide as fixtures
      - input: ref('seed_customers')
        format: csv
        rows: |
          ix,name,country
          1,Frodo,middle earth
          2,Mr. Tumnus,narnia
          3,Lucy,narnia
      - input: ref('seed_countries')
        format: csv
        rows: |
          name
          middle earth
          narnia
    expect: # required: the expected output given the inputs above
      format: csv
      rows: |
        country_name,customer_count
        narnia,2
        middle earth,1
```


Write a unit test for the model `{model_name}`. The model description is:

{model_description}

The model code is:

```
{raw_code}
```

{extra_instructions}

The output should be a JSON containing a key "unit_test" with the YAML as a string, as shown in the example above, and the key "explanation" with a string explaining the test.
"""

GENERATE_MODEL_SYSTEM_PROMPT = """
You are a data engineer, fluent in SQL and dbt, and are tasked with creating a new dbt model. The model should be a SQL query that returns a table. They are formatted as CTEs, and select from other other dbt models (tables) using the jinja reference "{{ ref('model_name') }}" instead of a table name.

A dbt model is a SQL query that returns a table. They are formatted as CTEs, and select from other other dbt models (tables) using the jinja reference "{{ ref('model_name') }}" instead of a table name.

An example of a dbt model:

```
WITH customers AS (
  SELECT * FROM {{ ref('seed_customers') }}
),
countries AS (
  SELECT * FROM {{ ref('seed_countries') }}
),
countries_customers AS (
  SELECT
    countries.name AS country_name,
    customers.name AS customer_name
  FROM countries
  JOIN customers ON countries.name = customers.country
),
country_report AS (
  SELECT country_name, 
  COUNT(*) AS customer_count 
  FROM countries_customers 
  GROUP BY country_name
)
SELECT * FROM country_report
```

It is important for model clarity to use CTEs, and that the final SQL statement is a SELECT star statement without any logic. 
The logic should be in the CTEs.
"""

GENERATE_MODEL = """
Write a dbt model named `{model_name}`, with the following description:

{description}

The model should use the following upstream models:

{upstream_docs}

The output should be a JSON containing a key "code" with the dbt model code, and a key "explanation" with a string explaining the code.
"""

FIX_MODEL_PROMPT = """
Given the following dbt model code:
{model_code}

Change the model code to fix the following issue:
{issue}

The tables referenced in the code are the following:
{tables}


The output should be a JSON containing a key "code" with the dbt model code, and a key "explanation" with a string explaining the changes made.
"""


FIX_CODE_PROMPT = """
Given the following dbt model code:
{model_code}

Rewrite the code for better clarity and to adhere to the dbt coding style:

- Field names, keywords, and function names should all be lowercase.
- Indents should be four spaces.
- Use trailing commas.
- Avoid table aliases in join conditions (especially initialisms) — it's harder to understand what the table called "c" is as compared to "customers".
- The as keyword should be used explicitly if aliasing a field or table.
- Fields should be stated before aggregates and window functions.
- Aggregations should be executed as early as possible (on the smallest data set possible) before joining to another table to improve performance.
- Ordering and grouping by a number (eg. group by 1, 2) is preferred over listing the column names (see this classic rant for why). Note that if you are grouping by more than a few columns, it may be worth revisiting your model design.
- Prefer union all to union unless you explicitly want to remove duplicates.
- If joining two or more tables, always prefix your column names with the table name. If only selecting from one table, prefixes are not needed.
- Be explicit about your join type (i.e. write inner join instead of join).
- Always move left to right to make joins easy to reason about - right joins often indicate that you should change which table you select from and which one you join to.
- All {{ ref('...') }} statements should be placed in CTEs at the top of the file.
- 'Import' CTEs should be named after the table they are referencing.
- Limit the data scanned by CTEs as much as possible. Where possible, only select the columns you're actually using and use where clauses to filter out unneeded data.
- Where performance permits, CTEs should perform a single, logical unit of work.
- CTE names should be as verbose as needed to convey what they do e.g. events_joined_to_users instead of user_events (this could be a good model name, but does not describe a specific function or transformation).


In-model configurations should be specified like this for maximum readability:
```
{{
    config(
      materialized = 'table',
      sort = 'id',
      dist = 'id'
    )
}}
```

The output should be a JSON containing a key "code" with the dbt model code, and a key "explanation" with a string explaining the changes made.
"""