from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ResearchPlannerCrew():
	"""ResearchPlannerCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def market_research_planner(self) -> Agent:
		return Agent(
			config=self.agents_config['market_research_planner'],
			verbose=True
		)
	@task
	def idea_structuring_task(self) -> Task:
		return Task(
			config=self.tasks_config['idea_structuring_task'],
			output_file='Reports/Structured_Idea.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the 0ResearchPlannerCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
