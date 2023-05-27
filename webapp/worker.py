from worker.predict_job import main
import logging
import asyncio


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
