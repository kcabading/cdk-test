import aws_cdk as core
import aws_cdk.assertions as assertions

from galaxy_cdk2.galaxy_cdk2_stack import GalaxyCdk2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in galaxy_cdk2/galaxy_cdk2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GalaxyCdk2Stack(app, "galaxy-cdk2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
