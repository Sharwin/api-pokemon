# Pokémon API

A serverless REST API for managing Pokémon data, built with AWS Lambda, API Gateway, and DynamoDB.

## Architecture

- **API Gateway**: REST API with CORS support
- **Lambda Functions**: 4 Python functions (CREATE, READ, UPDATE, DELETE)
- **DynamoDB**: On-demand table with `id` as primary key
- **IAM**: Least-privilege policies (no CloudWatch Logs permissions)

## Prerequisites

- Terraform >= 1.0
- AWS CLI configured with credentials
- Python 3.11+ (for local testing)

## Deployment

```bash
cd terraform
terraform init
terraform apply
```

The deployment creates:
- 1 DynamoDB table (`pokemon`)
- 4 Lambda functions with individual IAM roles
- 1 API Gateway REST API with stage `v1`
- CORS-enabled OPTIONS endpoints

## API Endpoints

Base URL: `https://<api-id>.execute-api.us-east-1.amazonaws.com/v1`

### Create Pokémon
```bash
POST /pokemon
Content-Type: application/json

{
  "id": "001",
  "name": "Bulbasaur",
  "height": 7,
  "weight": 69,
  "types": ["grass", "poison"]
}

Response: 201 Created
```

### Get Pokémon
```bash
GET /pokemon/{id}

Response: 200 OK (or 404 Not Found)
```

### Update Pokémon
```bash
PUT /pokemon/{id}
Content-Type: application/json

{
  "name": "Ivysaur",
  "height": 10
}

Response: 200 OK
```

### Delete Pokémon
```bash
DELETE /pokemon/{id}

Response: 200 OK
```

### CORS Preflight
```bash
OPTIONS /pokemon
OPTIONS /pokemon/{id}

Response: 200 OK with CORS headers
```

## Testing

### Local Unit Tests
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

### Manual API Testing
```bash
# Get API URL
cd terraform
export API_URL=$(terraform output -raw api_url)

# Create
curl -X POST $API_URL/pokemon \
  -H "Content-Type: application/json" \
  -d '{"id":"001","name":"Bulbasaur","height":7,"weight":69,"types":["grass","poison"]}'

# Read
curl -X GET $API_URL/pokemon/001

# Update
curl -X PUT $API_URL/pokemon/001 \
  -H "Content-Type: application/json" \
  -d '{"name":"Ivysaur","height":10}'

# Delete
curl -X DELETE $API_URL/pokemon/001
```

## CORS Configuration

All endpoints support CORS with:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS`
- `Access-Control-Allow-Headers: *`

## IAM Permissions

Each Lambda function has minimal permissions:
- **CREATE**: `dynamodb:PutItem`
- **READ**: `dynamodb:GetItem`
- **UPDATE**: `dynamodb:UpdateItem`
- **DELETE**: `dynamodb:DeleteItem`

**Note**: No CloudWatch Logs permissions are granted.

## PUT Semantics

The PUT endpoint uses DynamoDB's `UpdateItem` operation with `ExpressionAttributeNames` to safely update specific fields without replacing the entire item. Only provided fields are updated; others remain unchanged.

## Error Handling

- `400 Bad Request`: Invalid JSON or missing required fields
- `404 Not Found`: Resource does not exist
- `500 Internal Server Error`: Unexpected errors

All responses include `Content-Type: application/json`.

## Outputs

After deployment, Terraform provides:
- `api_url`: API Gateway invoke URL
- `lambda_*_arn`: ARNs of all Lambda functions
- `dynamodb_table_name`: Table name
- `dynamodb_table_arn`: Table ARN

View outputs:
```bash
terraform output
```

## Teardown

```bash
cd terraform
terraform destroy
```

## Project Structure

```
.
├── lambdas/
│   ├── create_post.py
│   ├── read_get.py
│   ├── update_put.py
│   └── delete_delete.py
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   └── versions.tf
├── tests/
│   ├── test_create.py
│   ├── test_read.py
│   ├── test_update.py
│   └── test_delete.py
├── requirements.txt
└── README.md
```
