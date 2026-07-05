from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activity.activities import (
        save_message_activity,
        get_messages_activity,
        call_ai_activity,
        save_summary_activity,
        summarize_activity,
    )


@workflow.defn
class AgentWorkflow:

    def __init__(self):
        self.events = []

    @workflow.signal
    async def user_event(self, event: str):
        self.events.append(event)

    @workflow.run
    async def run(self, run_id: str):

        while True:
            print("Waiting for event...")

            await workflow.wait_condition(lambda: len(self.events) > 0)

            user_message = self.events.pop(0)

            print(f"Received Event: {user_message}")

            await workflow.execute_activity(
                save_message_activity,
                args=[run_id, "user", user_message],
                start_to_close_timeout=timedelta(seconds=10),
            )

            messages = await workflow.execute_activity(
                get_messages_activity,
                args=[run_id],
                start_to_close_timeout=timedelta(seconds=10),
            )

            prompt = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI Order Supervisor.\n"
                        "You monitor an order lifecycle.\n"
                        "Summarize the latest order event.\n"
                        "Maintain memory.\n"
                        "Decide if intervention is needed.\n"
                        "Keep responses short."
                    ),
                }
            ]

            prompt.extend(messages)

            response = await workflow.execute_activity(
                call_ai_activity,
                args=[prompt],
                start_to_close_timeout=timedelta(seconds=30),
            )

            await workflow.execute_activity(
                save_message_activity,
                args=[run_id, "assistant", response],
                start_to_close_timeout=timedelta(seconds=10),
            )

            updated_messages = await workflow.execute_activity(
                get_messages_activity,
                args=[run_id],
                start_to_close_timeout=timedelta(seconds=10),
            )

            summary = await workflow.execute_activity(
                summarize_activity,
                args=[updated_messages],
                start_to_close_timeout=timedelta(seconds=20),
            )

            await workflow.execute_activity(
                save_summary_activity,
                args=[run_id, summary],
                start_to_close_timeout=timedelta(seconds=10),
            )

            event = user_message.lower()

            if (
                "order cancelled" in event
                or "shipment delivered" in event
                or "order completed" in event
                or "delivered" in event
                or "cancelled" in event
            ):
                print("Workflow completed.")
                return

            print("Workflow sleeping until next event...")