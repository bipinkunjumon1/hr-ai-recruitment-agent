from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import RecruitmentState

from graph.nodes import (
    process_jd_node,
    process_resumes_node,
    ranking_node,
    finalize_node
)


def build_graph():

    workflow = StateGraph(
        RecruitmentState
    )

    workflow.add_node(
        "process_jd",
        process_jd_node
    )

    workflow.add_node(
        "process_resumes",
        process_resumes_node
    )

    workflow.add_node(
        "ranking",
        ranking_node
    )

    workflow.add_node(
        "finalize",
        finalize_node
    )




    workflow.set_entry_point(
        "process_jd"
    )

    workflow.add_edge(
        "process_jd",
        "process_resumes"
    )

    workflow.add_edge(
        "process_resumes",
        "ranking"
    )

    workflow.add_edge(
        "ranking",
        "finalize"
    )

    workflow.add_edge(
        "finalize",
        END
    )

    return workflow.compile()