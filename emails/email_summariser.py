from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_STUDIO_API_KEY

llm = ChatGoogleGenerativeAI(
    model="models/gemma-3-27b-it", google_api_key=GOOGLE_STUDIO_API_KEY
)

prompt = PromptTemplate(
    input_variables=["text"],
    template="""
        Please provide a concise summary of the following email content:
        
        Email Content:
        {text}
        
        Summary Guidelines:
        - Keep it brief but comprehensive
        - Highlight key points and action items
        - Identify the main purpose/request
        - Note any deadlines or urgent matters
        - Use bullet points for clarity

        Summary:
    """,
)

chain = prompt | llm | StrOutputParser()


def summarise_email(email_body: str):
    return chain.invoke({"text": email_body})
