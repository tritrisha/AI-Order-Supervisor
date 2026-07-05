from temporalio import activity
from activity.activity_ai import summarize, generate_ai_response

from services.memory_service import (
    save_message,
    get_messages,
    save_summary,
)

@activity.defn
async def save_message_activity(run_id: str, role: str, content: str):
    print("Saving message:", role, content)
    save_message(run_id, role, content)


@activity.defn
async def get_messages_activity(run_id: str):
    return get_messages(run_id)


@activity.defn
async def save_summary_activity(run_id: str, summary: str):
    save_summary(run_id, summary)


@activity.defn
async def call_ai_activity(messages):
    return generate_ai_response(messages)

@activity.defn
async def summarize_activity(messages):
    return summarize(messages)