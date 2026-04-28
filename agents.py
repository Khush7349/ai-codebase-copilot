from rag import search
from llm import call

def refine_query(q):
    prompt = f"""
You are an expert developer.

Rewrite the query to make it more specific for searching a codebase.

Original query:
{q}

Refined query:
"""
    return call(prompt).strip()

def build_context(results):
    context_blocks = []
    for content, path in results:
        context_blocks.append(f"""
FILE: {path}
--------------------
{content[:500]}
""")
    return "\n\n".join(context_blocks)

def qa_agent(q):
    try:
        refined_q = refine_query(q)

        results = search(refined_q)
        context = build_context(results)

        prompt = f"""
You are a senior software engineer analyzing a codebase.

Instructions:
- Answer clearly and concisely
- Reference file paths
- Explain logic step-by-step
- If unsure, say "Not enough context"

Context:
{context}

Question:
{q}

Answer:
"""
        answer = call(prompt)

        return {
            "answer": answer,
            "sources": [r[1] for r in results]
        }

    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }

def explain_agent():
    try:
        results = search("project architecture structure flow data pipeline")

        context = build_context(results)

        prompt = f"""
You are a senior software architect.

Analyze the codebase and explain:

1. Overall architecture
2. Key components
3. Data flow
4. Design patterns used

Context:
{context}

Explanation:
"""
        return call(prompt)

    except Exception as e:
        return f"Error: {str(e)}"