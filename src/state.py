from typing import Any, Literal
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

class ToolHint(BaseModel):
    name:Literal["shell_tool", "read_document_tool", "write_document_tool", "modify_document_tool", "return_final_output_tool"] | None = None
    parameters:dict|None = None

class Task(BaseModel):
    id: str = ""
    description: str = ""
    tool_hint: list[ToolHint]
    depends_on: list[str] | None = None
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


class FeasibilityCheckerDimensionScores(BaseModel):
    goal_alignment:Literal["pass", "warn", "fail"] = "warn"
    precondition_validity:Literal["pass", "warn", "fail"] = "warn"
    step_sequencing:Literal["pass", "warn", "fail"] = "warn"
    resource_feasibility:Literal["pass", "warn", "fail"] = "warn"
    ambiguity:Literal["pass", "warn", "fail"] = "warn"
    error_handling:Literal["pass", "warn", "fail"] = "warn"
    halting:Literal["pass", "warn", "fail"] = "warn"
    observability:Literal["pass", "warn", "fail"] = "warn"

class BlockingIssues(BaseModel):
    dimension:str=""
    step_ref:str=""
    severity:Literal[ "critical", "major", "minor",] = "minor"
    issue:str=""
    remediation:str=""

class PlanFeasibilityCheckerState(BaseModel):
    verdict: Literal[
        "PASS", 
        "REVISE",
        "REJECT"
    ] = "PASS"
    confidence: float = Field(
        # ..., # '...' means that this field is a mandatory field and that without a value given, it will throw an error.
        0.67, # means that 0.0 is given as a default value instead of '...'.
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0"
    )
    dimension_scores: FeasibilityCheckerDimensionScores = Field(default_factory=FeasibilityCheckerDimensionScores)
    blocking_issues: list[BlockingIssues] = Field(default_factory=list)
    replanning_prompt:str=""
    summary:str=""


class SaftyCriticDimensionScores(BaseModel):
    irreversibility:Literal["pass", "warn", "fail"] = "warn"
    data_sensitivity:Literal["pass", "warn", "fail"] = "warn"
    authorization_scope:Literal["pass", "warn", "fail"] = "warn"
    external_world_effects:Literal["pass", "warn", "fail"] = "warn"
    safety_policy_compliance:Literal["pass", "warn", "fail"] = "warn"
    adversarial_surface:Literal["pass", "warn", "fail"] = "warn"
    human_oversight:Literal["pass", "warn", "fail"] = "warn"
    dual_use:Literal["pass", "warn", "fail"] = "warn"

class Findings(BaseModel):
    dimension:str=""
    step_ref:str=""
    severity:Literal[ "critical", "major", "minor",] = "minor"
    finding:str=""
    constraint:str=""

class ConstraintsToInject(BaseModel):
    after_step_id: str|None = ""
    constraint_type:Literal["dry_run", "human_checkpoint", "scope_restriction", "rate_limit", "data_masking", "confirmation_prompt", "other"] = "rate_limit"
    description:str = ""

class PlanSaftyCriticState(BaseModel):
    verdict:Literal["APPROVED", "CONSTRAIN", "VETO", "ESCALATE"]="CONSTRAIN"
    risk_level:Literal["low", "medium", "high", "critical"]="low"
    confidence: float = Field(
        # ..., # '...' means that this field is a mandatory field and that without a value given, it will throw an error.
        0.0, # means that 0.0 is given as a default value instead of '...'.
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0"
    )
    dimension_scores: SaftyCriticDimensionScores = Field(default_factory=SaftyCriticDimensionScores)
    findings: list[Findings] = Field(default_factory=list)
    constraints_to_inject: list[ConstraintsToInject] = Field(default_factory=list)
    escalation_reason:str = ""
    veto_reason:str = ""
    replanning_prompt:str = ""
    summary:str = ""


class PlanReviewerConfidences(BaseModel):
    plan_feasibility_checker_confidence:float = 0.0
    plan_feasibility_blocking_issues:list[BlockingIssues] = Field(default_factory=list)
    plan_safty_critic_state_confidence:float = 0.0
    plan_safty_findings:list[Findings] = Field(default_factory=list)

class PlanReviewerState(BaseModel):
    plan_review: list[PlanReviewerConfidences] = Field(default_factory=list)
    human_approval_required:bool = False
    approval: bool=False
    review_count:int=0


class ExecutionTask(BaseModel):
    id: str = ""
    description:str = ""
    status: Literal[
        "pending",
        "running",
        "done",
        "failed"
    ] = "pending"
    depends_on:list[str] = []
    tool_hint: list[ToolHint]
    expected_output: str = ""
    result: Any = None
    error: str | None = None
    retry_count:int = 0
    feedback:str = ""

class ExecutorState(BaseModel):
    tasks: list[ExecutionTask] = Field(default_factory=list)
    current_task:ExecutionTask | None = None


class AgentState(BaseModel):
    input: InputState = Field(default_factory=InputState)
    planner: PlannerState = Field(default_factory=PlannerState)
    plan_reviewer: PlanReviewerState = Field(default_factory=PlanReviewerState)
    plan_feasibility_checker: PlanFeasibilityCheckerState = Field(default_factory=PlanFeasibilityCheckerState)
    plan_safty_critic:PlanSaftyCriticState = Field(default_factory=PlanSaftyCriticState)
    executor: ExecutorState = Field(default_factory=ExecutorState)
    final_output:str=""
    # approval:str = ""