import os
from openai import AzureOpenAI
from backend.services import sop_service, cite_service, web_service
from dotenv import load_dotenv
load_dotenv()


client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),

)


# def generate_answer(query: str):
#     """
#     Orchestrates SOP search, read, and citation validation.
#     """

#     # Step 1: Search SOPs
#     search_results = sop_service.search(query)
#     if not search_results["matches"]:
#         return {"answer": "No relevant SOP found. Please clarify your query.", "citations": []}

#     # Step 2: Read top SOP match
#     top_match = search_results["matches"][0]["file"].replace(".md", "")
#     sop_text = sop_service.read(top_match).get("content", "")

#     # Step 3: Ask LLM to compose grounded answer
#     prompt = f"""
#     You are a clinical SOP assistant.
#     Question: {query}
#     Use the following SOP content to answer:
#     SOP: {sop_text}

#     Answer in clear steps and include citations like [SOP:{top_match}].
#     """

#     response = client.chat.completions.create(
#         model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
#         messages=[{"role": "system", "content": "You are a clinical SOP assistant."},
#                   {"role": "user", "content": prompt}]
#     )

#     answer = response.choices[0].message.content

#     # Step 4: Validate citations
#     citations = [f"[SOP:{top_match}]"]
#     validation = cite_service.validate(answer, citations)

#     return {"answer": answer, "citations": citations, "validation": validation}


def generate_answer(query: str):
    """
    Orchestrates SOP search, read, and citation validation with fallback web search.
    """
    # Step 1: Search SOPs
    search_results = sop_service.search(query)

    if not search_results["matches"]:
        # Step 1a: If no SOP → fallback to web search
        web_results = web_service.search(query)
        docs = "\n".join([f"{r['title']} - {r['snippet']} ({r['link']})"
                          for r in web_results.get("organic", [])[:3]])

        prompt = f"""
        User Question: {query}
        No SOP found. Use the following external references:
        {docs}
        Provide answer in clinical style with citation links.
        """
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
            messages=[{"role": "system", "content": "You are a clinical assistant."},
                      {"role": "user", "content": prompt}]
        )
        # final_answer = response.choices[0].message.content
        # eval_service.log_interaction(
        #     query, final_answer, ["External Sources"], tool_used="web")
        return {"answer": response.choices[0].message.content, "citations": ["External Sources"]}

    # Step 2: Read top SOP match
    top_match = search_results["matches"][0]["file"].replace(".md", "")
    sop_text = sop_service.read(top_match).get("content", "")

    # Step 3: Ask LLM to compose grounded answer
    prompt = f"""
    You are a clinical SOP assistant. 
    Question: {query}
    SOP: {sop_text}

    Answer clearly and include citation like [SOP:{top_match}].
    """

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL_NAME"),
        messages=[{"role": "system", "content": "You are a clinical SOP assistant."},
                  {"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    citations = [f"[SOP:{top_match}]"]

    # Step 4: Validate citations
    validation = cite_service.validate(answer, citations)
    # final_answer = response.choices[0].message.content
    # eval_service.log_interaction(
    #     query, final_answer, citations, tool_used="sop")

    return {"answer": answer, "citations": citations, "validation": validation}
