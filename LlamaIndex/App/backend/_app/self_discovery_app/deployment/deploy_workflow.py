import os
import sys

from llama_deploy import deploy_workflow, WorkflowServiceConfig

__curdir__ = os.getcwd()
if "deployment" in __curdir__:
    sys.path.append("../workflows")

from core import control_plane_config
from selfdiscovery import SelfDiscoverWorkflow

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