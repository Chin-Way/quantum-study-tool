import { Suspense } from 'react';
import { getViz } from './registry';

/**
 * Renders the visualization registered under `id`.
 *
 * Unknown ids degrade gracefully to a small inline notice instead of crashing
 * the page, so a typo in a content file never takes down a whole topic. The
 * registered component is loaded lazily, so we wrap it in <Suspense>.
 */
export default function VizHost({ id }: { id: string }) {
  const Viz = getViz(id);

  if (!Viz) {
    return (
      <div className="viz-fallback" role="note">
        No visualization is registered for <code>{id}</code>.
      </div>
    );
  }

  return (
    <div className="viz">
      <Suspense fallback={<div className="viz-loading">Loading visualization…</div>}>
        <Viz />
      </Suspense>
    </div>
  );
}
