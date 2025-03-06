import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const config: Config = {
  title: 'LZX Technical Manual',
  tagline: 'Documentation and resources for LZX Industries video synthesizers.',
  favicon: 'img/favicon.ico',
  // Set the production url of your site here
  url: 'https://docs.lzxindustries.net',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',
  trailingSlash: false,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'lzxindustries', // Usually your GitHub org/user name.
  projectName: 'lzxindustries.github.io', // Usually your repo name.
  deploymentBranch: 'main',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.24/dist/katex.min.css',
      type: 'text/css',
      integrity:
        'sha384-odtC+0UGzzFL/6PNoE8rX/SPcQDXBJ+uRepguP4QkPCm2LBxH3FA3y+fKSiJ+AmM',
      crossorigin: 'anonymous',
    },
  ],
  headTags: [
    {
      tagName: "link",
      attributes: {
        rel: "preload",
        href: "static/font/ReliefSingleLineOutline-Regular.woff2",
        as: "font",
        type: "font/woff2",
        crossorigin: "anonymous",
      },
    }],
  plugins: [
    'docusaurus-plugin-image-zoom'
  ],
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          // editUrl:
          //   'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          postsPerPage: 'ALL',
          blogSidebarTitle: 'All posts',
          blogSidebarCount: 'ALL',
          feedOptions: {
            type: 'all',
            copyright: `© ${new Date().getFullYear()} LZX`,
            createFeedItems: async (params) => {
              const {blogPosts, defaultCreateFeedItems, ...rest} = params;
              return defaultCreateFeedItems({
                // keep only the 10 most recent blog posts in the feed
                blogPosts: blogPosts.filter((item, index) => index < 10),
                ...rest,
              });
            },
          },
        // Please change this to your repo.
        // Remove this to remove the "edit this page" links.
        // editUrl:
        //   'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],
  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],
  themeConfig: {
    colorMode: {
      defaultMode: 'light',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
    mermaid: {
      // theme: { light: 'neutral', dark: 'forest' },
      options: {
        maxTextSize: 1024,
      },
    },
    zoom: {
      selector: '.markdown > img',
      background: {
        light: 'rgb(255, 255, 255)',
        dark: 'rgb(50, 50, 50)'
      },
      config: {
        // options you can specify via https://github.com/francoischalifour/medium-zoom#usage
        // container: '.main-wrapper'
      }
    },
    // blog: false,
    // Replace with your project's social card
    image: 'img/social-card.jpg',
    navbar: {
      title: 'Technical Manual',
      logo: {
        alt: 'LZX Industries',
        src: 'img/logo.svg',
      },
      items: [
        // {
        //   type: 'docSidebar',
        //   sidebarId: 'guidesSidebar',
        //   position: 'left',
        //   label: 'Guides',
        // },
        // {
        //   type: 'docSidebar',
        //   sidebarId: 'instrumentsSidebar',
        //   position: 'left',
        //   label: 'Instruments',
        // },
        {
          type: 'docSidebar',
          sidebarId: 'modulesSidebar',
          position: 'left',
          label: 'Modules',
        },
        // {
        //   type: 'docSidebar',
        //   sidebarId: 'caseAndPowerSidebar',
        //   position: 'left',
        //   label: 'Case & Power',
        // },
        // {to: '/docs/glossary', label: 'Glossary', position: 'left'},
        {to: '/blog', label: 'Blog', position: 'left'},
        // {
        //   href: 'https://github.com/lzxindustries',
        //   label: 'GitHub',
        //   position: 'right',
        // },
      ],
    },
    footer: {
      style: 'light',
      links: [
        // {
        //   title: 'Docs',
        //   items: [
        //     {
        //       label: 'Tutorial',
        //       to: '/docs/intro',
        //     },
        //   ],
        // },
        // {
        // title: 'Community',
        // items: [
        //   {
        //     label: 'Stack Overflow',
        //     href: 'https://stackoverflow.com/questions/tagged/docusaurus',
        //   },
        //   {
        //     label: 'Discord',
        //     href: 'https://discordapp.com/invite/docusaurus',
        //   },
        //   {
        //     label: 'Twitter',
        //     href: 'https://twitter.com/docusaurus',
        //   },
        // ],
        // },
        // {
        //   title: 'More',
        //   items: [
        //     {
        //       label: 'Blog',
        //       to: '/blog',
        //     },
        //     // {
        //     //   label: 'GitHub',
        //     //   href: 'https://github.com/facebook/docusaurus',
        //     // },
        //   ],
        // },
      ],
      copyright: `© ${new Date().getFullYear()} LZX`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
