from langsmith import traceable

@traceable(run_type="tool")
def run(content:str="")->dict:
    """This tool returns the final output to the user. This tool must be madatorily called if the user needs to get the output for their query."""
    status=True
    if content:
        final_output=content
    else:
        final_output="No results to display"
    
    return {
                "status":status,
                "content":final_output,
                "error":"",
                "metadata":{}
            }