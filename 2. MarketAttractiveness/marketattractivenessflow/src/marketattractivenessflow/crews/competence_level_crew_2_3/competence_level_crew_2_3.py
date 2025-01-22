from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from marketattractivenessflow.tools.PerplexitySearchTool import PerplexitySearchTool

# ============================ TOOLS ============================
perplexity_search_tool = PerplexitySearchTool()

# ============================ CREW ============================

@CrewBase
class CompetenceLevelCrew23():
	"""CompetenceLevelCrew23 crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# ============================ AGENTS ============================
	@agent
	def competitive_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['competitive_analyst'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def technical_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_specialist'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def local_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['local_expert'],
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
	def competitor_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['competitor_analysis'],
		)

	@task
	def technical_benchmarking(self) -> Task:
		return Task(
			config=self.tasks_config['technical_benchmarking'],
		)

	@task
	def local_market_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['local_market_analysis'],
		)

	@task
	def competitive_strategy(self) -> Task:
		return Task(
			config=self.tasks_config['competitive_strategy'],
			context=[
				self.competitor_analysis(),
				self.technical_benchmarking(),
				self.local_market_analysis()
			],
			output_file='Reports/Competitive_Level_2_3.md'
		)	

	# ============================ CREW ============================
	@crew
	def crew(self) -> Crew:
		"""Creates the CompetenceLevelCrew23 crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
