import src.mvc.control as control
import src.services.server as server
import asyncio

"""
CHECK README.md file! :)
"""

if __name__ == "__main__":
    ibn_run = control.IBNControl()
    asyncio.run(server.main())