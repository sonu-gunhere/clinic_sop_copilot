# import os
# import opik
# from dotenv import load_dotenv
# load_dotenv()


# client = opik.Client(api_key=os.getenv("OPIK_API_KEY"))

# def log_interaction(query, response, citations, tool_used):
#     """
#     Send interaction logs to Opik for evaluation.
#     """

#     # Tool compliance → Did we use SOP or Web tool?
#     tool_compliance = "Yes" if tool_used else "No"

#     # Citation coverage → % sentences with citations
#     sentences = [s.strip() for s in response.split(".") if s.strip()]
#     cited = sum(1 for s in sentences if any(c in s for c in citations))
#     citation_coverage = round((cited / len(sentences)) * 100, 2) if sentences else 0

#     # Send to Opik
#     client.log({
#         "query": query,
#         "response": response,
#         "tool_compliance": tool_compliance,
#         "citation_coverage": citation_coverage,
#         "citations": citations
#     })

#     return {"tool_compliance": tool_compliance, "citation_coverage": citation_coverage}
