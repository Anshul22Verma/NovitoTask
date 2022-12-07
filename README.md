# Documentation
Original README in [README_TASK.md](README_TASK.md)

## Setup 

I used `python 3.10` to build the project and all the requirements are mentioned in `requirements.txt`, all the packages are suppose to be the latest package versions.
To install the requirements in your virtual environment run the following command from the project directory.

```bash
pip install -r requirements.txt
```

I havent changed the original `test.db` location and the `metrics.csv` file and the files can be run on their own without any argument.

### 1. How did you complete the DB schema. You need to at least provide a SQL statement.

Used SQL command to create the table if it does not exist in the database, function `create_value_definition_table` in `db_ops.py` file executes this table creation query.

I have also added `argparse` to the `db_ops.py` file, although it can be run on its own with the default argument pointing to the data and db files in the repository one can change them to a local file by running the file as a module like:

```bash
python -m db_ops --db_file <locationOfDBfile> --csv_file <locationOfCSVFile>
```

Ex:
```bash
python -m db_ops --db_file ./db/test.db --csv_file ./resources/metrics.csv
```

This file can only be run once and it creates the needed table and adds the values to the database, rerunning it will not throw any error but create duplicate records in the `value_definition` table. 

### 2. How to import the CSV to the SQL database. Document the entry point in your software to do so.

Ex:
```bash
python -m db_ops --db_file ./db/test.db --csv_file ./resources/metrics.csv
```

if you manually want to just change the file paths and run the db_ops.py file then you will need to edit line `104` and `106` in `db_ops.py` file and run it. Output after running `db_ops.py` file

```python
----------   Table after insert   ----------


----------     Table metric     ----------
[id, code, description]
row 1:  (3, 'TB-001', 'Dog related')
row 2:  (4, 'TB-002', 'TV related')


----------     Table value_definition     ----------
[id, label, type, metric_id]
row 1:  (1, 'How many dogs do you own?', 'number', 3)
row 2:  (2, 'Favorite color of dog', 'text', 3)
row 3:  (3, 'Favorite show', 'text', 4)
row 4:  (4, 'Average hours per week spent watching tv', 'number', 4)
row 5:  (5, 'Favorite actor', 'text', 4)
```


### 3. How to start your web framework, document the entry point in your software to do so.

I have created a fast API application without any front end and the API returning JSONs as requested to run it I use `uvicorn`. To run the web framework run the following command from the project directory

```bash
uvicorn inference.app:app --host 0.0.0.0 --port 80
```

You might need `sudo` if you do not access to this port.

### 4. How to call your API endpoint to read the database and show the result of your route(s). Document your route(s).

Example is shown in `inference/demo.py` you can make CURL request with POST to get responses for your needs.

I have created two APIs for querying and one for information
i) just run `<host>:80` -> to get information about the app
ii) run `<host>:80/query`, with payload template [payload_query](./inference/payload_query.json) -> to run a custom Query against the DB and get information in respose.
ii) run `<host>:80/getMetaData`, with payload template [payload_metadata](./inference/payload_metadata.json) -> to get a **csv** like `./resources/metrics.csv` like df-dictonary for desired metric_code mentioned in the payload.


Output after running `./inference/demo.py`
```python
{"message": "Novisto Demo"}

{"queryResult": "[(3, 'TB-001', 'Dog related'), (4, 'TB-002', 'TV related')]"}

{"metadata": 
    {
        "metric_code": ["TB-002","TB-002","TB-002"],
        "metric_description":["TV related","TV related","TV related"],
        "value_label":["Favorite show","Average hours per week spent watching tv","Favorite actor"],
        "value_type":["text","number","text"]
    }
}
```

### 5. Any additional documentation you wish to provide or is required to run your project.

The project contains a Dockerfile which was used to create the docker image in **AWS ECR** and then this **ECR** was hosted in **ECS** using **fargate**

 Docker related commands: 

1. To create a docker image, run `docker build -t novito .`
2. To host the docker in the instance rather than pushing it to ECR and using ECS to deploy, run `docker run -p 80:80 --cpus 2 novito`

3. To deploy it using ECR and ECS fargate we can just use the AWS console, and CLI to create the ECR and then host using the ECS. ref: [AWS ref](https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-ecs-ecr-codedeploy.html)
