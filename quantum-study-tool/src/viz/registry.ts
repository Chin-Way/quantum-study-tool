import { lazy } from 'react';
import type { ComponentType, LazyExoticComponent } from 'react';

/**
 * Visualization registry: maps a string `id` (referenced from content via the
 * `viz` field) to a React component.
 *
 * Components are lazy-loaded so the heavy Plotly bundle is split into its own
 * chunk and only fetched when a plot is actually shown — pages with no
 * visualization never pay for it. Adding a new plot is two steps: drop a
 * component in ./plots, then add one line to the map below.
 */
export type Viz = LazyExoticComponent<ComponentType>;

export const vizRegistry: Record<string, Viz> = {
  'isw-eigenstates': lazy(() => import('./plots/ISWEigenstates')),
};

/** Look up a visualization component by id, or `undefined` if none is registered. */
export function getViz(id: string): Viz | undefined {
  return vizRegistry[id];
}
