import get_news



def main():
    news_sites = get_news.get_news_sites("bitcoin", "2024-01-01")
    get_news.save_news_sites(news_sites)

if __name__ == "__main__":
    main()
