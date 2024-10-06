# Welcome to an exploration of the LLM Multiverse
This little GitHub repository aims to provide very basic cookbook recipes for LLMs. 

<p align="center">
    <img src="./images/llama_crew.jpg">
</p>

The aim is to explore the 'multiverse' of LLM land where there are many different tools that handle similar tasks (perfect competitors), each with its own pros and cons. Feel free to request for an article!

## Roadmap
1. ~Basic LlamaIndex Recipes for LLMs (up to creating a single agent)~ - Done!
2. ~Basic Langchain Recipe for LLMs (up to creating a single agent)~ - Done!
3. Basic LlamaIndex Multi Agent Recipes (including the creation and deployment of the agents) - Upcoming
4. Basic Langgraph Multi Agent Recipes (including the creation and deployment of the agents) - Upcoming

## Related articles
Coming soon!

## Repository Layout
Note that each folder has its own requirements.txt! This is in the event of version conflicts - for example LlamaIndex and Langchain have moved to pydantic v2 but not all the LLM libraries have done the same!
```
.
├── LlamaIndex                                  
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for LlamaIndex (up to single agents)
│   ├── requirements.txt                  <- Requirements.txt for LlamaIndex repository
├── Langchain
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for Langchain (up to single agents)
│   ├── requirements.txt                  <- Requirements.txt for Langchain repository
├── data                                  <- Folder containing data sets for recipes
│       ├── paul_graham                   
│           |── paul_graham_essay.txt     <- txt file for RAG
```