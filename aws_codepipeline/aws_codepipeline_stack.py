from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    Stage,
    Environment,
    pipelines,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions
)

from aws_cdk.pipelines import ManualApprovalStep

from constructs import Construct
from resource_stack.resource_stack import ResourceStack


class DeployStage(Stage):
    def __init__(self, scope: Construct, id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)
        ResourceStack(self, 'ResourceStack', env=env, stack_name="resource-stack-deploy")

class AwsCodepipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_input = pipelines.CodePipelineSource.connection(
            repo_string="kcabading/cdk-test",
            branch="main",
            connection_arn="arn:aws:codeconnections:us-east-1:193365704239:connection/fd1664c8-3772-4211-a2e9-8e0ddadffcc2"
        )

        code_pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name="new-pipeline",
            cross_account_keys=False
        )

        synth_step = pipelines.ShellStep(
            id="Synth",
            install_commands=[
                'pip install -r requirements.txt'
            ],
            commands=[
                'npx cdk synth'
            ],
            input=git_input
        )

        pipeline = pipelines.CodePipeline(
            self, 'CodePipeline',
            self_mutation=True,
            code_pipeline=code_pipeline,
            synth=synth_step
        )

        deployment_wave = pipeline.add_wave("DeploymentWave")

        # in dev
        # deployment_wave.add_stage(DeployStage(
        #     self, 'DeployStage',
        #     env=(Environment(account='193365704239', region='us-east-1'))
        # ))

        # in prod
        deployment_wave.add_stage(DeployStage(
            self, 'DeployStage',
            env=(Environment(account='193365704239', region='us-east-1'))
        ),
            pre = [ManualApprovalStep('PromoteToProduction')]
        )
        


        