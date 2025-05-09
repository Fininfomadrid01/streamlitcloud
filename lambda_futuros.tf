provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "api-futuros-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_dynamodb_policy" {
  name = "lambda-dynamodb-read-policy"
  role = aws_iam_role.lambda_exec_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:Scan",
          "dynamodb:GetItem"
        ]
        Resource = "arn:aws:dynamodb:us-east-1:797161732660:table/futuros-table"
      }
    ]
  })
}

resource "aws_lambda_function" "api_futuros_lambda" {
  function_name = "api-futuros-lambda"
  filename      = "iv_smile_project/lambda/api_futuros_handler.zip"
  handler       = "api_futuros_handler.lambda_handler"
  runtime       = "python3.9"
  role          = aws_iam_role.lambda_exec_role.arn

  environment {
    variables = {
      RAW_TABLE_NAME = "futuros-table"
    }
  }
} 