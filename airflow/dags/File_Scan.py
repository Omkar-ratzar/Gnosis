from airflow.sdk import dag, task
from app.config.config import config
from app.tasks.processing.validate import is_valid

@dag(dag_id="file_scanner")
def file_scan():
    @task
    def walk_dir(**kwargs):
        print("Walking through Directory")
        ti=kwargs['ti']
        #IMPLEMENT FUNCTION TO SCAN THE DIRECTORY WITH HELP OF POSTGRES
        #USING RAANDOM DATA RN TO STIMULATE DAG WITHOUT PG
        new_files={"files":["xyz.doc","abc.img"]}
        ti.xcom_push(key='return_result', value=new_files)

    @task
    def validate_files(**kwargs):
        ti=kwargs['ti']
        new_files=ti.xcom_pull(task_ids='walk_dir',key='return_result')['files']
        files_to_be_processed=list(new_files.values())
        valid_files=[]
        invalid_files=[]
        for file in files_to_be_processed:
            if(is_valid(file)):
                valid_files.append(file)
            else:
                invalid_files.append(file)

        #mark_valid_files(valid_files)
        #mark_invalid_files(invalid_files)

        #if images exist in any valid file: output new image asset
        #if document exist in any valid file: output new document asset






file_scan()
