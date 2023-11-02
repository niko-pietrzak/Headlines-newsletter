## ROLES
# 1. Creating assuming role policy (Trust relationship)
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# 2. Creating IAM Role for lambda with assuming role policy
resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# 3. Defining json policies for lambda
data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]

    resources = ["arn:aws:logs:*:*:*"]
  }
}

data "aws_iam_policy_document" "lambda_s3_write" {
  statement {
    effect = "Allow"

    actions = [
          "s3:PutStorageLensConfiguration",
          "s3:CreateJob",
          "s3:PutObject"
    ]

    resources = ["*"]
  }
}

# 4. Assigning policy definitions to policy names
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_policy" "lambda_s3_write" {
  name        = "lambda_s3_write"
  path        = "/"
  description = "IAM policy for S3 write access for a lambda"
  policy      = data.aws_iam_policy_document.lambda_s3_write.json
}

# 5. Assigning policies to roles
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_iam_role_policy_attachment" "lambda_s3_writes" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_s3_write.arn
}