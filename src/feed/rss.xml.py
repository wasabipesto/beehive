import tomllib
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

rss_cfg_file = "src/feed/rss_cfg.toml"
with open(rss_cfg_file, "rb") as file:
    rss_cfg = tomllib.load(file)

fg = FeedGenerator()
fg.title(rss_cfg["title"])
fg.link(href=rss_cfg["link"])
fg.description(rss_cfg["description"])

for item in rss_cfg["entries"]:
    fe = fg.add_entry()
    fe.title(item["title"])
    fe.published(
        datetime.combine(item["date"], datetime.min.time(), tzinfo=timezone.utc)
    )
    fe.guid(item["link"])
    fe.description(item["summary"])

rss_feed_str = fg.rss_str(pretty=True).decode("utf-8")
print(rss_feed_str)
