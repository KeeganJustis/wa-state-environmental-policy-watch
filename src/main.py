import get_news



def main():
    news_sites = get_news.get_news_sites("plastics washington state legislature", "2025-01-01")
    get_news.save_news_sites(news_sites)
    get_news.get_urls(news_sites)
if __name__ == "__main__":
    main()
