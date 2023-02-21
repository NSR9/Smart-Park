import json
from pymongo import MongoClient, errors

def lambda_handler(event, context):
    # TODO implement
        responseObject = {}
        headers = event['headers']
        print(headers)
        
        params = event['resource']
        parking_lot_uuid = params.split('/')[2]
        
        if parking_lot_uuid == "":
            responseObject["statusCode"] = 400
            responseObject["headers"] = {}
            responseObject["headers"]["Content-Type"] = "error"
            response["body"] = "N parking_lot_uuid"
        elif len(parking_lot_uuid) < 35:
            responseObject["statusCode"] = 400
            responseObject["headers"] = {}
            responseObject["headers"]["Content-Type"] = "error"
            response["body"] = "Invalid parking_lot_uuid"
            
        print(parking_lot_uuid)
  
        DOMAIN = '54.186.63.33'
        PORT = 27017

  # use a try-except indentation to catch MongoClient() errors
        try:
    # try to instantiate a client instance
            client = MongoClient(
              host = [ str(DOMAIN) + ":" + str(PORT) ],
              serverSelectionTimeoutMS = 3000, # 3 second timeout
              username = "root",
              password = "12345",
              )
    
      # print the version of MongoDB server if connection successful
            print ("server version:", client.server_info()["version"])
    
            database = client.plv_detection_data
            collection = database.ResultsAndImagelinks
            
            query = { "parking_lot_uuid": parking_lot_uuid }
             
            db_record = collection.find(query).sort('_id',-1).limit(1)
            mongo_record = db_record[0]
           
    # get the database_names from the MongoClient()
            database_names = client.list_database_names()

        except errors.ServerSelectionTimeoutError as err:
      # set the client and DB name list to 'None' and `[]` if exception
            client = None
            database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
            print ("pymongo ERROR:", err)

        #print ("\ndatabases:", database_names)
        
        
    # Creating the Mongo response object
        mongoResponseObject = {
            "parking_lot_name": mongo_record['parking_lot_name'],
            "parking_lot_uuid": mongo_record['parking_lot_uuid'],
            "number_of_vehicles": mongo_record['number_of_vehicles'],
            "number_of_empty_parking_slots":mongo_record['number_of_empty_parking_slots'],
            "timestamp": mongo_record['timestamp'],
            "image_s3_http_url": mongo_record['image_s3_http_url']
         }

    
    
    
    #Creating a HTTP response object    
       
        responseObject["statusCode"] = 200
        responseObject["headers"] = {}
        responseObject["headers"]["Content-Type"] = "application/json"
        responseObject["body"] = json.dumps(mongoResponseObject)
        print(responseObject)
        return responseObject