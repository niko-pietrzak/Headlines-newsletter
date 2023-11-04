output "lambda_role_arn" {
    value = aws_iam_role.iam_for_lambda.arn
}

output "lambda_news_role_arn" {
    value = aws_iam_role.iam_for_news_lambda.arn
}