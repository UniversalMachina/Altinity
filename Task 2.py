# from testflows.core import TestScenario, Given, When, Then, Module, main
# from testflows.asserts import error
# import subprocess
#
#
# try:
#     result = subprocess.run("clickhouse-client --query='SELECT 1'", shell=True, capture_output=True, text=True)
#     output = result.stdout.strip()
#     print(output)
# except Exception as e:
#     raise error(f"Error executing command: {e}")

from testflows.core import TestScenario, Given, When, Then, Module, main
from testflows.asserts import error
import subprocess

@TestScenario
def check_select_1_query(self):
    """Check that SELECT 1 query returns 1."""
    with Given("I have clickhouse-client installed"):
        try:
            result = subprocess.run("clickhouse-client --query='SELECT 1'", shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
        except Exception as e:
            raise error(f"Error executing command: {e}")

        with Then("the output should be '1'"):
            assert output == "1", error(f"Expected output: '1', got: '{output}'")

with Module("Test SELECT 1 query in ClickHouse"):
    check_select_1_query()

if __name__ == "__main__":
    main()