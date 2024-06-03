import os
import sys
import frontmatter
from markdown2 import markdown
from feedgen.feed import FeedGenerator

markdown_folder = "/opt/beehive/src/feed"
output_folder = sys.argv[1]

fg = FeedGenerator()
fg.title("wasabipesto")
fg.link(href="https://wasabipesto.com")
fg.description("Infrequent updates about the site and my other projects.")

for file_name in os.listdir(markdown_folder):
    if file_name.endswith(".md"):
        post = frontmatter.load(os.path.join(markdown_folder, file_name))
        fe = fg.add_entry()
        fe.guid("https://wasabipesto.com/dev/null/" + post["date"].isoformat())
        fe.title(post["title"])
        fe.published(post["date"].isoformat() + "T00:00:00Z")
        fe.description(markdown(post.content))

fg.rss_file(os.path.join(output_folder, "rss.xml"), pretty=True)
# fg.atom_file(os.path.join(output_folder, "atom.xml"), pretty=True)
