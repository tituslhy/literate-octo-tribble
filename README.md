# Welcome to an exploration of the LLM Multiverse
This little GitHub repository aims to provide very basic cookbook recipes for LLMs. 

<p align="center">
    <img src="./images/llama_crew.jpg">
</p>

The aim is to explore the 'multiverse' of LLM land where there are many different tools that handle similar tasks (perfect competitors), each with its own pros and cons. Feel free to request for an article!

## Roadmap
1. ~Basic Langchain Recipes for LLMs (up to creating a single agent)~ - Done!
2. ~Basic Haystack Recipe for LLMs (up to creating a single agent)~ - Done!
3. ~Basic LlamaIndex Recipe for LLMs (up to creating a single agent)~ - Done!
4. ~Basic Langgraph Multi Agent Recipes (building a personal assistant)~ - Done!
5. ~Basic Autogen Multi Agent Recipes (building a stock assistant)~ - Done!
6. Basic LlamaIndex Multi Agent Recipes - Upcoming
7. Basic crewAI Mult Agent Recipes - Upcoming

## Related articles
1. [A gentle introduction to the LLM Multiverse (Part 1): Langchain](https://medium.com/@tituslhy/a-gentle-introduction-to-the-llm-multiverse-part-1-langchain-023a899d294e)
2. [A gentle introduction to the LLM Multiverse (Part 2): Haystack](https://medium.com/mitb-for-all/a-gentle-introduction-to-the-llm-multiverse-part-2-haystack-c6af2548df04)
3. [A gentle introduction to the LLM Multiverse (Part 3): LlamaIndex](https://medium.com/mitb-for-all/a-gentle-introduction-to-the-llm-multiverse-part-3-llamaindex-798344050c49)
4. [A gentle introduction to the LLM Multi-Agents Multiverse (Part 1): Langgraph](https://medium.com/@tituslhy/a-gentle-introduction-to-the-llm-multi-agents-multiverse-part-1-langgraph-2ac56f1b5b3c)

## Repository Layout
Note that each folder has its own requirements.txt! This is in the event of version conflicts - for example LlamaIndex and Langchain have moved to pydantic v2 but not all the LLM libraries have done the same!
```
.
├── Autogen
│   ├── notebooks
│       ├── stock_analysis.ipynb          <- Code book for autogen stock analyst app
│       ├── blogs                         <- Python scripts generated by Autogen's command line executor
│       ├── report.md                     <- Final report generated
│   ├── requirements.txt                  <- Requirements.txt for Autogen code
│   ├── AutogenStudio                     <- Snapshots of AutogenStudio executions
├── Haystack                                
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for Haystack (up to RAG)
│   ├── requirements.txt                  <- Requirements.txt for Haystack recipe
├── Langchain
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for Langchain (up to single agents)
│       ├── langgraph.ipynb               <- Code book for Langgraph personal assistant app
│       ├── langgraph_studio              <- Files for loading into the Langgraph Studio software
│   ├── requirements.txt                  <- Requirements.txt for LangChain and Langgraph codes
├── LlamaIndex                                  
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for LlamaIndex (up to single agents)
│   ├── requirements.txt                  <- Requirements.txt for LlamaIndex recipe
├── data                                  <- Folder containing data sets for recipes
│       ├── paul_graham                   
│           |── paul_graham_essay.txt     <- txt file for RAG
```