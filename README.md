
# HTTP services

## Problem Statement

#### Develop Average Calculator HTTP Microservice
Create an Average Calculator microservice that exposes a REST API "numbers/{numberid}" that exclusively accepts qualified number IDs.
- Qualified IDs include 'p' for prime, 'f' for Fibonacci, 'e' for even, and 'r' for random numbers.
- Upon each request, fetch numbers from a third-party server and store them.
- Ensure stored numbers are unique, disregarding duplicates. 
- Ignore responses taking longer than 500 ms or encountering errors.
- If stored numbers are fewer than the window size, calculate their average. 
- Limit stored numbers to the window size. 
- Upon breaching the window size, replace the oldest number with the newest one.
- Respond to each request with the numbers stored before and after the latest API call, along with the average of numbers matching the window size.

### Solution

This project is an Average Calculator microservice that exposes a REST API endpoint to handle requests for different types of numbers.

### Features

- Fetch numbers from third-party APIs based on the specified type (`p`, `f`, `e`, `r`).
- Store unique numbers while maintaining a sliding window.
- Calculate the average of the numbers within the sliding window.
- Handle and refresh access tokens when they become invalid.
- Ensure response time for each request does not exceed 500 milliseconds.

### Usage

To use the microservice, follow these steps:

1. Clone the repository.
2. Install the required dependencies.
3. Run the Flask application.
4. Make requests to the `/numbers/<numberid>` endpoint with the appropriate number ID (`p`, `f`, `e`, `r`).

### Example Request

```sh
curl -X GET http://localhost:5000/numbers/p
```

### Response 
```
{
  "windowPrevState": [1, 3, 5],
  "windowCurrState": [5, 7, 8, 9, 12, 15],
  "numbers": [8, 9, 12, 15],
  "avg": 11.0
}
```
Like wise you can get correct responses for other methods.
