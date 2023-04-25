# shopifyGPT-backend

This repo is a GPT powered Shopify chat backend prototype. It uses Flask as a backend with a single endpoint, aimed to serve requests from in store chat widgets. The idea of the plugin is to have an easily pluggable chat widget on ANY store, stricly using the store URL as input.

Notes:
- This was developped independently of the Shopify AI plugin
- This is a prototype. It's missing a bunch of features, but the design is scalable for anyone to implement on top of it.

Below are some features of the application/design:
- Authentification less scraping of ANY shopify store. All that's needed is a URL
- Chat session management including infinite memory.
- Ability to ask questions about products and store information and policies about any shopify store

Application architecture


![image](https://i.ibb.co/K9XjTKD/plugin-drawio.png)
