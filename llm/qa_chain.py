from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory='/Users/othmanezoheir/tmp/shopify/vector_stores/TheGoodGoodco_vector_store',
                  embedding_function=embeddings)
llm = ChatOpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type="map_reduce",
                                       retriever=vectordb.as_retriever())