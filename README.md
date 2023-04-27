# A GPT powered Shopify customer representative

### Description 
This repo is a GPT powered Shopify chat backend prototype. It uses Flask as a backend with a single endpoint, aimed to serve requests from in store chat widgets. The idea of the plugin is to have an easily pluggable chat widget on ANY store, stricly using the store URL as input.

### Notes:
- This was developped independently of the Shopify AI plugin
- This is a prototype. It's missing a bunch of features, but the design is scalable for anyone to implement on top of it.

### Below are some features of the application/design:
- Authentification less scraping of ANY shopify store. All that's needed is a URL
- Chat session management including infinite memory.
- Ability to ask questions about products and store information and policies about any shopify store

### Application architecture

![image](https://i.ibb.co/K9XjTKD/plugin-drawio.png)


### TODOS
- Multi store management (Database, Vector store..)
- Improve Customer Rep agent through prompt engineering (tone, dealing with unrelated queries etc...)
- Eventually directly plug into Shopify plugin for additional use cases (creating/managing/tracking orders...)
- Generate recommendations using customer chat history
- Dockerize, CI/CD...


### Running the app

Any recent version of Python would work. Dependencies:
```
pip install flask langchain openai chromedb tiktoken pandas requests numpy
```

Running the app locally:
```
python app/app.py
```




