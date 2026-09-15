from ai.schemas import RunDetailArguments

print(RunDetailArguments.model_validate({"run_id": 6}))
print(RunDetailArguments.model_validate({"run_id": "6"}))
print(RunDetailArguments.model_json_schema())