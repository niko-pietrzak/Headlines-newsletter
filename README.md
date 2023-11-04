# Terraform_aws_project

My Second AWS Project.

I prepared a tool that is collecing daily data about most important headlines in US and UK.
Data is collected by topics, countires, data sources and then stored on S3.
Every Sunday the data from last week is filtered based on selected words / topics and then send to end-user.
Whole infrustructure is written in Terraform with proper use of modules, variables and outputs.

Tools: 
- AWS (S3, Lambda, EventBridge, SES)
- IaC (Terraform)
- Python (boto3, pandas, requests)
- News API (https://newsapi.org/)
