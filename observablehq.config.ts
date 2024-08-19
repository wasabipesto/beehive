// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: 'wasabipesto.com',
  pages: [
    {
      name: 'Personal',
      pages: [
        { name: 'Blogroll', path: '/blogroll/' },
        { name: 'Hardware', path: '/hardware/' },
        { name: 'Software', path: '/software/' },
        { name: 'Media', path: '/media/' }
      ]
    },
    {
      name: 'Other',
      pages: [
        { name: 'Plex', path: '/plex/' },
        { name: 'Genesis 3:1', path: '/genesis/' },
        { name: 'Nice Numbers', path: '/nice/' },
        { name: 'Outer Wilds', path: '/outer-wilds/' },
        { name: 'Thermistors', path: '/thermistors/' }
      ]
    }
  ],
  // Some additional configuration options and their defaults:
  theme: 'coffee', // https://observablehq.com/framework/themes
  head: `<link rel="icon" type="image/png" href="/homepage/crows.40x40.png"><link rel="alternate" type="application/rss+xml" title="RSS" href="/_file/assets/feed/rss.xml" />`,
  header: '', // what to show in the header (HTML)
  footer: '', // what to show in the footer (HTML)
  toc: true, // whether to show the table of contents
  pager: false, // whether to show previous & next links in the footer
  root: 'src' // path to the source root for preview
  // output: "dist", // path to the output root for build
  // search: true, // whether to enable search on the project
}
