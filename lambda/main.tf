## LAMBDA
data "archive_file" "lambda" {
  type        = "zip"
  source_file = "lambda_function.py"
  output_path = "lambda_function_payload.zip"
}

resource "aws_lambda_function" "get_data_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  filename      = "lambda_function_payload.zip"
  function_name = "lambda_by_terraform"
  role          = var.lambda_role_arn
  handler       = "lambda_function.lambda_handler"

  source_code_hash = data.archive_file.lambda.output_base64sha256

  runtime = "python3.9"
  timeout = "30"

  layers = ["arn:aws:lambda:eu-central-1:336392948345:layer:AWSSDKPandas-Python39:6", "arn:aws:lambda:eu-central-1:597570747370:layer:newsapi-boto3-libraries:1"]

  environment {
    variables = {
      api_key = var.api_key
    }
  }
}

## EventBridge (CloudWatch) Event to trigger lambda every day
resource "aws_cloudwatch_event_rule" "daily_lambda_trigger" {
  name                = "DailyLambdaTrigger"
  schedule_expression = "cron(0 12 * * ? *)"
}

resource "aws_cloudwatch_event_target" "terraform_lambda_every_day" {
    rule = aws_cloudwatch_event_rule.daily_lambda_trigger.name
    target_id = "get_data_lambda"
    arn = aws_lambda_function.get_data_lambda.arn
}

resource "aws_lambda_permission" "allow_event_to_trigger_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_data_lambda.arn
  principal     = "events.amazonaws.com"

  source_arn = aws_cloudwatch_event_rule.daily_lambda_trigger.arn
}