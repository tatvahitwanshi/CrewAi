from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, task, crew
from dotenv import load_dotenv
import os

from task.github_tool.github_tool import fetch_pr_files
from crew.output_schema import PRReviewOutput

# Load environment variables
load_dotenv()

# Configure Groq LLM
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


@CrewBase
class GitHubPRCrew:
    """GitHub PR Review Crew"""
    
    # Load YAML configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # TASK-2: GitHub Tool Agent
    @agent
    def github_tool_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['github_tool_agent'],
            tools=[fetch_pr_files],
            llm=groq_llm,
            verbose=True
        )

    # TASK-3: Code Analysis Agents
    @agent
    def code_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_analyzer_agent'],
            llm=groq_llm,
            verbose=True
        )
    
    @agent
    def bug_detection_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['bug_detection_agent'],
            llm=groq_llm,
            verbose=True
        )
    
    @agent
    def optimization_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['optimization_agent'],
            llm=groq_llm,
            verbose=True
        )

    # TASK-2: Fetch PR Files
    @task
    def fetch_pr_files_task(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_pr_files_task'],
            agent=self.github_tool_agent(),
            context=[]
        )
    
    # TASK-3: Code Review Tasks
    @task
    def code_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_analysis_task'],
            agent=self.code_analyzer_agent(),
            context=[self.fetch_pr_files_task()]
        )
    
    @task
    def bug_detection_task(self) -> Task:
        return Task(
            config=self.tasks_config['bug_detection_task'],
            agent=self.bug_detection_agent(),
            context=[self.fetch_pr_files_task()]
        )
    
    @task
    def optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['optimization_task'],
            agent=self.optimization_agent(),
            context=[self.fetch_pr_files_task()]
        )
    
    @task
    def merge_review_results_task(self) -> Task:
        return Task(
            config=self.tasks_config['merge_review_results_task'],
            agent=self.code_analyzer_agent(),  # Lead agent merges all results
            context=[
                self.code_analysis_task(),
                self.bug_detection_task(),
                self.optimization_task()
            ],
            output_json=PRReviewOutput
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
            # output_log_file="crew_output.log"
        )
