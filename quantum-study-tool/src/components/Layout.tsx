import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="app">
      <header className="app-header">
        <Link to="/" className="brand">
          <span className="brand-mark">Ψ</span> Quantum Study
        </Link>
      </header>
      <main className="container">{children}</main>
      <footer className="app-footer">
        Personal study tool · add topics by dropping a folder in <code>content/</code>
      </footer>
    </div>
  );
}
