def standardize_legal_query(user_query: str) -> str:
    """
    Generates a prompt to extract standardized legal search terms from a user query.
    The agent's model will use this prompt to generate the keywords.
    """
    return f'''
    Extract 3-6 legal search terms relevant to this query:
    "{user_query}"

    Return only a Python list of strings like:
    ["mold", "tenant rights", "habitability"]
    '''
