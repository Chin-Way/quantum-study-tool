import { useMemo, useState } from 'react';
import Plot from 'react-plotly.js';
import type { Data, Layout, Shape } from 'plotly.js';

/**
 * Quantum harmonic oscillator eigenstates.
 *
 * In natural units (m = omega = hbar = 1) the stationary states are
 *
 *   psi_n(x) = pi^(-1/4) / sqrt(2^n n!) * H_n(x) * exp(-x^2 / 2),
 *
 * with energies E_n = n + 1/2 and exactly n nodes. We draw the parabolic
 * potential V(x) = x^2 / 2, the energy ladder E_n, and the selected
 * eigenfunction psi_n offset to sit at its own energy level -- the canonical
 * textbook picture -- with a slider for n = 0..6.
 */

const X_MAX = 5;
const SAMPLES = 400;
const N_MIN = 0;
const N_MAX = 6;
const PSI_SCALE = 1.2; // vertical exaggeration so psi_n is visible at its level

const POTENTIAL_COLOR = '#9aa3b2';
const LEVEL_COLOR = '#c8cdd8';
const PSI_COLOR = '#4f46e5';

/** Physicists' Hermite polynomial H_n(x) via the standard recurrence. */
function hermite(n: number, x: number): number {
  if (n === 0) return 1;
  let hPrev = 1;
  let h = 2 * x;
  for (let k = 1; k < n; k++) {
    const hNext = 2 * x * h - 2 * k * hPrev;
    hPrev = h;
    h = hNext;
  }
  return h;
}

/** Normalization constant pi^(-1/4) / sqrt(2^n n!). */
function normalization(n: number): number {
  let twoPowNFactorial = 1; // product of 2k for k = 1..n  ==  2^n * n!
  for (let k = 1; k <= n; k++) twoPowNFactorial *= 2 * k;
  return Math.PI ** -0.25 / Math.sqrt(twoPowNFactorial);
}

/** Sample psi_n across [-X_MAX, X_MAX]. */
function eigenstate(n: number) {
  const norm = normalization(n);
  const x: number[] = [];
  const psi: number[] = [];
  for (let i = 0; i <= SAMPLES; i++) {
    const xi = -X_MAX + (2 * X_MAX * i) / SAMPLES;
    x.push(xi);
    psi.push(norm * hermite(n, xi) * Math.exp(-(xi * xi) / 2));
  }
  return { x, psi };
}

const energy = (n: number) => n + 0.5;
const turningPoint = (n: number) => Math.min(Math.sqrt(2 * energy(n)), X_MAX);

export default function QHOEigenstates() {
  const [n, setN] = useState(N_MIN);
  const { x, psi } = useMemo(() => eigenstate(n), [n]);
  const En = energy(n);

  // Parabolic potential V(x) = x^2 / 2 (fixed, so memoize once).
  const potential = useMemo(() => {
    const xs: number[] = [];
    const ys: number[] = [];
    for (let i = 0; i <= SAMPLES; i++) {
      const xi = -X_MAX + (2 * X_MAX * i) / SAMPLES;
      xs.push(xi);
      ys.push((xi * xi) / 2);
    }
    return { xs, ys };
  }, []);

  // Energy ladder: a horizontal line at each E_n spanning its classical region.
  const levels: Partial<Shape>[] = [];
  for (let k = N_MIN; k <= N_MAX; k++) {
    const xt = turningPoint(k);
    const selected = k === n;
    levels.push({
      type: 'line',
      xref: 'x',
      yref: 'y',
      x0: -xt,
      x1: xt,
      y0: energy(k),
      y1: energy(k),
      line: {
        color: selected ? PSI_COLOR : LEVEL_COLOR,
        width: selected ? 2 : 1,
        dash: selected ? 'solid' : 'dot',
      },
      layer: 'below',
    });
  }

  const data: Data[] = [
    {
      x: potential.xs,
      y: potential.ys,
      type: 'scatter',
      mode: 'lines',
      name: 'V(x) = x²/2',
      line: { color: POTENTIAL_COLOR, width: 2 },
      hoverinfo: 'skip',
    },
    {
      x,
      y: psi.map((p) => En + PSI_SCALE * p),
      type: 'scatter',
      mode: 'lines',
      name: 'ψₙ(x) at Eₙ',
      line: { color: PSI_COLOR, width: 2.5 },
      hovertemplate: 'x = %{x:.2f}<extra></extra>',
    },
  ];

  const layout: Partial<Layout> = {
    height: 400,
    margin: { l: 52, r: 20, t: 34, b: 46 },
    xaxis: { title: { text: 'x' }, range: [-X_MAX, X_MAX], zeroline: false },
    yaxis: { title: { text: 'energy / ℏω' }, range: [-0.6, N_MAX + 1.8], zeroline: false },
    shapes: levels,
    legend: { orientation: 'h', x: 0, y: 1.16, yanchor: 'bottom' },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif', color: '#1c2230', size: 13 },
  };

  return (
    <figure className="viz-figure">
      <Plot
        data={data}
        layout={layout}
        config={{ displayModeBar: false, responsive: true }}
        style={{ width: '100%' }}
        useResizeHandler
      />

      <div className="viz-controls">
        <label htmlFor="qho-n">
          Quantum number&nbsp;<strong>n = {n}</strong>
        </label>
        <input
          id="qho-n"
          type="range"
          min={N_MIN}
          max={N_MAX}
          step={1}
          value={n}
          onChange={(e) => setN(Number(e.target.value))}
        />
        <span className="viz-hint">
          Eₙ = {En.toFixed(1)} ℏω · {n} node{n === 1 ? '' : 's'}
        </span>
      </div>

      <figcaption className="viz-caption">
        Harmonic oscillator eigenstates ψₙ(x) drawn at their energy
        Eₙ = (n + ½)ℏω inside the potential V(x) = ½x² (natural units). Levels are
        evenly spaced by ℏω, and ψₙ has n nodes. Drag the slider to climb the
        ladder. The vertical scale of ψₙ is exaggerated for visibility.
      </figcaption>
    </figure>
  );
}
