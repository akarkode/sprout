from typing import TypedDict
from langgraph.graph import StateGraph, END

from app.src.agents.cv_parser import AICVParser
from app.src.agents.skill_analyst import SkillAnalystAgent
from app.src.agents.market_intel import MarketIntelligenceAgent
from app.src.agents.report import ReportAgent


class PipelineState(TypedDict):
    cv_text: str
    parsed_cv: dict
    skill_analysis: dict
    market_analysis: dict
    report: dict
    role: str


graph = StateGraph(PipelineState)


def parse_cv(state: PipelineState) -> PipelineState:
    parsed = AICVParser().parse(state["cv_text"])
    state["parsed_cv"] = parsed.model_dump()
    return state


def analyze_skills(state: PipelineState) -> PipelineState:
    analyzed = SkillAnalystAgent().analyze(state["parsed_cv"])
    state["skill_analysis"] = analyzed.model_dump()
    return state


def market_intel(state: PipelineState) -> PipelineState:
    intel = MarketIntelligenceAgent().analyze(state["role"])
    state["market_analysis"] = intel.model_dump()
    return state


def generate_report(state: PipelineState) -> PipelineState:
    report = ReportAgent().generate_report(
        candidate_info=state["parsed_cv"],
        skill_analysis=state["skill_analysis"],
        market_analysis=state["market_analysis"],
    )
    state["report"] = report.model_dump()
    return state


# Register nodes
graph.add_node("parse_cv", parse_cv)
graph.add_node("analyze_skills", analyze_skills)
graph.add_node("market_intel", market_intel)
graph.add_node("generate_report", generate_report)

# Define edges
graph.add_edge("parse_cv", "analyze_skills")
graph.add_edge("analyze_skills", "market_intel")
graph.add_edge("market_intel", "generate_report")
graph.add_edge("generate_report", END)

# Set entry point
graph.set_entry_point("parse_cv")

# Compile
pipeline = graph.compile()