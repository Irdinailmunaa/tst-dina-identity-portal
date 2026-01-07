# Add this after the imports and before @app routes

from fastapi.middleware.cors import CORSMiddleware

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://irdinailmunaa.github.io",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
