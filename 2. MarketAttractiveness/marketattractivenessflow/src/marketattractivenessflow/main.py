#!/usr/bin/env python
# ===============================================
# Import libraries
# ===============================================
import pandas as pd
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, and_
from src.marketattractivenessflow.crews.research_planner_crew.research_planner_crew import ResearchPlannerCrew
from src.marketattractivenessflow.crews.demand_analysis_crew_2_1.demand_analysis_crew_2_1 import DemandAnalysisCrew21
from src.marketattractivenessflow.crews.barriers_to_entry_crew_2_2.barriers_to_entry_crew_2_2 import BarriersToEntryCrew22
from src.marketattractivenessflow.crews.competence_level_crew_2_3.competence_level_crew_2_3 import CompetenceLevelCrew23
from src.marketattractivenessflow.crews.scalability_crew_2_4.scalability_crew_2_4 import ScalabilityCrew24
from src.marketattractivenessflow.crews.final_report_crew.final_report_crew import FinalReportCrew
# Must precede any llm module imports
import os
from dotenv import load_dotenv
import agentops

# Загружаем переменные окружения
load_dotenv()

# Инициализируем AgentOps
agentops.init(api_key=os.getenv('AGENTOPS_API_KEY'))

# ===============================================
# Define state
# ===============================================

class ReportSection(BaseModel):
    title: str
    content: str
    char_count: int

class DemandAnalysisSection(ReportSection):
    title: str = "2.1 Анализ спроса на товары или услуги"

class BarriersToEntrySection(ReportSection):
    title: str = "2.2 Существующие барьеры для входа"

class CompetenceLevelSection(ReportSection):
    title: str = "2.3 Уровень компетенции"

class ScalabilitySection(ReportSection):
    title: str = "2.4 Масштабируемость ваших товаров или услуг"


class ResearchPlannerState(BaseModel):
    raw_idea: str = ""
    structured_idea: str = ""
    demand_analysis: str = ""
    barriers_to_entry: str = ""
    competence_level: str = ""
    scalability: str = ""
    final_report: list[str] = []
# ===============================================
# Define flow
# ===============================================
class ResearchPlannerFlow(Flow[ResearchPlannerState]):

# ============== Start Task ==============
    @start()
    def import_raw_idea(self):
        """Import the raw idea from markdown file"""
        print("========== Import the raw idea ==========")
        try:
            with open("../NewIdea.md", "r", encoding="utf-8") as file:
                self.state.raw_idea = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                "NewIdea.md file not found. Please create a file '../NewIdea.md' with your idea description."
            )
        except Exception as e:
            raise Exception(f"Error reading NewIdea.md: {str(e)}")

# ============== Research Plan Task ==============
    @listen(import_raw_idea)
    def idea_structuring_task(self):
        print("========== Structuring the idea ==========")
        result = (
            ResearchPlannerCrew()
            .crew()
            .kickoff(inputs={"raw_idea": self.state.raw_idea})
        )
        print("Structured idea generated", result.raw)
        self.state.structured_idea = result.raw

# ============== Demand Analysis Task ==============
    @listen(idea_structuring_task)
    def demand_analysis_task(self):
        print("========== Demand analysis task ==========")
        result = (
            DemandAnalysisCrew21()
            .crew()
            .kickoff(inputs={"structured_idea": self.state.structured_idea})
        )
        print("Demand analysis task completed", result.raw)
        self.state.demand_analysis = result.raw

# ============== Barriers to Entry Task ==============
    @listen(demand_analysis_task)
    def barriers_to_entry_task(self):
        print("========== Barriers to entry task ==========")
        result = (
            BarriersToEntryCrew22()
            .crew()
            .kickoff(inputs={
                "startup_description": self.state.structured_idea, 
                "demand_research_insights": self.state.demand_analysis
                })
        )
        print("Barriers to entry task completed", result.raw)
        self.state.barriers_to_entry = result.raw

# ============== Competence Level Task ==============
    @listen(barriers_to_entry_task)
    def competence_level_task(self):
        print("========== Competence level task ==========")
        result = (
            CompetenceLevelCrew23()
            .crew()
            .kickoff(inputs={
                "startup_description": self.state.structured_idea,
                "demand_research_insights": self.state.demand_analysis,
                })
        )
        print("Competence level task completed", result.raw)
        self.state.competence_level = result.raw

# ============== Scalability Task ==============
    @listen(and_(demand_analysis_task, barriers_to_entry_task, competence_level_task))
    def scalability_task(self):
        print("========== Scalability task ==========")
        result = (
            ScalabilityCrew24()
            .crew()
            .kickoff(inputs={
                "startup_description": self.state.structured_idea,
                "demand_research_insights": self.state.demand_analysis,
                "barriers_research_insights": self.state.barriers_to_entry,
                "competence_level_research_insights": self.state.competence_level,
                })
        )
        print("Scalability task completed", result.raw)
        self.state.scalability = result.raw

# ============== Final Report Task ==============
    @listen(and_(demand_analysis_task, barriers_to_entry_task, competence_level_task, scalability_task))
    def final_report_task(self):
        print("========== Final report task ==========")
        result = (
            FinalReportCrew()
            .crew()
            .kickoff(inputs={
                "startup_description": self.state.structured_idea,
                "demand_research_insights": self.state.demand_analysis,
                "barriers_research_insights": self.state.barriers_to_entry,
                "competence_level_research_insights": self.state.competence_level,
                "scalability_research_insights": self.state.scalability,
                })
        )
        print("Final report task completed", result.raw)
        self.state.final_report = result.raw

# ===============================================
# Kickoff
# ===============================================
def kickoff():
    research_plan_flow = ResearchPlannerFlow()
    research_plan_flow.kickoff()


def plot():
    research_plan_flow = ResearchPlannerFlow()
    research_plan_flow.plot()


if __name__ == "__main__":
    kickoff()
