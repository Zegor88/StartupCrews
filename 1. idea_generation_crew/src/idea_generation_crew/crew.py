from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool, TXTSearchTool
from idea_generation_crew.tools.PerplexitySearchTool import PerplexitySearchTool

# ============================== TOOLS ==============================

perplexity_search = PerplexitySearchTool()

# law_of_serbia_txt_tool = TXTSearchTool(txt="idea_generation_crew/src/idea_generation_crew/tools/StartupLawSpain.txt")

# ============================== CREW ==============================
@CrewBase
class IdeaGenerationCrew():
	"""IdeaGenerationCrew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# ============================== AGENTS ==============================
	@agent
	def trend_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['trend_analyst'],
			verbose=True,
			tools=[perplexity_search]
		)

	@agent
	def customer_insight_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['customer_insight_specialist'],
			verbose=True,
			tools=[perplexity_search]
		)

	@agent
	def innovative_ideas_developer(self) -> Agent:
		return Agent(
			config=self.agents_config['innovative_ideas_developer'],
			verbose=True
		)

	@agent
	def concept_paper_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['concept_paper_specialist'],
			verbose=True,
			# tools=[PDFSearchTool(pdf='src/idea_generation_crew/tools/StartupLawSpain.pdf')]
		)

# ============================== TASKS ==============================
	@task
	def research_emerging_trends(self) -> Task:
		return Task(
			config=self.tasks_config['research_emerging_trends'],
		)

	@task
	def analyze_customer_pain_points(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_customer_pain_points'],
		)

	@task
	def develop_innovative_solutions(self) -> Task:
		return Task(
			config=self.tasks_config['develop_innovative_solutions'],
		)

	@task
	def create_concept_paper(self) -> Task:
		return Task(
			config=self.tasks_config['create_concept_paper'],
			output_file='Report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the IdeaGenerationCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True
		)