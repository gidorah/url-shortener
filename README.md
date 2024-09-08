# url-shortener

A simple RESTful API that allows users to shorten long URLs.  

This project build as one of roadmap.sh Backend Projects: https://roadmap.sh/projects/url-shortening-service

The API allows users to perform the following operations:
- Create a new short URL
- Retrieve an original URL from a short URL
- Update an existing short URL
- Delete an existing short URL
- Get statistics on the short URL (e.g., number of times accessed)

## Tech Stack

Used Flask as web framework and MongoDB as DB.

## API Endpoints

### Create Short URL
Create a new short URL using the POST method

    POST /shorten
    {
        "url": "https://www.example.com/some/long/url"
    }

Returns newly created short URL

    {
        "id": "1",
        "url": "https://www.example.com/some/long/url",
        "shortCode": "abc123",
        "createdAt": "2021-09-01T12:00:00Z",
        "updatedAt": "2021-09-01T12:00:00Z"
    }

### Retrieve Original URL

Retrieve the original URL from a short URL using the GET method

    GET /shorten/abc123

Returns short URL

    {
        "id": "1",
        "url": "https://www.example.com/some/long/url",
        "shortCode": "abc123",
        "createdAt": "2021-09-01T12:00:00Z",
        "updatedAt": "2021-09-01T12:00:00Z"
    }

### Update Short URL

Update an existing short URL using the PUT method

    PUT /shorten/abc123
    {
        "url": "https://www.example.com/some/updated/url"
    }

Returns updated short URL
    
    {
        "id": "1",
        "url": "https://www.example.com/some/updated/url",
        "shortCode": "abc123",
        "createdAt": "2021-09-01T12:00:00Z",
        "updatedAt": "2021-09-01T12:30:00Z"
    }

### Delete Short URL

Delete an existing short URL using the DELETE method

    DELETE /shorten/abc123

### Get URL Statistics

Get statistics for a short URL using the GET method

    GET /shorten/abc123/stats

The endpoint returns statistics

    {
        "id": "1",
        "url": "https://www.example.com/some/long/url",
        "shortCode": "abc123",
        "createdAt": "2021-09-01T12:00:00Z",
        "updatedAt": "2021-09-01T12:00:00Z",
        "accessCount": 10
    }