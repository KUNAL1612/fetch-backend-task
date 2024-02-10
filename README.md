# fetch-backend-task
Original question: https://github.com/fetch-rewards/receipt-processor-challenge.
Brief summary: Used Python's flask libary to define the required endpoints. Used docker to containerize the requirements. Used postman for testing the input/output correctness.
#### Requirements

To run this application, you need the following dependencies:

- Python 3.x
- Flask
- SQLite3 (standard Python library)
- math (standard Python library)
- logging (standard Python library)
- uuid (standard Python library)


### Steps to run:

#### Option 1: Run locally with all required installations
Summary: The code has been written in Python and uses Python's flask library. The best way to run this locally is to install and set up these libraries locally. 

1 .Install python from this [link](https://www.python.org/downloads/) based on your machine 

2. Use python's package manager 'pip' to install flask such as `pip3 install flask`
3. Run the code with `python3 ReceiptProcessor.py`


#### Option 2: Use the provided dockerfile
Summary: The provided DockerFile should do most of the heavy lifting in order to get this project up and running succesfully

1. Move to the directory with the required Dockerfile as provided in this Repository
   
2. If not installed already, install docker on your local machine from [here](https://www.docker.com/products/docker-desktop/)
   
3. Run `docker build -t receipt-processor .`
   
4. Run `docker run -p 10001:10001 receipt-processor`
   (Please note to update the port number if any other process is already using this port on your machine)


### Testing
For testing, it is recommended to use something like [Postman]([url](https://www.postman.com/downloads/)) to call the POST and GET endpoints

Example input for `receipts/process`:
>{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
>
Sample output for the above:
>{
>    "id": "5b9fdd1c-223f-447a-a9d9-2d8f391a1038"
>}



Screenshot example in Postman:
Input receipt:
![image](https://github.com/KUNAL1612/fetch-backend-task/assets/13079247/37a85e82-d3ec-4861-bc5f-bc93aafe2fd9)
Input ID to get the points
![image](https://github.com/KUNAL1612/fetch-backend-task/assets/13079247/47368dd3-cb98-4891-b5ec-d3fc834b3230)

