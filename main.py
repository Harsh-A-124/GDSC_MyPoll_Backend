from os import getenv
import uvicorn

if __name__ == "__main__":
    port = int(getenv("PORT",8000))
    uvicorn.run("GDSC_MyPoll_Backend_API:app", host="0.0.0.0", port=port, reload=True)