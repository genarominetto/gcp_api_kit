from google.cloud import bigquery
from google.api_core.exceptions import Conflict

class BigQueryTable:
    def __init__(self, dataset_id, table_id, columns, SERVICE_ACCOUNT_CREDENTIALS):
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.columns = columns
        self.SERVICE_ACCOUNT_CREDENTIALS = SERVICE_ACCOUNT_CREDENTIALS
        self.client = bigquery.Client.from_service_account_json(self.SERVICE_ACCOUNT_CREDENTIALS)
        self.create_table()

    def create_table(self):
        dataset = bigquery.Dataset(self.client.dataset(self.dataset_id))
        dataset.location = "US"
        try:
            self.client.create_dataset(dataset)
            print("Dataset {} created".format(self.dataset_id))
        except Conflict:
            print("Dataset {} already exists".format(self.dataset_id))

        schema = [bigquery.SchemaField(*col.split()) for col in self.columns.split(',')]
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        table = bigquery.Table(table_ref, schema=schema)
        try:
            self.client.create_table(table)
        except Conflict:
            print("Table {} already exists".format(self.table_id))

        print(f'Table {self.table_id} created in dataset {self.dataset_id}')
        
    def execute_command(self, sql_query):
        command = sql_query.format(dataset=self.dataset_id, table=self.table_id)
        query_job = self.client.query(command, location="US")
        results = query_job.result()
        return results

    def insert_records(self, records):
        columns = ', '.join(col.split()[0] for col in self.columns.split(','))
        max_id_result = self.read_records("TRUE ORDER BY ID DESC LIMIT 1")

        # Initialize max_id to 0 if there are no records yet
        max_id = max_id_result[0][0] if max_id_result else 0

        if isinstance(records, list):
            for record in records:
                max_id += 1
                record_values = record.split(", ", 1)[1]  # skip the first element (NULL)
                self.execute_command(f"INSERT INTO `{self.dataset_id}.{self.table_id}` ({columns}) VALUES ({max_id}, {record_values})")
            print(f'Multiple records inserted into table {self.table_id} in dataset {self.dataset_id}')
        else:
            max_id += 1
            record_values = records.split(", ", 1)[1]  # skip the first element (NULL)
            self.execute_command(f"INSERT INTO `{self.dataset_id}.{self.table_id}` ({columns}) VALUES ({max_id}, {record_values})")
            print(f'Record inserted into table {self.table_id} in dataset {self.dataset_id}')
            
    def read_records(self, condition="TRUE"):
        row_iterator = self.execute_command(f"SELECT * FROM {self.dataset_id}.{self.table_id} WHERE {condition}")
        return [tuple(row.values()) for row in row_iterator]
    
    def delete(self, entity):
        if entity == 'table':
            table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
            try:
                self.client.delete_table(table_ref)
                print(f"Table {self.table_id} deleted from dataset {self.dataset_id}")
            except Exception as e:
                print(f"Error occurred while deleting table {self.table_id} from dataset {self.dataset_id}: {e}")
        elif entity == 'dataset':
            dataset_ref = self.client.dataset(self.dataset_id)
            try:
                self.client.delete_dataset(dataset_ref, delete_contents=True)
                print(f"Dataset {self.dataset_id} and its contents deleted successfully")
            except Exception as e:
                print(f"Error occurred while deleting dataset {self.dataset_id}: {e}")
        elif entity == 'table_content':
            sql = f"DELETE FROM `{self.dataset_id}.{self.table_id}` WHERE TRUE"
            try:
                self.client.query(sql)
                print(f"Table {self.table_id} contents deleted in dataset {self.dataset_id}")
            except Exception as e:
                print(f"Error occurred while deleting table {self.table_id} contents in dataset {self.dataset_id}: {e}")
