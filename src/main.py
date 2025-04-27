import get_news
import analyze_news


def main():
    # find the start date as 3 months ago
    news_sites = get_news.get_news_sites("plastics washington state legislature", "2025-04-21")
    get_news.save_news_sites(news_sites)
    news_urls = get_news.get_urls(news_sites)
    final_summary = analyze_news.analyze_all_summaries(news_urls)
    print(final_summary)
    # analyze the news sites with lang
    # send out  summary of the news sites and summaries by email
if __name__ == "__main__":
    main()

