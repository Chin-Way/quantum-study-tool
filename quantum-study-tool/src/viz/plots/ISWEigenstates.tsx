import { useMemo, useState } from 'react';
import Plot from 'react-plotly.js';
import type { Data, Layout } from 'plotly.js';

/**
 * Infinite square well eigenstates.
 *
 * For a well of width a, the stationary states are
 *
 *   psi_n(x) = sqrt(2/a) * sin(n*pi*x/a),   0 < x < a,
 *
 * with probability density |psi_n(x)|^2. We work in natural units (a = 1) and
 * let the reader sweep the quantum number n with a slider. The state has n - 1
 * interior nodes, and its energy grows as n^2.
 */

const A = 1; // well width (natural units)
const SAMPLES = 240; // x-resolution of each curve
const N_MIN = 1;
const N_MAX = 6;

const PSI_COLOR = '#4f46e5'; // matches the app accent
const DENSITY_COLOR = '#b42318';

/** Sample psi_n and |psi_n|^2 across the well [0, a]. */
function eigenstate(n: number) {
  const x: number[] = [];
  const psi: number[] = [];
  const density: number[] = [];
  const amplitude = Math.sqrt(2 / A);

  for (let i = 0; i <= SAMPLES; i++) {
    const xi = (A * i) / SAMPLES;
    const value = amplitude * Math.sin((n * Math.PI * xi) / A);
    x.push(xi);
    psi.push(value);
    density.push(value * value);
  }

  return { x, psi, density };
}

export default function ISWEigenstates() {
  const [n, setN] = useState(N_MIN);
  const { x, psi, density } = useMemo(() => eigenstate(n), [n]);
  const nodes = n - 1;

  const data: Data[] = [
    {
      x,
      y: psi,
      type: 'scatter',
      mode: 'lines',
      name: 'ψₙ(x)',
      line: { color: PSI_COLOR, width: 2.5 },
      hovertemplate: 'x = %{x:.3f}<br>ψ = %{y:.3f}<extra></extra>',
    },
    {
      x,
      y: density,
      type: 'scatter',
      mode: 'lines',
      name: '|ψₙ(x)|²',
      line: { color: DENSITY_COLOR, width: 2.5 },
      fill: 'tozeroy',
      fillcolor: 'rgba(180, 35, 24, 0.08)',
      hovertemplate: 'x = %{x:.3f}<br>|ψ|² = %{y:.3f}<extra></extra>',
    },
  ];

  const layout: Partial<Layout> = {
    height: 380,
    margin: { l: 50, r: 20, t: 34, b: 46 },
    xaxis: { title: { text: 'x / a' }, range: [0, A], zeroline: false },
    yaxis: { title: { text: 'amplitude' }, zeroline: true, zerolinecolor: '#c8cdd8' },
    legend: { orientation: 'h', x: 0, y: 1.18, yanchor: 'bottom' },
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
        <label htmlFor="isw-n">
          Quantum number&nbsp;<strong>n = {n}</strong>
        </label>
        <input
          id="isw-n"
          type="range"
          min={N_MIN}
          max={N_MAX}
          step={1}
          value={n}
          onChange={(e) => setN(Number(e.target.value))}
        />
        <span className="viz-hint">
          {nodes} interior node{nodes === 1 ? '' : 's'}
        </span>
      </div>

      <figcaption className="viz-caption">
        Eigenstates of the infinite square well, ψₙ(x) = √(2/a)·sin(nπx/a), in
        natural units (a = 1). Drag the slider to change n: the wavefunction gains
        an interior node with each step, while the energy grows as n².
      </figcaption>
    </figure>
  );
}
