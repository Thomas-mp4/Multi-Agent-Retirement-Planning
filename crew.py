from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from crewai_tools.tools.txt_search_tool.txt_search_tool import TXTSearchTool
import os

# Global settings
verbose = True

# Prepare prompt
client = "John Doe"
query = "Am I on track for retirement?"
request = (
    f"{client} requests retirement advice. Their question is as follows: '{query}'."
    " This task involves collecting client information, researching industry data, analyzing the data,"
    " and generating tailored advice."
)
print(f"Continuing with the following request:"
      f"\n------------------------------------------------------------------------------------\n"
      f"{request}"
      f"\n------------------------------------------------------------------------------------\n")


# Tools
@tool("Retrieve client information")
def retrieve_client_information(full_client_name: str):
    """
    Retrieve information about the client.
    :param full_client_name: The full name of the client. (E.g., "Firstname_Lastname")
    :return: Information about the client.
    """
    # Note: For demonstration purposes, this information is
    # stored in a text file. In practice, this could be retrieved from an internal database.
    path_to_file = os.path.join("./assets/mock-customers/", f"{full_client_name}.txt")
    try:
        with open(path_to_file, "r") as file:
            content = file.read()
    except FileNotFoundError:
        return (
            f"Client information for {full_client_name} not found. Make sure the client's name is formatted correctly."
            f"(e.g., 'Firstname_Lastname')")

    return content


@tool("Retrieve average account balances by age")
def retrieve_average_account_balances_by_age():
    """List of Average Superannuation Account Balances by Age and Gender"""
    try:
        with open("assets/RAG-sources/superannuation-account-balances.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        return "File not found, tool is unusable"
    return content


rag_industry_average_performance_return = TXTSearchTool(
    txt="assets/RAG-sources/industry-average-performance-return.txt")

rag_concessional_contribution_cap = TXTSearchTool(
    txt="assets/RAG-sources/concessional-contributions-cap.txt")

rag_non_concessional_contribution_cap = TXTSearchTool(
    txt="assets/RAG-sources/non-consessional-contributions-cap.txt")

rag_restrictions_on_voluntary_contributions = TXTSearchTool(
    txt="assets/RAG-sources/restrictions-on-voluntary-contributions.txt")

rag_understanding_concessional_contributions = TXTSearchTool(
    txt="assets/RAG-sources/understanding-contributions.txt")

# Define Agents
advisory_agent = Agent(
    role="Advisory Expert",
    goal=("Understand the client's inquiry, and based on the information gathered by colleagues, "
          "provide the best retirement advice in a simple manner "
          "that is easy for the client to understand."),
    backstory=("With a background in client advisory services, "
               "you specialize in understanding client inquiries and synthesizing complex information into clear, "
               "actionable advice. "
               "Your communication skills ensure clients feel confident in their financial decisions."
               "Make sure to provide full, complete answers, and make no assumptions."),
    verbose=verbose,
    tools=[retrieve_client_information],
    allow_delegation=False
)

policy_agent = Agent(
    role="Policy Expert",
    goal=("Analyze current retirement policies and regulations based on client details, "
          "and the tools available to you, to provide a comprehensive report on relevant retirement policy information."),
    backstory=("With over 20 years of experience in financial regulation, "
               "you specialize in understanding the intricacies of retirement policies and regulations. "
               "Your analytical skills and attention to detail make you adept at providing detailed "
               "reports on relevant policy information."
               "Make sure to provide full, complete answers, and make no assumptions."),
    verbose=verbose,
    tools=[retrieve_client_information,
           rag_concessional_contribution_cap,
           rag_non_concessional_contribution_cap,
           rag_restrictions_on_voluntary_contributions,
           rag_understanding_concessional_contributions],
    allow_delegation=False
)

industry_agent = Agent(
    role="Industry Expert",
    goal=("Analyze the retirement industry through the tools available to you, and based on the client's request, "
          "to provide a comprehensive report on relevant retirement industry information."),
    backstory=("With a deep understanding of the retirement industry and trends, "
               "you specialize in analyzing industry data to provide insights on retirement savings. "
               "Your expertise in industry analysis helps you identify key trends and patterns "
               "to support client requests."
               "Make sure to provide full, complete answers, and make no assumptions."),
    verbose=verbose,
    tools=[retrieve_client_information,
           retrieve_average_account_balances_by_age,
           rag_industry_average_performance_return],
    allow_delegation=False
)

quality_assurance_agent = Agent(
    role="Quality Assurance Expert",
    goal=("Review the reports generated by the policy, industry, and advisory experts to ensure they are accurate, "
          "comprehensive, and meet the client's needs."),
    backstory=("With a keen eye for detail and a focus on quality, "
               "you specialize in reviewing reports to ensure they meet the highest standards. "
               "Your role is crucial in ensuring the client receives accurate and relevant information."
               "Make sure to provide full complete answers, and make no assumptions."),
    verbose=verbose,
    allow_delegation=True)

# Define Tasks
policy_task = Task(
    description=(
        f'Research and gather data on retirement policy options and limitations,'
        f' focusing on information relevant to the client\'s request, and the tools'
        f' available to you.The client\'s request: {query}'
        f'The client\'s name: {client}'
        f'Consider which tools you actually need, and also consider whether this task is necessary given the client\'s request.'),
    agent=policy_agent,
    expected_output="A comprehensive report on retirement policy information relevant to the client's request.",
)

industry_task = Task(
    description=(f'Research and gather data on the retirement industry, '
                 f'focusing on information relevant to the client\'s request, and the tools available to you.'
                 f'The client\'s request: {query}'
                 f'The client\'s name: {client}'
                 f'Consider which tools you actually need, and also consider whether this task is necessary given the client\'s request.'),
    agent=industry_agent,
    expected_output="A comprehensive report on industry information relevant to the client's request.",
)

advisory_task = Task(
    description=(f'Understand the client\'s inquiry, and based on the information gathered by '
                 f'the policy and industry experts, provide the best retirement advice in a simple manner '
                 f'that is easy for the client to understand.'
                 f'The client\'s request: {query}'
                 f'The client\'s name: {client}'
                 f'Consider which tools you actually need, and also consider whether this task is necessary given the client\'s request.'),
    expected_output="A clear and concise retirement advice report that addresses the client's inquiry"
                    " and integrates insights from policy and market analysis.",
    agent=advisory_agent
)

quality_review_task = Task(
    description=(
        f'Review the reports generated by the policy, industry, and advisory experts to ensure they are accurate, '
        f'comprehensive, and meet the client\'s needs.'
        f'The client\'s request: {query}'
        f'The client\'s name: {client}'
    ),
    expected_output="A final version of retirement advice report that has been reviewed and approved by the QA expert.",
    agent=quality_assurance_agent)


# Define the Crew
crew = Crew(
    agents=[policy_agent, industry_agent, advisory_agent, quality_assurance_agent],
    tasks=[policy_task, industry_task, advisory_task, quality_review_task],
    process=Process.sequential,
    verbose=2,
    memory=True
)

# Run the Crew
result = crew.kickoff()
print(f"\n------------------------------------------------------------------------------------\n"
      f"CREWAI RESULTS:"
      f"{result}"
      f"\n------------------------------------------------------------------------------------\n")
