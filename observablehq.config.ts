// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the webpage titles.
  title: 'wasabipesto.com',
  // Used in the sidebar header.
  home: 'Home',
  // Defines the sidebar contents.
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
      name: 'HVAC',
      pages: [
        { name: 'The Old Schoolhouse', path: '/schoolhouse/' },
        { name: 'Life as a Controls Subcontractor', path: '/controls-life/' },
        { name: 'Thermistors', path: '/thermistors/' }
      ]
    },
    {
      name: 'Other',
      pages: [
        { name: 'Plex', path: '/plex/' },
        { name: 'Genesis 3:1', path: '/genesis/' },
        { name: 'Nice Numbers', path: '/nice/' },
        { name: 'Outer Wilds', path: '/outer-wilds/' },
      ]
    }
  ],
  // Some additional configuration options and their defaults:
  theme: 'coffee', // https://observablehq.com/framework/themes
  head: `<link rel="icon" type="image/png" href="/homepage/crows.40x40.png">`,
  header: '', // what to show in the header (HTML)
  footer: '', // what to show in the footer (HTML)
  toc: true, // whether to show the table of contents
  pager: false, // whether to show previous & next links in the footer
  root: 'src' // path to the source root for preview
  // output: "dist", // path to the output root for build
  // search: true, // whether to enable search on the project
}
