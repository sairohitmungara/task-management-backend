from fastapi.middleware.gzip import GZipMiddleware

def add_gzip(app):
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    