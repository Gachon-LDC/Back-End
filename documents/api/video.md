# 📁 Collection: video

## End-point: get Videos

### Method: GET

> ```
> {{url}}/api/videos
> ```

### Response: 200

```json
[
    {
        "video_id": "c471a9e2-0e7f-426b-b858-1c9554931b02",
        "uploader_id": "87edc546-fc7c-48d6-ab90-9287d647b1b3",
        "title": "'title'",
        "content": "\"1\"",
        "dance": "5398d5cb-4dbd-4353-a3fe-99daf4fae5c4"
    },
    {
        "video_id": "5907b142-16de-42d3-b7cd-c7ac06e16c28",
        "uploader_id": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
        "title": "'title'",
        "content": "\"1\"",
        "dance": "5398d5cb-4dbd-4353-a3fe-99daf4fae5c4"
    }
]
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: new Video

### Method: POST

> ```
> {{url}}/api/videos
> ```

### Body formdata

| Param   | value                           | Type |
| ------- | ------------------------------- | ---- |
| fps     | 10                              | text |
| file    | /E:/80.grade/model test/out.mp4 | file |
| content | "1"                             | text |
| title   | 'title'                         | text |
| dance   | {{category_id}}                 | text |

### Response: 200

```json
{
    "video_id": "5907b142-16de-42d3-b7cd-c7ac06e16c28",
    "uploader_id": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
    "dance": "9a19d9bb-dd9d-4e07-a731-a6a16f1c13a1",
    "title": "'title'",
    "content": "\"1\""
}
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: get Video by Id

### Method: GET

> ```
> {{url}}/api/videos/{{video_id}}
> ```

### Query Params

| Param   | value |
| ------- | ----- |
| comment | false |

### Response: 200

```json
{
    "video_id": "c471a9e2-0e7f-426b-b858-1c9554931b02",
    "uploader_id": "87edc546-fc7c-48d6-ab90-9287d647b1b3",
    "title": "'title'",
    "content": "\"1\"",
    "dance": "5398d5cb-4dbd-4353-a3fe-99daf4fae5c4",
    "comments": [
        {
            "uid": "d6323a8b-15ad-4c16-a828-dad774d7b72c",
            "videoId": "c471a9e2-0e7f-426b-b858-1c9554931b02",
            "writerId": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
            "content": "1234"
        }
    ]
}
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Delete video

### Method: DELETE

> ```
> {{url}}/api/videos/{{video_id}}
> ```

### Response: 401

```json
Unauthorized
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: learn video

### Method: POST

> ```
> {{url}}/api/videos/{{video_id}}/learn
> ```

### Body formdata

| Param  | value                       | Type |
| ------ | --------------------------- | ---- |
| image  | /D:/insir/Desktop/image.png | file |
| nframe | 1                           | text |

### Response: 200

```json
{
    "simirarity": 0.9875914970370748
}
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: add comment

### Method: POST

> ```
> {{url}}/api/videos/{{video_id}}/comment
> ```

### Body (**raw**)

```json
{
    "content": "1234"
}
```

### Response: 201

```json
{
    "uid": "f2fc69c4-9b6c-426b-91db-e7131f447fa3",
    "videoId": "c471a9e2-0e7f-426b-b858-1c9554931b02",
    "writerId": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
    "content": "1234"
}
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: get_comments

### Method: GET

> ```
> {{url}}/api/videos/{{video_id}}/comment
> ```

### Body (**raw**)

```json
{
    "videoId": "46ab087d-0200-4111-a28c-1c36095b3faa"
}
```

### Response: 201

```json
[
    {
        "uid": "d6323a8b-15ad-4c16-a828-dad774d7b72c",
        "videoId": "c471a9e2-0e7f-426b-b858-1c9554931b02",
        "writerId": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
        "content": "1234"
    },
    {
        "uid": "8627538f-7770-4bf9-b0ec-26b80da6d56a",
        "videoId": "c471a9e2-0e7f-426b-b858-1c9554931b02",
        "writerId": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
        "content": "1234"
    }
]
```

## ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃
