Presentation details for project:

No more than 10 minutes total!!


1. general project introduction 

**Introduce ourselves (Nathan, Jack)**

**Introduce project -> it's a data ingestion project (into high-level overview of project, example-extract data, transform data, load data)**

**Introduce our project approach (maybe? like breaking big problems into smaller ones, idk)**

**Introduce our perspective to the data sources we chose -> (fun, exciting, etc)**
**Lead this introduction of dataset(so like -> source & source type, volume, structure, issues discovered, etc)**

**Introduce responsibilities of each team member -> into previous project experience (highlights why the project is professionally curated)**


2. problem statement

**Our project solves the problem of having raw, unnormalized data and being able to extract that data, normalize that data and filter out**
**invalid data, missing data, and load that into postgresql database where you can query from and making connections (could be a big talking point)**


3. architecture & pipeline flow
**Architecture-Core modules:**
**Go into detail on Config and Settings**
**Go into detail on Database connection**
**Go into detail on Read / Ingest**
**Go into detail on Transform / Validate**
**Go into detail on Load**  
**Go into detail on Pipelines**                                                                                    
**Go into detail on Orchestration**

**Lead this into separation of concerns (like easier to test)**


**Wrap up with how new data sets could be added (shows our architecture is strong) so like just add new pipeline with transform and validators**
**Basically, you're able to reuse the runner and load and orchestration**


**For the pipeline, just how the data flows through the structure**

4. Showcase ERD/Schema, i.e explain it

5. data cleaning/transformation logic + error handling/logging
**High-level like normalization, the validation chain, rejected records and reason, logging + custom erros**

6. Demo plan slide (overview of what to expect during demonstration) into Demo

7. Challenges and future improvements



2. problem statement what problem is this project solving?
3. introduction to the dataset - source & source type, volume, structure, issues discovered, etc.
4. data cleaning/transformation logic - key transformations performed, data validation rules, handling of null/missing values, deduplication strategy, normalization (ETL/ELT)
5. Schema design - ERD
6. ingestion pipeline flow - visual diagram of your ingestion pipeline (source, ingestion, transformation, database load, logging/error handling)
7. error handling/logging - briefly address how errors are handled and logging practices
8. Performance considerations - bulk inserts vs row-by-row inserts, transactions, query optimization, runtime benchmarks (even rough ones)
9. testing strategy - unit tests or validation queries
10. modularity/code organization - file structure, separation of concerns, reusable functions, config files
11. assumptions/limitations - what are some known weaknesses or limitations of the project? Any real-world scaling limitations?
12. Demo plan slide - a placeholder slide that has a short overview of what to expect during the demonstration (and initiates the actual demonstration of the application)
13. Metrics of success - how is success defined? query response time? Data completeness?
14. Stretch goal slide - what would be the next step if this project were to continue? Any stretch goals you would want implemented to improve this application?


Possible structure to fill your 10 minutes:

1. Title & Problem Statement (1 min)
2. Dataset & Data Characteristics (1 min)
3. Architecture & Pipeline Flow (2 min)
4. ERD & Schema Rationale (2 min)
5. Transformations & Data Quality Handling (1–2 min)
6. Challenges & Trade-offs (1 min)
7. Demo (2–3 min)
8. Stretch Goals & Production Scaling (1 min)


