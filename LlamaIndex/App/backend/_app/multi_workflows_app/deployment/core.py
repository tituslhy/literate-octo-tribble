from llama_deploy import (
    deploy_core,
    ControlPlaneConfig,
)
from llama_deploy.message_queues.apache_kafka import KafkaMessageQueueConfig

control_plane_config = ControlPlaneConfig()
message_queue_config = KafkaMessageQueueConfig()

if __name__ == "__main__":
    import asyncio

    asyncio.run(
        deploy_core(
            control_plane_config=control_plane_config,
            message_queue_config=message_queue_config,
        )
    )