## EventBridge (CloudWatch) Event to trigger lambda every day
resource "aws_cloudwatch_event_rule" "daily_lambda_trigger" {
  name                = "DailyLambdaTrigger"
  schedule_expression = "cron(0 12 * * ? *)"
}

resource "aws_cloudwatch_event_target" "terraform_lambda_every_day" {
    rule = aws_cloudwatch_event_rule.daily_lambda_trigger.name
    target_id = "get_data_lambda"
    arn = var.lambda_arn
}

resource "aws_lambda_permission" "allow_event_to_trigger_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_arn
  principal     = "events.amazonaws.com"

  source_arn = aws_cloudwatch_event_rule.daily_lambda_trigger.arn
}