import os

if __name__ == "__main__":
    # sanity check 
    os.system('curl http://0.0.0.0:80/')
    print("\n")

    # making a post custom query request
    os.system('curl -X POST http://0.0.0.0:80/query -H "Content-Type: application/json" -d @inference/payload_query.json')
    print("\n")

    # making a post request to get all the metadata for a metric_code
    os.system('curl -X POST http://0.0.0.0:80/getMetaData -H "Content-Type: application/json" -d @inference/payload_metadata.json')
    print("\n")