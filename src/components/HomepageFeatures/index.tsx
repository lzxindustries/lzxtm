import clsx from 'clsx';
import Heading from '@theme/Heading';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  description: string;
  link: string;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Guides',
    description: 'Learn video synthesis fundamentals, patch your first system, and understand the standards behind analog video.',
    link: '/docs/guides/what-is-a-video-synthesizer',
  },
  {
    title: 'Instruments',
    description: 'Standalone video synthesis instruments — Videomancer, Chromagnon, and more.',
    link: '/docs/category/videomancer',
  },
  {
    title: 'Modules',
    description: 'EuroRack modules for modular video synthesis across Gen3, P-Series, and legacy product lines.',
    link: '/docs/modules/module-list',
  },
  {
    title: 'Blog',
    description: 'Development updates, artist features, firmware releases, and the story behind the builds.',
    link: '/blog',
  },
];

function Feature({ title, description, link }: FeatureItem) {
  return (
    <div className={clsx('col col--3')}>
      <Link to={link} className={styles.featureCard}>
        <div className={styles.featureContent}>
          <Heading as="h3" className={styles.featureTitle}>{title}</Heading>
          <p className={styles.featureDescription}>{description}</p>
        </div>
      </Link>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
