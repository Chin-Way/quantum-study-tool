import ReactMarkdown from 'react-markdown';
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
 */
export default function Markdown({ children }: { children: string }) {
  return (
    <div className="markdown">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeMathjax]}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
