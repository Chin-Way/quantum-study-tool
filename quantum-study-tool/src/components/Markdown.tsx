import ReactMarkdown from 'react-markdown';
import type { Components } from 'react-markdown';
import { Link } from 'react-router-dom';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeMathjax from 'rehype-mathjax/svg';

/**
 * Renders a Markdown-plus-LaTeX string. Every piece of content in the app —
 * topic notes, problem prompts, and solutions — goes through this one component,
 * so math is typeset identically everywhere.
 *
 *   $...$   inline math
 *   $$...$$ display math
 *
 * MathJax renders to self-contained SVG, so no fonts or CDN scripts are needed.
 *
 * Links are routed through React Router: a Markdown link to an in-app hash route
 * (e.g. [text](#/topic/harmonic-oscillator)) becomes a client-side <Link>, so
 * cross-references between topics navigate without a full page reload. External
 * http(s) links open in a new tab.
 */
const components: Components = {
  a({ href, children, node: _node, ...rest }) {
    const url = href ?? '';
    if (url.startsWith('#/')) {
      // In-app hash route: strip the leading '#' so React Router sees a path.
      return <Link to={url.slice(1)}>{children}</Link>;
    }
    if (/^https?:\/\//i.test(url)) {
      return (
        <a href={url} target="_blank" rel="noreferrer" {...rest}>
          {children}
        </a>
      );
    }
    return (
      <a href={url} {...rest}>
        {children}
      </a>
    );
  },
};

export default function Markdown({ children }: { children: string }) {
  return (
    <div className="markdown">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeMathjax]}
        components={components}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
