import uvicorn
from fastapi import FastAPI


def init_app():
    lifespan = None

    app = FastAPI(title="FastAPI TODO server", lifespan=lifespan)
    from routes.authenticate import router as auth_router
    from routes.root import router as root_router
    from routes.todos import router as todo_router

    # Redirect router
    app.include_router(root_router)

    # routes authorization
    app.include_router(auth_router, prefix="/api", tags=["Authentication"])

    # routes todos
    app.include_router(todo_router, prefix="/api", tags=["ToDos"])

    return app


if __name__ == "__main__":
    fastapi_app = init_app()
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)
