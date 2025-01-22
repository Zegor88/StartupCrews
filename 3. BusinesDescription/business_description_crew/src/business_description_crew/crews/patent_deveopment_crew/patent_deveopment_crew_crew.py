from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class PatentDeveopmentCrew():
	"""Patent Development Crew"""

# ============================ AGENTS ============================
	@agent
	def founder(self) -> Agent:
		return Agent(
			config=self.agents_config['founder'],			
			verbose=True
		)

	@agent
	def legal_advisor(self) -> Agent:
		return Agent(
			config=self.agents_config['legal_advisor'],
			verbose=True
		)

	@agent
	def patent_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['patent_manager'],
			verbose=True
		)

# ============================ TASKS ============================
	@task
	def patent_research(self) -> Task:
		return Task(
			config=self.tasks_config['patent_research'],
		)

	@task
	def patent_strategy(self) -> Task:
		return Task(
			config=self.tasks_config['patent_strategy'],
			output_file='report.md'
		)

	@task
	def executive_summary(self) -> Task:
		return Task(
			config=self.tasks_config['executive_summary'],
			output_file='Patent_Development_1_1.md'
		)

# ============================ CREW ============================
	@crew
	def crew(self) -> Crew:
		"""Creates the Patent Development Crew"""
		return Crew(
			agents=[self.founder(), self.legal_advisor()], 
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			verbose=True,
			manager_agent=self.patent_manager(),
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)