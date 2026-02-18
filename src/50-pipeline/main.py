import asyncio

from validate_fanout_class_pipeline import run_validation as run_fanout_class
from validate_fanout_concurrent_pipeline import run_validation as run_fanout_concurrent
from validate_fanout_sequential_pipeline import run_validation as run_fanout_sequential
from validate_sequential_class_pipeline import run_validation as run_sequential_class
from validate_sequential_function_pipeline import run_validation as run_sequential_function
from validate_stream_printing_pipeline import run_validation as run_stream_printing


async def main() -> None:
    print("=== Pipeline Validation Start ===")
    await run_sequential_function()
    print("PASS: function sequential pipeline")
    await run_fanout_concurrent()
    print("PASS: function fanout concurrent pipeline")
    await run_fanout_sequential()
    print("PASS: function fanout sequential pipeline")
    await run_sequential_class()
    print("PASS: class sequential pipeline")
    await run_fanout_class()
    print("PASS: class fanout pipeline")
    await run_stream_printing()
    print("PASS: stream printing pipeline")
    print("=== ALL PIPELINE VALIDATIONS PASSED ===")


if __name__ == "__main__":
    asyncio.run(main())
