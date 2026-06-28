PROMPT = """
You are an information extraction engine.

Convert the supplied maintenance report into JSON.

Return ONLY JSON.

Schema:

{
    "asset":"",
    "issue":"",
    "priority":"",
    "operator":"",
    "recommendation":""
}

Report:

{text}
"""