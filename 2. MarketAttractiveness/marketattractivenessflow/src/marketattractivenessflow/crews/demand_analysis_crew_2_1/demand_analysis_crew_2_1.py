from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from marketattractivenessflow.tools.PerplexitySearchTool import PerplexitySearchTool
# ============================ TOOLS ============================
perplexity_search_tool = PerplexitySearchTool()

# ============================ CREW ============================
@CrewBase
class DemandAnalysisCrew21():
	"""Analysis of the Demand for Products or Services"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# ============================ AGENTS ============================
	@agent
	def market_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['market_researcher'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def competitive_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['competitive_analyst'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def regional_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['regional_analyst'],
			verbose=True,
			tools=[perplexity_search_tool]
		)

	@agent
	def data_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['data_strategist'],
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
	def collect_market_data(self) -> Task:
		return Task(
			config=self.tasks_config['collect_market_data'],
		)

	@task
	def identify_growth_drivers(self) -> Task:
		return Task(
			config=self.tasks_config['identify_growth_drivers'],
		)

	@task
	def analyze_local_specifics(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_local_specifics'],
		)

	@task
	def assess_competition(self) -> Task:
		return Task(
			config=self.tasks_config['assess_competition'],
		)

	@task
	def forecast_demand(self) -> Task:
		return Task(
			config=self.tasks_config['forecast_demand'],
		)

	@task
	def compile_final_report(self) -> Task:
		return Task(
			config=self.tasks_config['compile_final_report'],
			output_file='Reports/Demand_Analysis_2_1.md',
			context=[
				self.collect_market_data(),
				self.identify_growth_drivers(),
				self.analyze_local_specifics(),
				self.assess_competition(),
				self.forecast_demand()
			]
		)

	# ============================ CREW ============================
	@crew
	def crew(self) -> Crew:
		"""Analysis of the Demand for Products or Services"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
