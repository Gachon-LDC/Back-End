# 📁 Collection: dance_category

## End-point: get_dance_category

### Method: GET

> ```
> {{url}}/api/category
> ```

### Body (**raw**)

```json

```

### Response: 201

```json
[
    {
        "uid": "5398d5cb-4dbd-4353-a3fe-99daf4fae5c4",
        "title": "댄스카테고리1"
    }
]
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: get_dance_category_byID

### Method: GET

> ```
> {{url}}/api/category/{{category_id}}?video=true
> ```

### Body (**raw**)

```json

```

### Query Params

| Param | value |
| ----- | ----- |
| video | true  |

### Response: 201

```json
{
    "uid": "5398d5cb-4dbd-4353-a3fe-99daf4fae5c4",
    "title": "댄스카테고리1",
    "videos": [
        {
            "video_id": "c471a9e2-0e7f-426b-b858-1c9554931b02",
            "uploader_id": "87edc546-fc7c-48d6-ab90-9287d647b1b3",
            "dance": "c54bc1b5-828b-43b7-8891-08e7e88ce303",
            "title": "'title'",
            "content": "\"1\""
        },
        {
            "video_id": "5907b142-16de-42d3-b7cd-c7ac06e16c28",
            "uploader_id": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
            "dance": "9a19d9bb-dd9d-4e07-a731-a6a16f1c13a1",
            "title": "'title'",
            "content": "\"1\""
        },
        {
            "video_id": "5ab53680-6fc9-4ff8-a1c7-86574048ca4c",
            "uploader_id": "dcda245b-2e73-4fb7-9c51-cc322c09c320",
            "dance": "37b2d821-3b28-4052-9d30-9592e58caab8",
            "title": "'title'",
            "content": "\"1\""
        }
    ]
}
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: add_dance_category

### Method: POST

> ```
> {{url}}/api/category
> ```

### Body (**raw**)

```json
{
    "title": "댄스카테고리1"
}
```

### Response: 201

```json
{
    "uid": "5398d5cb-4dbd-4353-a3fe-99daf4fae5c4",
    "title": "댄스카테고리1"
}
```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃
