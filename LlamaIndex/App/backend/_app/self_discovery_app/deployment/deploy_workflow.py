from llama_deploy import deploy_workflow, WorkflowServiceConfig
from self_discovery_app.deployment.core import control_plane_config
from self_discovery_app.workflows.selfdiscovery import SelfDiscoverWorkflow

if __name__ == "__main__":
    import asyncio
    
    asyncio.run(
        deploy_workflow(
            workflow=SelfDiscoverWorkflow(timeout=3600, verbose = True),
            workflow_config=WorkflowServiceConfig(
                service_name="self_discovery_workflow"
            ),
            control_plane_config=control_plane_config,
        )
    )