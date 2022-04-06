from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    from app.api.api_plants import plants_router
    app.include_router(plants_router)

    from app.api.api_water_sprinkler import water_sprinkler_router
    app.include_router(water_sprinkler_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
