from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ScalabilityCrew24():
	"""ScalabilityCrew24 crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

# ============================ AGENTS ============================
	@agent
	def technical_architect(self) -> Agent:
		return Agent(
			config=self.agents_config['technical_architect'],
			verbose=True
		)

	@agent
	def business_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['business_strategist'],
			verbose=True
		)

	@agent
	def operations_manager(self) -> Agent:
		return Agent(
			config=self.agents_config['operations_manager'],
			verbose=True
		)

	@agent
	def report_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['report_writer'],
			verbose=True,
		)

# ============================ TASKS ============================
	@task
	def technical_scalability_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['technical_scalability_analysis'],
		)

	@task
	def business_model_scaling(self) -> Task:
		return Task(
			config=self.tasks_config['business_model_scaling'],
		)

	@task
	def operations_scaling_plan(self) -> Task:
		return Task(
			config=self.tasks_config['operations_scaling_plan'],
			context=[
				self.technical_scalability_analysis(),
				self.business_model_scaling()
			]
		)

	@task
	def report_writing(self) -> Task:
		return Task(
			config=self.tasks_config['report_writing'],
			context=[
				self.technical_scalability_analysis(),
				self.business_model_scaling(),
				self.operations_scaling_plan()
			],
			output_file='Reports/Scalability_2_4.md'
		)

# ============================ CREW ============================
	@crew
	def crew(self) -> Crew:
		"""Creates the ScalabilityCrew24 crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
