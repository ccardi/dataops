import os
import pandas
import pandas_gbq

print('================ Start ==================')
test_variable = os.environ['TEST_VARIABLE']
project_id = "pod-fr-retail"
table_id = 'demo_supply_eu_test.panda'
location='EU'
print(test_variable)
df = pandas.DataFrame(
    {
        "my_string": [test_variable, "abc", "abc"],
        "my_int64": [1, 2, 3],
        "my_float64": [4.0, 5.0, 6.0],
        "my_bool1": [True, False, True],
        "my_bool2": [False, True, False],
        "my_dates": pandas.date_range("now", periods=3),
    }
)

pandas_gbq.to_gbq(df, table_id, project_id=project_id, location=location, if_exists='replace')
print('================ End ==================')
