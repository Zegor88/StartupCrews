from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from marketattractivenessflow.tools.PerplexitySearchTool import PerplexitySearchTool

# ============================ TOOLS ============================
perplexity_search_tool = PerplexitySearchTool()

# ============================ CREW ============================
@CrewBase
class BarriersToEntryCrew22():
	"""BarriersToEntryCrew22 crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# ============================ AGENTS ============================
	@agent
	def market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['market_analyst'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def technical_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_expert'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def regulatory_advisor(self) -> Agent:
		return Agent(
			config=self.agents_config['regulatory_advisor'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def report_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['report_writer'],
			verbose=True,
		)

	# ============================ TASKS ============================
	@task
	def market_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['market_analysis_task'],
		)

	@task
	def technical_assessment_task(self) -> Task:
		return Task(
			config=self.tasks_config['technical_assessment_task'],
		)

	@task
	def regulatory_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['regulatory_analysis_task'],
		)

	@task
	def final_report_task(self) -> Task:
		return Task(
			config=self.tasks_config['final_report_task'],
			output_file='Reports/Barriers_to_Entry_2_2.md',
			context=[
				self.market_analysis_task(),
				self.technical_assessment_task(),
				self.regulatory_analysis_task()
			]
		)

	# ============================ CREW ============================
	@crew
	def crew(self) -> Crew:
		"""Creates the BarriersToEntryCrew22 crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)