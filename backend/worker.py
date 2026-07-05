import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import AgentWorkflow
from activity.activities import (
    save_message_activity,
    get_messages_activity,
    call_ai_activity,
    save_summary_activity,
    summarize_activity
)


TASK_QUEUE = "ai-task-queue"

async def main():
    client = await Client.connect("localhost:7233")

    worker = Worker(
    client,
    task_queue="ai-task-queue",
    workflows=[AgentWorkflow],
    activities=[
        save_message_activity,
        get_messages_activity,
        call_ai_activity,
        save_summary_activity,
        summarize_activity,   
        ],
    )
    print("🚀 Worker started... listening on ai-task-queue")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())