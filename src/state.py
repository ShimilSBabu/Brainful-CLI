from typing import TypedDict, Any, Literal
from pydantic import Field, BaseModel

# class Task(BaseModel):
#     id: str = Field(..., description="Unique identifier, e.g. 't1'")
#     description: str = Field(..., min_length=10)
#     tool_hint: Literal["execute_shell_command"] | None
#     depends_on: list[str] = Field(default_factory=list)
#     expected_output: str = Field(..., min_length=5)
#     status: Literal["pending","running","done","failed"] = "pending"
#     result: Any = None
#     error: str | None = None

class Task(BaseModel):
    id: str = ""
    description: str = ""
    tool_hint: Literal["execute_shell_command"] | None = None
    depends_on: list[str] = Field(default_factory=list)
    expected_output: str = ""
    status: Literal["pending", "running", "done", "failed"] = "pending"
    result: Any = None
    error: str | None = None

class InputState(BaseModel):
    user_query: str = ""

# class PlannerState(BaseModel):
#     tasks: list[Task] = Field(..., min_length=1)
#     goal_summary: str = Field(..., description="One-sentence restatement of the goal")
#     estimated_steps: int = Field(..., ge=1)

class PlannerState(BaseModel):
    tasks: list[Task] = Field(default_factory=list)
    goal_summary: str = ""
    estimated_steps: int = 0
# class PlanNormalizerState(BaseModel):
#     normalized_plan: dict[
#         str, list[str]
#     ]

class PlanReviewerState(BaseModel):
    review: str=""
    approval: bool=0

class ExecutionStep(BaseModel):
    status: Literal[
        "pending",
        "running",
        "done",
        "failed"
    ] = "pending"

    result: Any = None
    error: str | None = None


class ExecutorState(BaseModel):

    tasks: dict[
        str,
        ExecutionStep
    ] = Field(default_factory=dict)

    current_task: str | None = None


class AgentState(BaseModel):
    input: InputState = Field(default_factory=InputState)
    planner: PlannerState = Field(default_factory=PlannerState)
    plan_reviewer: PlanReviewerState = Field(default_factory=PlanReviewerState)
    executor: ExecutorState = Field(default_factory=ExecutorState)