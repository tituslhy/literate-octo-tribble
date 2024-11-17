#%%

from llama_index.core.workflow import (
    Workflow,
    step,
    Event,
    Context,
    StartEvent,
    StopEvent
)
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import LLM
from llama_index.core.prompts import PromptTemplate
from llama_index.core.llms import ChatMessage

from typing import List
import json

llm = OpenAI(model="gpt-4o-mini", temperature=0)

_REASONING_MODULES = [
    "1. How could I devise an experiment to help solve that problem?",
    "2. Make a list of ideas for solving this problem, and apply them one by one to the problem to see if any progress can be made.",
    "3. How could I measure progress on this problem?",
    "4. How can I simplify the problem so that it is easier to solve?",
    "5. What are the key assumptions underlying this problem?",
    "6. What are the potential risks and drawbacks of each solution?",
    "7. What are the alternative perspectives or viewpoints on this problem?",
    "8. What are the long-term implications of this problem and its solutions?",
    "9. How can I break down this problem into smaller, more manageable parts?",
    "10. Critical Thinking: This style involves analyzing the problem from different perspectives, questioning assumptions, and evaluating the evidence or information available. It focuses on logical reasoning, evidence-based decision-making, and identifying potential biases or flaws in thinking.",
    "11. Try creative thinking, generate innovative and out-of-the-box ideas to solve the problem. Explore unconventional solutions, thinking beyond traditional boundaries, and encouraging imagination and originality.",
    "12. Seek input and collaboration from others to solve the problem. Emphasize teamwork, open communication, and leveraging the diverse perspectives and expertise of a group to come up with effective solutions.",
    "13. Use systems thinking: Consider the problem as part of a larger system and understanding the interconnectedness of various elements. Focuses on identifying the underlying causes, feedback loops, and interdependencies that influence the problem, and developing holistic solutions that address the system as a whole.",
    "14. Use Risk Analysis: Evaluate potential risks, uncertainties, and tradeoffs associated with different solutions or approaches to a problem. Emphasize assessing the potential consequences and likelihood of success or failure, and making informed decisions based on a balanced analysis of risks and benefits.",
    "15. Use Reflective Thinking: Step back from the problem, take the time for introspection and self-reflection. Examine personal biases, assumptions, and mental models that may influence problem-solving, and being open to learning from past experiences to improve future approaches.",
    "16. What is the core issue or problem that needs to be addressed?",
    "17. What are the underlying causes or factors contributing to the problem?",
    "18. Are there any potential solutions or strategies that have been tried before? If yes, what were the outcomes and lessons learned?",
    "19. What are the potential obstacles or challenges that might arise in solving this problem?",
    "20. Are there any relevant data or information that can provide insights into the problem? If yes, what data sources are available, and how can they be analyzed?",
    "21. Are there any stakeholders or individuals who are directly affected by the problem? What are their perspectives and needs?",
    "22. What resources (financial, human, technological, etc.) are needed to tackle the problem effectively?",
    "23. How can progress or success in solving the problem be measured or evaluated?",
    "24. What indicators or metrics can be used?",
    "25. Is the problem a technical or practical one that requires a specific expertise or skill set? Or is it more of a conceptual or theoretical problem?",
    "26. Does the problem involve a physical constraint, such as limited resources, infrastructure, or space?",
    "27. Is the problem related to human behavior, such as a social, cultural, or psychological issue?",
    "28. Does the problem involve decision-making or planning, where choices need to be made under uncertainty or with competing objectives?",
    "29. Is the problem an analytical one that requires data analysis, modeling, or optimization techniques?",
    "30. Is the problem a design challenge that requires creative solutions and innovation?",
    "31. Does the problem require addressing systemic or structural issues rather than just individual instances?",
    "32. Is the problem time-sensitive or urgent, requiring immediate attention and action?",
    "33. What kinds of solution typically are produced for this kind of problem specification?",
    "34. Given the problem specification and the current best solution, have a guess about other possible solutions."
    "35. Let’s imagine the current best solution is totally wrong, what other ways are there to think about the problem specification?"
    "36. What is the best way to modify this current best solution, given what you know about these kinds of problem specification?"
    "37. Ignoring the current best solution, create an entirely new solution to the problem."
    "38. Let’s think step by step ."
    "39. Let’s make a step by step plan and implement it with good notation and explanation.",
]

_REASONING_MODULES = "\n".join(_REASONING_MODULES)

SELECT_PRMOPT_TEMPLATE = PromptTemplate(
    "Given the task: {task}, which of the following reasoning modules are relevant? Do not elaborate on why.\n\n {reasoning_modules}"
)

ADAPT_PROMPT_TEMPLATE = PromptTemplate(
    "Without working out the full solution, adapt the following reasoning modules to be specific to our task:\n{selected_modules}\n\nOur task:\n{task}"
)

IMPLEMENT_PROMPT_TEMPLATE = PromptTemplate(
    "Without working out the full solution, create an actionable reasoning structure for the task using these adapted reasoning modules:\n{adapted_modules}\n\nTask Description:\n{task}"
)

REASONING_PROMPT_TEMPLATE = PromptTemplate(
    "Using the following reasoning structure: {reasoning_structure}\n\nSolve this task, providing your final answer: {task}"
)

class SetupEvent(Event):
    task: str

class GetModulesEvent(Event):
    """Event to get modules."""
    task: str
    modules: str

class RefineModulesEvent(Event):
    """Event to refine modules."""
    task: str
    refined_modules: str

class ReasoningStructureEvent(Event):
    """Event to create reasoning structure."""
    task: str
    reasoning_structure: str

class SelfDiscoverWorkflow(Workflow):
    def __init__(
        self,
        llm: LLM = llm,
        chat_history: List[ChatMessage] = [],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.agent = SimpleChatEngine.from_defaults(llm=llm)
        self.chat_history = chat_history
    
    def process_chat_history(self):
        return [message.dict() for message in self.chat_history]
    
    @step
    async def judge_query(self, ctx: Context, ev: StartEvent) -> StopEvent | SetupEvent:
        """Event to judge whether a query is well-written and to seek
        clarification if the query is not well-written"""
        
        self.chat_history.append(ChatMessage(**{"role": "user", "content": ev.task}))
        
        response = await self.agent.achat(
            f"""
            Given a user query, determine if this is likely to yield good results from a RAG system as-is. If it's good, return 'good', if it's bad, return 'bad', if 
            it's not a question (for e.g. "Hi!", "Thanks!"), return "not a question".
            Good queries use a lot of relevant keywords and are detailed. Bad queries are vague or ambiguous.

            Here is the query: {ev.task}
            """
        )
        print("\n\nJudge Query response: "+ str(response) + "\n\n")
        if str(response) == "bad":
            final_response = await self.agent.achat(
                f"""
                The user has given a poor query. Seek for clarification from the user.
                
                Here's the user's query: {ev.task}
                """,
                chat_history = self.chat_history
            )   
            self.chat_history.append(ChatMessage(**{"role": "assistant", "content": str(final_response)}))
            return StopEvent(str(final_response)) 
        
        elif str(response) == "not a question":
            final_response = await self.agent.achat(
                f"""
                Here's the user's remark or greeting: {ev.task}
                
                Respond to the user politely.
                """,
                chat_history = self.chat_history
            )   
            self.chat_history.append(ChatMessage(**{"role": "assistant", "content": str(final_response)}))
            return StopEvent(str(final_response)) 
        
        return SetupEvent(task=ev.task)

    @step
    async def get_modules(
        self, ctx: Context, ev: SetupEvent
    ) -> GetModulesEvent:
        """Get modules step."""
        task = ev.get("task")
        
        # format prompt and get result from LLM
        prompt = SELECT_PRMOPT_TEMPLATE.format(
            task=task, reasoning_modules=_REASONING_MODULES
        )
        result = await self.agent.achat(prompt, chat_history = self.chat_history)
        print("\n\nModules selected: " + str(result) + "\n\n")
        self.chat_history.append(ChatMessage(**{"role": "assistant", "content": str(result)}))
        return GetModulesEvent(task=str(task), modules=str(result))

    @step
    async def refine_modules(
        self, ctx: Context, ev: GetModulesEvent
    ) -> RefineModulesEvent:
        """Refine modules step."""
        task = ev.task
        modules = ev.modules
        
        # format prompt and get result
        prompt = ADAPT_PROMPT_TEMPLATE.format(
            task=task, selected_modules=modules
        )
        result = await self.agent.achat(prompt, chat_history = self.chat_history)
        print("\n\nRefined modules: " + str(result) + "\n\n")
        self.chat_history.append(ChatMessage(**{"role": "assistant", "content": str(result)}))
        return RefineModulesEvent(task=task, refined_modules=str(result))

    @step
    async def create_reasoning_structure(
        self, ctx: Context, ev: RefineModulesEvent
    ) -> ReasoningStructureEvent:
        """Create reasoning structures step."""
        task = ev.task
        refined_modules = ev.refined_modules

        # format prompt, get result
        prompt = IMPLEMENT_PROMPT_TEMPLATE.format(
            task=task, adapted_modules=refined_modules
        )
        result = await self.agent.achat(prompt, chat_history = self.chat_history)
        print("\n\nImplementation results: " + str(result) + "\n\n")
        self.chat_history.append(ChatMessage(**{"role": "assistant", "content": str(result)}))

        return ReasoningStructureEvent(
            task=task, reasoning_structure=str(result)
        )

    @step
    async def get_final_result(
        self, ctx: Context, ev: ReasoningStructureEvent
    ) -> StopEvent:
        """Gets final result from reasoning structure event."""
        task = ev.task
        reasoning_structure = ev.reasoning_structure

        # format prompt, get res
        prompt = REASONING_PROMPT_TEMPLATE.format(
            task=task, reasoning_structure=reasoning_structure
        )
        result = await self.agent.achat(prompt, chat_history = self.chat_history)
        print("\n\nReasoning: " + str(result) + "\n\n")
        self.chat_history.append(ChatMessage(**{"role": "assistant", "content": str(result)}))

        return StopEvent(
            result=str(result) + " ||History||: " + json.dumps(self.process_chat_history())
        )
# %%
