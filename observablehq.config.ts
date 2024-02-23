// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "wasabipesto.com",
  pages: [
    {
      name: "About",
      pages: [
        {name: "Hardware", path: "/hardware"},
        {name: "Software", path: "/software"},
        {name: "Blogroll", path: "/blogroll"},
        {name: "Cats", path: "/cats"},
      ]
    }
  ],
  // Some additional configuration options and their defaults:
  theme: "coffee", // https://observablehq.com/framework/themes
  head: `<link rel="icon" type="image/png" href="_file/assets/crows.40x40.png">`,
  header: "", // what to show in the header (HTML)
  footer: "", // what to show in the footer (HTML)
  toc: true, // whether to show the table of contents
  pager: false, // whether to show previous & next links in the footer
  // root: "docs", // path to the source root for preview
  // output: "dist", // path to the output root for build
};
