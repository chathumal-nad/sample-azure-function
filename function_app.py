import azure.functions as func
import logging
from datetime import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.debug('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        logging.info(f"Hello, {name}. This HTTP triggered function executed successfully.")
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


@app.route(route="blob_output")
@app.blob_output(arg_name="outputblob",
                path="blob-output/test.txt",
                connection="WEBSITE_CONTENTAZUREFILECONNECTIONSTRING")
def blob_output(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    # Get the query parameter from the request
    parameter_value = req.params.get('parameter')

    # Check if the parameter is present in the query
    if not parameter_value:
        return func.HttpResponse("Please provide a 'parameter' in the query.", status_code=400)

    # Log the parameter value
    logging.info(f'Received parameter: {parameter_value}')

    # Set the parameter value to the output blob
    outputblob.set(parameter_value)

    return func.HttpResponse(f"Parameter '{parameter_value}' written to the Blob Storage container.", status_code=200)



@app.blob_trigger(arg_name="myblob", path="blob-trigger/{name}",
                               connection="WEBSITE_CONTENTAZUREFILECONNECTIONSTRING") 
def BlobTrigger(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")



# seconds, minutes, hour, day of the month, month, day of the week
@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    
    if myTimer.past_due: # if the function failed to execute in the given time
        logging.info('The timer is past due!')

    logging.info(f'Python timer trigger function executed. Datetime : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')