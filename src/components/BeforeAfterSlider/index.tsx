import React, { useState, useRef, useCallback } from 'react';
import styles from './styles.module.css';

interface Source {
  label: string;
  before: string;
  after: string;
}

interface BeforeAfterSliderProps {
  sources: Source[];
  caption?: string;
}

export default function BeforeAfterSlider({
  sources,
  caption,
}: BeforeAfterSliderProps): JSX.Element | null {
  const [activeTab, setActiveTab] = useState(0);
  const [sliderPos, setSliderPos] = useState(50);
  const containerRef = useRef<HTMLDivElement>(null);
  const dragging = useRef(false);

  const updatePos = useCallback((clientX: number) => {
    const el = containerRef.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const pct = ((clientX - rect.left) / rect.width) * 100;
    setSliderPos(Math.max(2, Math.min(98, pct)));
  }, []);

  const onPointerDown = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      dragging.current = true;
      containerRef.current?.setPointerCapture(e.pointerId);
      updatePos(e.clientX);
    },
    [updatePos],
  );

  const onPointerMove = useCallback(
    (e: React.PointerEvent<HTMLDivElement>) => {
      if (!dragging.current) return;
      updatePos(e.clientX);
    },
    [updatePos],
  );

  const onPointerUp = useCallback(() => {
    dragging.current = false;
  }, []);

  if (!sources || sources.length === 0) return null;
  const active = sources[activeTab] ?? sources[0];

  return (
    <div className={styles.wrapper}>
      {sources.length > 1 && (
        <div className={styles.tabs} role="tablist">
          {sources.map((s, i) => (
            <button
              key={i}
              role="tab"
              aria-selected={i === activeTab}
              className={`${styles.tab} ${i === activeTab ? styles.tabActive : ''}`}
              onClick={() => setActiveTab(i)}
              type="button"
            >
              {s.label}
            </button>
          ))}
        </div>
      )}
      <div
        ref={containerRef}
        className={`${styles.container} ${sources.length <= 1 ? styles.containerNoTabs : ''}`}
        onPointerDown={onPointerDown}
        onPointerMove={onPointerMove}
        onPointerUp={onPointerUp}
        onPointerCancel={onPointerUp}
      >
        {/* After (processed) — base layer */}
        <img
          src={active.after}
          className={styles.image}
          alt="Processed"
          draggable={false}
        />
        {/* Before (source) — clipped overlay */}
        <div
          className={styles.beforeOverlay}
          style={{ clipPath: `inset(0 ${100 - sliderPos}% 0 0)` }}
        >
          <img
            src={active.before}
            className={styles.image}
            alt="Source"
            draggable={false}
          />
        </div>
        {/* Divider line + handle */}
        <div className={styles.divider} style={{ left: `${sliderPos}%` }}>
          <div className={styles.handle}>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M7 4 3 10 7 16" />
              <path d="M13 4 17 10 13 16" />
            </svg>
          </div>
        </div>
        {/* Labels */}
        <span
          className={`${styles.label} ${styles.labelBefore}`}
          style={{ opacity: sliderPos > 12 ? 1 : 0 }}
        >
          Source
        </span>
        <span
          className={`${styles.label} ${styles.labelAfter}`}
          style={{ opacity: sliderPos < 88 ? 1 : 0 }}
        >
          Processed
        </span>
      </div>
      {caption && <em className={styles.caption}>{caption}</em>}
    </div>
  );
}
