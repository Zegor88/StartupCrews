#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start
import pandas as pd
from .crews.business_description_crew.business_description_crew import BusinessDescriptionCrew
from .crews.patent_deveopment_crew.patent_deveopment_crew_crew import PatentDeveopmentCrew

class BusinessDescriptionState(BaseModel):
    structured_idea: str = ""
    demand_analysis: str = ""
    barriers_to_entry: str = ""
    competitive_level: str = ""
    scalability: str = ""
    business_model: str = ""
    patent_strategy: str = ""


class BusinessDescriptionFlow(Flow[BusinessDescriptionState]):

    @start()
    def import_research(self):
        print("\n\n=======Load researches=======\n\n")
        try:
            with open("../market_research/Structured_Idea.md", "r", encoding="utf-8") as file:
                self.state.structured_idea = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(    
                "Structured_Idea.md file not found. Please create a file '../market_research/Structured_Idea.md' with your idea description."
            )
        except Exception as e:
            raise Exception(f"Error reading Structured_Idea.md: {str(e)}")
        try:
            with open("../market_research/Demand_Analysis_2_1.md", "r", encoding="utf-8") as file:
                self.state.demand_analysis = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(    
                "Demand_Analysis_2_1.md file not found. Please create a file '../market_research/Demand_Analysis_2_1.md' with your idea description."
            )
        except Exception as e:
            raise Exception(f"Error reading Demand_Analysis_2_1.md: {str(e)}")
        try:
            with open("../market_research/Barriers_to_Entry_2_2.md", "r", encoding="utf-8") as file:
                self.state.barriers_to_entry = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(    
                "Barriers_to_Entry_2_2.md file not found. Please create a file '../market_research/Barriers_to_Entry_2_2.md' with your idea description."
            )
        except Exception as e:
            raise Exception(f"Error reading Barriers_to_Entry_2_2.md: {str(e)}")
        try:
            with open("../market_research/Scalability_2_4.md", "r", encoding="utf-8") as file:
                self.state.scalability = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(    
                "Scalability_2_4.md file not found. Please create a file '../market_research/Scalability_2_4.md' with your idea description."
            )
        except Exception as e:
            raise Exception(f"Error reading Scalability_2_4.md: {str(e)}")

    @listen(import_research)
    def generate_business_model(self):
        print("\n\n=======Generating business model=======\n\n")
        result = (
            BusinessDescriptionCrew()
            .crew()
            .kickoff(inputs={"structured_idea": self.state.structured_idea,
                            "demand_analysis": self.state.demand_analysis,
                            "barriers_to_entry": self.state.barriers_to_entry,
                            "competitive_level": self.state.competitive_level,
                            "scalability": self.state.scalability})
        )

        print("\n****Business description generated****\n")
        self.state.business_model = result.raw

    @listen(generate_business_model)
    def generate_patent_strategy(self):
        print("\n\n=======Generating patent strategy=======\n\n")
        result = (
            PatentDeveopmentCrew()
            .crew()
            .kickoff(inputs={"business_model": self.state.business_model})
        )
        print("\n****Patent strategy generated****\n")
        self.state.patent_strategy = result.raw


    @listen(generate_patent_strategy)
    def save_reports(self):
        print("\n\n=======Saving reports=======\n\n")
        with open("Reports/business_model.md", "w") as f:
            f.write(self.state.business_model)
        with open("Reports/Patent_Development_1_1.md", "w") as f:
            f.write(self.state.patent_strategy)


def kickoff():
    business_description_flow = BusinessDescriptionFlow()
    business_description_flow.kickoff()


def plot():
    business_description_flow = BusinessDescriptionFlow()
    business_description_flow.plot()


if __name__ == "__main__":
    kickoff()
