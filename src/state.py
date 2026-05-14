from typing import TypedDict

class InputState(TypedDict):
    user_query: str

class PlannerState(TypedDict):
    plan: dict[str, str]

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