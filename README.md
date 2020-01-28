# REST API to find shortest path length in graph

## Description
Web service for very quick shortest path calculations on graph. It precomputes all distances while graph
is being updated and fetches distances from that cache.

### Keep in mind!
 - The service is not secured on application level
 - It stores the graph in-memory so you can scale it only vertically

## How to run development server

### Requirements
 - Python 3.x
 - pip

### Run it

You will need all the dependencies so navigate to the root folder(and probably create new virtual environment) and run:

`pip install -r requirements.txt`

Secondly, run:

`python3 main.py`

And everything should start just fine!

## Endpoints

### PUT `/v1/graph`

This endpoint receives JSON object and sets the in-memory graph as described in the body and returns the newly created 
graph.

Graph schema:
```
{
	"directed": boolean,
	"graph": {
		"name": string,
		"version": number
	},
	"links"(optional): [
	{
		"attributes": {
		    "weight": number
		},
		"source": string,
		"target": string
		}
	],
	
	"nodes": [
		{
		    "id": string
		},
		{
		    "id": string
		}
	]
}
```

Returns
```
{
    "result": <Graph>
}
```

### PUT `/v1/graph/distance/<node1>/<node2>`

This endpoint calculates the shortest path between two nodes send as uri parameters.

Returns
```
{
    "result": number
}
```

### Errors

Format:
```
{
    "errorCode": "<code>", "longDescription": "<human_readable_description>"
}
```
Possible error codes are: `invalidLinkWeight`, `nodeDoesntExist`, `noPathExists`, `internalError`