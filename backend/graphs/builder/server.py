from fastapi import APIRouter, Response, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from .ServerTee import ServerTee
from .thread_handler import ThreadHandler
from .WorkFlow import run_workflow_as_server
from .FileTransmit import file_transmit_router

router = APIRouter()

# Initialize ServerTee and ThreadHandler
server_tee = ServerTee("server.log")
thread_handler = ThreadHandler.get_instance()

def server_func():
    try:
        run_workflow_as_server()
    except Exception as e:
        print(str(e))
        raise

@router.post("/run")
async def run_script():
    if thread_handler.is_running():
        raise HTTPException(status_code=409, detail="Another instance is already running")

    def generate():
        try:
            thread_handler.start_thread(target=server_func)
            yield from server_tee.stream_to_frontend()
        except Exception as e:
            print(str(e))
            yield {"error": str(e)}
        finally:
            if not thread_handler.is_running():
                yield {"message": "finished"}

    return StreamingResponse(generate(), media_type="text/plain")

@router.get("/status")
async def get_status():
    running = thread_handler.is_running()
    return {"running": running}


# Include the file transmit router
router.include_router(file_transmit_router, prefix="/file_transmit")