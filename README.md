# Serverless URL Shortener

A URL shortener built entirely on serverless AWS infrastructure. Send it a long URL, get back a short code. Visit the short code, get redirected to the original URL. No servers to manage, no containers, just Lambda, API Gateway, and DynamoDB working together.

## What it does

- Accepts a POST request with a URL and returns a short code
- Accepts a GET request with a short code and redirects to the original URL
- Stores the mapping between short codes and URLs in DynamoDB
- Runs entirely on Lambda, so there's no server sitting idle when nobody's using it

## Why I built it this way

DynamoDB fits this project better than a traditional database like PostgreSQL. The lookups here are simple: one key, one value. DynamoDB handles that pattern fast and only charges for what you actually use, so an idle project costs almost nothing.

API Gateway's HTTP API type, rather than the older REST API type, keeps the setup simpler and cheaper for a project this size.

The Lambda function checks the AWS_PROXY integration format from API Gateway, so the entire request and response handling happens inside the function itself, rather than being split across multiple AWS resources.

## How to run this

1. Install Terraform and the AWS CLI
2. Run `aws configure` and add your credentials
3. Zip the Lambda function with `zip lambda_function.zip lambda_function.py`
4. Run `terraform init`
5. Run `terraform plan` to see what will be created
6. Run `terraform apply` and type yes to confirm

Terraform prints your API's public URL once it finishes. Send a POST request to `<url>/shorten` with a JSON body like `{"url": "https://example.com"}` to get a short code. Visit `<url>/<short_code>` in your browser to test the redirect.

## Notes

I tested each layer separately before connecting them. The Lambda function first, invoked directly through the AWS CLI. Then DynamoDB, checking the item saved correctly. Then API Gateway, once I confirmed the function itself worked as expected.
