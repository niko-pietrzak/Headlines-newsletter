resource "aws_ses_email_identity" "sender" {
  email = "nikodem4799@gmail.com"
}

resource "aws_ses_email_identity" "receiver" {
  email = "niko.j.pietrzak@gmail.com"
}