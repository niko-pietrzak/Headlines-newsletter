output "lambda_arn" {
    value = aws_lambda_function.get_data_lambda.arn
}

output "lambda_news_arn" {
    value = aws_lambda_function.send_news_lambda.arn
}