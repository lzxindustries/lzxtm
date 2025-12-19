# LZX Technical Manual

[![Deploy to GitHub Pages](https://github.com/lzxindustries/lzxtm/actions/workflows/deploy.yml/badge.svg)](https://github.com/lzxindustries/lzxtm/actions/workflows/deploy.yml)

Official documentation site for LZX Industries video synthesizer products. Documents modular video synthesis hardware including modules, instruments, cases, and power supplies across multiple product generations.

**Live Site:** https://docs.lzxindustries.net

## About

This documentation site covers:
- **Guides** - Getting started with video synthesis, troubleshooting, and standards
- **Modules** - Individual module documentation (DSG3, ESG3, SMX3, etc.)
- **Instruments** - Complete instrument docs (Chromagnon, Vidiot, Videomancer)
- **Case & Power** - Power systems and enclosure documentation
- **Blog** - Development updates and announcements

## Technology Stack

- **Framework:** [Docusaurus 3.x](https://docusaurus.io/)
- **Language:** TypeScript
- **Deployment:** GitHub Pages (automated via GitHub Actions)
- **Features:** Mermaid diagrams, KaTeX math, image zoom, Draw.io integration

## Local Development

### Prerequisites

- Node.js 20 or higher
- npm (comes with Node.js)

### Installation

```bash
npm install
```

### Development Server

```bash
npm start
```

This starts a local development server at `http://localhost:3000` with live reload. Most changes are reflected immediately without restarting.

### Build

```bash
npm run build
```

Generates static content into the `build` directory for production deployment.

### Preview Production Build

```bash
npm run serve
```

Serves the production build locally for testing.

### Type Checking

```bash
npm run typecheck
```

Validates TypeScript types across the project.

## Deployment

### Automated (Recommended)

The site automatically deploys to GitHub Pages on every push to the `main` branch via GitHub Actions.

View deployment status: [Actions](https://github.com/lzxindustries/lzxtm/actions)

### Manual Deployment

For manual deployment from Windows:

```powershell
.\deploy.ps1
```

This script sets the required environment variables and runs the Docusaurus deploy command.

## Project Structure

```
lzxtm/
├── docs/                    # Documentation content
│   ├── guides/             # User guides
│   ├── modules/            # Module documentation
│   ├── instruments/        # Instrument documentation
│   └── case-and-power/     # Power and case docs
├── blog/                    # Blog posts (YYYY-MM-DD-slug format)
├── static/                  # Static assets
│   ├── firmware/           # Firmware binaries
│   ├── pdf/                # PDF documentation
│   ├── zip/                # Downloadable apps and files
│   └── img/                # Images
├── src/                     # React components and pages
├── .github/                 # GitHub Actions workflows
│   ├── workflows/          
│   │   └── deploy.yml      # Automated deployment
│   └── copilot-instructions.md  # AI coding agent guidelines
├── docusaurus.config.ts    # Site configuration
└── sidebars.ts             # Sidebar configuration (auto-generated)
```

## Contributing

### Adding Module Documentation

1. Create `docs/modules/{module-code}.md` with frontmatter
2. Add images to `/static/img/modules/{module-code}/{module-code}-diagrams/`
3. Update the module spec table in `docs/modules/module-list.md`
4. Set `draft: false` when documentation is complete

### Adding Blog Posts

1. Create folder: `blog/YYYY-MM-DD-slug-name/index.md`
2. Set frontmatter: `slug`, `title`, `authors`, `tags`
3. Add `<!--truncate-->` after the intro paragraph
4. Place images alongside or reference `/static/` paths

### File Naming Conventions

- **Module images:** `{module-code}_description.png` (lowercase, underscores)
- **Firmware:** `{module}_{version}/{module}_{version}.bin`
- **Apps:** `{app-name}-{platform}-portable.zip`

See [.github/copilot-instructions.md](.github/copilot-instructions.md) for comprehensive development guidelines.

## License

© 2025 LZX Industries. All rights reserved.

## Support

For questions about LZX products, visit [lzxindustries.net](https://lzxindustries.net) or contact support through the official channels.
