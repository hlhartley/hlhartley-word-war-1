1) To fix issue with using psycopg2 in lambda:
  * https://github.com/jkehler/awslambda-psycopg2

2) Connecting Lambda to RDS
  * Don't forget to set lambdas to use VPC that RDS is using
  * Also need to have IAM role for Lambda to be able to use LambdaVPC

3) CORS issues with Lambda functions
  * Make sure to enable CORS within each API Gateway Method
  * Also, your lambda functions must return appropriate headers. Ex:

  ```
  return {
      'statusCode': 200,
      'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
      'body': json.dumps(body),
  }
  ```

4) Using Lambda to communicate to RDS (within VPC) and also send messages to Websocket clients:

* Current issue is for a lambda function to connect to RDS, we need to connect to VPC with its own subnets
* To send messages to clients though we need to make a POST to the public internet
* So need to configure Lambda to connect to both VPC and public internet:
  https://gist.github.com/reggi/dc5f2620b7b4f515e68e46255ac042a7