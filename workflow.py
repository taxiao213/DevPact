from typing import TypedDict
from langgraph.graph import StateGraph, END

from state import DevelopmentState, ProjectConfig
from agents import SupervisorAgent, FrontendAgent, BackendAgent
from discussion import DiscussionManager
from code_reader import CodeReader


class GraphState(TypedDict):
    state: DevelopmentState


def create_workflow():
    supervisor = SupervisorAgent()
    frontend = FrontendAgent()
    backend = BackendAgent()
    discussion_manager = DiscussionManager()
    code_reader = CodeReader()

    def read_project_code(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        if state.project_config.frontend_path or state.project_config.backend_path:
            print("\n[CodeReader] 正在读取项目代码...")
            state = code_reader.read_project(state)
            print(f"[CodeReader] 前端文件: {len(state.code_context.frontend_files)} 个")
            print(f"[CodeReader] 后端文件: {len(state.code_context.backend_files)} 个")
            print(f"[CodeReader] 现有接口: {len(state.code_context.existing_apis)} 个")
        return {"state": state}

    def supervisor_analyze(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = supervisor.analyze_requirement(state)
        return {"state": state}

    def frontend_breakdown(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = frontend.breakdown_tasks(state)
        return {"state": state}

    def backend_breakdown(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = backend.breakdown_tasks(state)
        return {"state": state}

    def create_proposals(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = discussion_manager.create_proposals(state)
        return {"state": state}

    def frontend_discuss(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = frontend.discuss(state)
        return {"state": state}

    def backend_discuss(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = backend.discuss(state)
        return {"state": state}

    def process_agreements(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = discussion_manager.process_agreements(state)
        state.current_round += 1
        return {"state": state}

    def check_consensus(state_dict: GraphState) -> str:
        state = state_dict["state"]
        if len(state.agreed_schemas) == len(state.schema_proposals) and len(state.schema_proposals) > 0:
            return "consensus"
        if state.current_round >= state.max_rounds:
            return "max_rounds"
        return "continue"

    def generate_contract(state_dict: GraphState) -> GraphState:
        state = state_dict["state"]
        state = supervisor.generate_contract(state)
        return {"state": state}

    workflow = StateGraph(GraphState)

    workflow.add_node("read_project_code", read_project_code)
    workflow.add_node("supervisor_analyze", supervisor_analyze)
    workflow.add_node("frontend_breakdown", frontend_breakdown)
    workflow.add_node("backend_breakdown", backend_breakdown)
    workflow.add_node("create_proposals", create_proposals)
    workflow.add_node("frontend_discuss", frontend_discuss)
    workflow.add_node("backend_discuss", backend_discuss)
    workflow.add_node("process_agreements", process_agreements)
    workflow.add_node("generate_contract", generate_contract)

    workflow.set_entry_point("read_project_code")

    workflow.add_edge("read_project_code", "supervisor_analyze")
    workflow.add_edge("supervisor_analyze", "frontend_breakdown")
    workflow.add_edge("frontend_breakdown", "backend_breakdown")
    workflow.add_edge("backend_breakdown", "create_proposals")
    workflow.add_edge("create_proposals", "frontend_discuss")
    workflow.add_edge("frontend_discuss", "backend_discuss")
    workflow.add_edge("backend_discuss", "process_agreements")

    workflow.add_conditional_edges(
        "process_agreements",
        check_consensus,
        {
            "consensus": "generate_contract",
            "max_rounds": "generate_contract",
            "continue": "frontend_discuss",
        },
    )

    workflow.add_edge("generate_contract", END)

    return workflow.compile()


def run_collaboration(
    requirement: str,
    frontend_path: str = "",
    backend_path: str = "",
    max_rounds: int = 3,
) -> DevelopmentState:
    project_config = ProjectConfig(
        frontend_path=frontend_path,
        backend_path=backend_path,
    )

    initial_state = DevelopmentState(
        requirement=requirement,
        project_config=project_config,
        max_rounds=max_rounds,
    )

    graph = create_workflow()
    result = graph.invoke({"state": initial_state})

    return result["state"]
