from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from marketattractivenessflow.tools.char_counter_tool import CharCounterTool

@CrewBase
class FinalReportCrew():
	"""FinalReportCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

# =============================== AGENTS ===============================
	@agent
	def research_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['research_analyst'],
			verbose=True,
		)

	@agent
	def report_reviewer(self) -> Agent:
		return Agent(
			config=self.agents_config['report_reviewer'],
			verbose=True,
			tools=[CharCounterTool()]
		)

	@agent
	def business_plan_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['business_plan_expert'],
			verbose=True,
		)

# =============================== TASKS ===============================
	@task
	def review_report(self) -> Task:
		return Task(
			config=self.tasks_config['review_report'],
		)

	@task
	def synthesis_task(self) -> Task:
		return Task(
			config=self.tasks_config['synthesis_task'],
		)

	@task 
	def review_task(self) -> Task:
		return Task(
			config=self.tasks_config['review_task'],
		)

	@task
	def final_report_task(self) -> Task:
		return Task(
			config=self.tasks_config['final_report_task'],
			output_file='MarketAttractivenessReport.md'
		)

# =============================== CREW ===============================
	@crew
	def crew(self) -> Crew:
		"""Creates the FinalReportCrew crew"""

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
