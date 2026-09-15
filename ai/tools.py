from product_normalizer.repository import get_run,get_runs,get_run_issues

def get_run_detail_tool(run_id:int):
    row=get_run(run_id)
    return row

def get_runs_tool(limit:int):
    rows=get_runs(limit)
    return rows

def get_run_issues_tool(run_id:int):
    issues=get_run_issues(run_id)
    return issues
