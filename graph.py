from langgraph.graph import StateGraph
class GraphState(dict):
    pass
def refine_query(state):
    from llm import call

    q = state["question"]

    prompt = f"""
Rewrite the query to improve codebase search.

Original:
{q}

Refined:
"""
    refined = call(prompt).strip()

    return {"refined_query": refined}
def retrieve(state):
    from rag import search
    query = state.get("refined_query", state["question"])
    results = search(query)

    return {"context": results}
def build_context(state):
    results = state.get("context", [])

    if not results:
        return {"formatted_context": "No relevant code found."}

    formatted = "\n\n".join(
        [f"FILE: {path}\n{content[:400]}" for content, path in results]
    )

    return {"formatted_context": formatted}

def generate_answer(state):
    from llm import call

    prompt = f"""
You are a senior software engineer.

Answer clearly using the code context.
Mention file paths where relevant.

Context:
{state['formatted_context']}

Question:
{state['question']}
"""
    answer = call(prompt)
    return {
        "answer": answer,
        "context": state.get("context", []) 
    }
graph = StateGraph(GraphState)
graph.add_node("refine", refine_query)
graph.add_node("retrieve", retrieve)
graph.add_node("context_builder", build_context)
graph.add_node("generate", generate_answer)
graph.set_entry_point("refine")
graph.add_edge("refine", "retrieve")
graph.add_edge("retrieve", "context_builder")
graph.add_edge("context_builder", "generate")
app_graph = graph.compile()