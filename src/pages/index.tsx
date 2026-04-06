import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

const showcaseItems = [
  { program: 'perlin', image: '/img/instruments/videomancer/perlin/perlin_hero_s4.png', label: 'Perlin' },
  { program: 'moire', image: '/img/instruments/videomancer/moire/moire_hero_s2.png', label: 'Moiré' },
  { program: 'delirium', image: '/img/instruments/videomancer/delirium/delirium_hero_s1.png', label: 'Delirium' },
  { program: 'kintsugi', image: '/img/instruments/videomancer/kintsugi/kintsugi_hero_s1.png', label: 'Kintsugi' },
  { program: 'glorious', image: '/img/instruments/videomancer/glorious/glorious_hero_s1.png', label: 'Glorious' },
  { program: 'corollas', image: '/img/instruments/videomancer/corollas/corollas_hero_s1.png', label: 'Corollas' },
  { program: 'elastica', image: '/img/instruments/videomancer/elastica/elastica_hero_s1.png', label: 'Elastica' },
  { program: 'shadebob', image: '/img/instruments/videomancer/shadebob/shadebob_hero_s1.png', label: 'Shadebob' },
  { program: 'mycelium', image: '/img/instruments/videomancer/mycelium/mycelium_hero_s1.png', label: 'Mycelium' },
  { program: 'faultplane', image: '/img/instruments/videomancer/faultplane/faultplane_hero_s1.png', label: 'Faultplane' },
  { program: 'howler', image: '/img/instruments/videomancer/howler/howler_hero_s1.png', label: 'Howler' },
  { program: 'sabattier', image: '/img/instruments/videomancer/sabattier/sabattier_hero_s1.png', label: 'Sabattier' },
];

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/guides/your-first-patch">
            Get Started
          </Link>
          <Link
            className="button button--outline button--secondary button--lg"
            to="/docs/modules/module-list">
            Explore Modules
          </Link>
        </div>
      </div>
    </header>
  );
}

function VisualShowcase() {
  return (
    <section className={styles.showcase}>
      <div className="container">
        <Heading as="h2" className={styles.showcaseHeading}>
          Made with Videomancer
        </Heading>
        <p className={styles.showcaseSubtitle}>
          A standalone video synthesis instrument with 300+ programs for real-time visual processing and generation.
        </p>
        <div className={styles.showcaseGrid}>
          {showcaseItems.map((item) => (
            <Link
              key={item.program}
              to={`/docs/instruments/videomancer/${item.program}`}
              className={styles.showcaseItem}>
              <img
                src={item.image}
                alt={`${item.label} — Videomancer program output`}
                loading="lazy"
              />
              <span className={styles.showcaseLabel}>{item.label}</span>
            </Link>
          ))}
        </div>
        <div className={styles.showcaseCta}>
          <Link
            className="button button--secondary button--md"
            to="/docs/category/videomancer">
            Explore Videomancer
          </Link>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Creative tools for video synthesis and analog image processing.">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <VisualShowcase />
      </main>
    </Layout>
  );
}
