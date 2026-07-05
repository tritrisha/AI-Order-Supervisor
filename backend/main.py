from fastapi import FastAPI, HTTPException
from temporalio.client import Client
import uuid
from pydantic import BaseModel
from services.memory_service import get_messages
from workflows import AgentWorkflow
from services.memory_service import (
    create_run,
    get_messages,
    get_summary,
    get_all_runs,
)
from temporalio.client import Client
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = None


@app.on_event("startup")
async def startup():
    global client
    client = await Client.connect("localhost:7233")


class RunRequest(BaseModel):
    order_id: str


@app.post("/runs")
async def create_new_run(body: RunRequest):

    run_id = str(uuid.uuid4())

    create_run(run_id)

    await client.start_workflow(
        AgentWorkflow.run,
        run_id,          
        id=run_id,
        task_queue="ai-task-queue",
    )

    return {
        "run_id": run_id,
        "order_id": body.order_id,
        "status": "RUNNING",
    }


@app.get("/runs")
async def list_runs():
    return get_all_runs()

class EventRequest(BaseModel):
    event: str



@app.post("/runs/{run_id}/events")
async def send_event(run_id: str, body: EventRequest):
    try:
        handle = client.get_workflow_handle(run_id)

        await handle.signal(
            AgentWorkflow.user_event,
            body.event,
        )

        return {
            "message": "Event received",
            "run_id": run_id,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/runs/{run_id}")
async def get_run(run_id: str):
    try:
        handle = client.get_workflow_handle(run_id)
        desc = await handle.describe()

        messages = get_messages(run_id)
        summary = get_summary(run_id)

        return {
            "run_id": run_id,
            "status": desc.status.name,
            "memory": summary,
            "timeline": messages,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/runs/{run_id}/events")
async def get_events(run_id: str):

    messages = get_messages(run_id)

    return {
        "run_id": run_id,
        "events": messages
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)