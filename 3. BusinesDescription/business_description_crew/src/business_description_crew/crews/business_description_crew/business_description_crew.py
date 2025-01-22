from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

# # Create a PDF knowledge source
# pdf_source = PDFKnowledgeSource(
#     file_paths=[
# 		# "DGM 1-2023.pdf", 
# 		"StartupLawSpain.pdf"]
# )

@CrewBase
class BusinessDescriptionCrew():
	"""BusinessDescriptionCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def founder(self) -> Agent:
		return Agent(
			config=self.agents_config['founder'],
			verbose=True,
			# knowledge_sources=[pdf_source]
		)

	@task
	def startup_description(self) -> Task:
		return Task(
			config=self.tasks_config['startup_description']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the BusinessDescriptionCrew crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			# knowledge_sources=[pdf_source],
			verbose=True,
		)