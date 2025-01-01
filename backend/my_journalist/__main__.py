from my_journalist.database.crud import init_rss

if __name__ == "__main__":
    init_rss()
    import uvicorn
    uvicorn.run("my_journalist.app:app", host="0.0.0.0", port=8000, reload=True)