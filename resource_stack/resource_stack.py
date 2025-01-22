from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    Duration,
    aws_lambda as function_lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3
)
from constructs import Construct


class ResourceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:

        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "GalaxyCodePipelineappQueue",
            visibility_timeout=Duration.seconds(500),
            queue_name="galaxy_queue"
        )



        account_inventory_function = function_lambda.Function(self,
                                            "DemoCDKGITHUBLambda",
                                            function_name="codepipeline_lambda",
                                            runtime=function_lambda.Runtime.PYTHON_3_9,
                                            code=function_lambda.Code.from_asset('./lambda'),
                                            handler="account_inventory.lambda_handler",
                                            timeout=Duration.seconds(5)),
        
        # Define the API Gateway resource
        api = apigateway.LambdaRestApi(
            self,
            "HelloWorldApi",
            handler = account_inventory_function,
            proxy = False,
        )
        
        # Define the '/hello' resource with a GET method
        hello_resource = api.root.add_resource("hello")
        hello_resource.add_method("GET")


        bucket = s3.Bucket(self, "MyfirstBucket", versioned=True,
                           bucket_name="account-inventory-bucket-123456",
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
