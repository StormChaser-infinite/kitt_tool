import azure.functions as func
import logging

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="kittsqlmodel/sql-inputs",
                               connection="sqlinputs") 



def sql_input_blob_trigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    
    with open(myblob) as f:
        lines = f.readlines()
        


