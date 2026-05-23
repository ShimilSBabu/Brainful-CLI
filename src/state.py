from typing import TypedDict, Any, Literal
from pydantic import Field

class Task(TypedDict):
    id: str = Field(..., description="Unique identifier, e.g. 't1'")
    description: str = Field(..., min_length=10)
    tool_hint: Literal["execute_shell_command"] | None
    depends_on: list[str] = Field(default_factory=list)
    expected_output: str = Field(..., min_length=5)
    status: Literal["pending","running","done","failed"] = "pending"
    result: Any = None
    error: str | None = None

class InputState(TypedDict):
    user_query: str

class PlannerState(TypedDict):
    tasks: list[Task] = Field(..., min_length=1)
    goal_summary: str = Field(..., description="One-sentence restatement of the goal")
    estimated_steps: int = Field(..., ge=1)

class PlanNormalizerState(TypedDict):
    normalized_plan: dict[
        str, list[str]
    ]

class PlanReviewerState(TypedDict):
    review: str
    approval: bool

class ExecutorState(TypedDict):
    step: dict[
        str, dict[
            bool, str
            ]
    ]


class AgentState(TypedDict):
    input: InputState
    planner: PlannerState
    plan_normalizer: PlanNormalizerState
    plan_reviewer: PlanReviewerState
    executor: ExecutorState