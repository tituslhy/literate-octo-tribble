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
4. Basic LlamaIndex Multi Agent Recipes (including the creation and deployment of the agents) - Upcoming
5. Basic Langgraph Multi Agent Recipes (including the creation and deployment of the agents) - Upcoming

## Related articles
1. [A gentle introduction to the LLM Multiverse (Part 1): Langchain](https://medium.com/@tituslhy/a-gentle-introduction-to-the-llm-multiverse-part-1-langchain-023a899d294e)
2. **Coming soon! A gentle introduction to the LLM Multiverse (Part 2): Haystack**

## Repository Layout
Note that each folder has its own requirements.txt! This is in the event of version conflicts - for example LlamaIndex and Langchain have moved to pydantic v2 but not all the LLM libraries have done the same!
```
.
├── Haystack                                
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for Haystack (up to RAG)
│   ├── requirements.txt                  <- Requirements.txt for Haystack recipe
├── Langchain
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for Langchain (up to single agents)
│   ├── requirements.txt                  <- Requirements.txt for Langchain recipe
├── LlamaIndex                                  
│   ├── notebooks
│       ├── the_basics.ipynb              <- Basic recipes for LlamaIndex (up to single agents)
│   ├── requirements.txt                  <- Requirements.txt for LlamaIndex recipe
├── data                                  <- Folder containing data sets for recipes
│       ├── paul_graham                   
│           |── paul_graham_essay.txt     <- txt file for RAG
```