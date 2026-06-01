import { Link, useParams } from 'react-router-dom';
import type { Topic } from '../types';
import { getAdjacentTopics, getTopic } from '../content/loader';
import { extractHeadings } from '../content/toc';
import Markdown from './Markdown';
import ProblemCard from './ProblemCard';
import VizHost from '../viz/VizHost';

function scrollToSection(slug: string) {
  document.getElementById(slug)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

export default function TopicPage() {
  const { id } = useParams();
  const topic = id ? getTopic(id) : undefined;

  if (!topic) {
    return (
      <div>
        <p>Topic not found.</p>
        <Link to="/" className="back">← All topics</Link>
      </div>
    );
  }

  const headings = extractHeadings(topic.notes);
  const { prev, next } = getAdjacentTopics(topic.id);

  // Resolve related topic ids to topics, silently dropping any unknown ids.
  const related = (topic.related ?? [])
    .map((relatedId) => getTopic(relatedId))
    .filter((t): t is Topic => Boolean(t));

  return (
    <article>
      <Link to="/" className="back">← All topics</Link>
      <h1>{topic.title}</h1>
      {topic.book && (
        <p className="topic-book">
          {topic.book}
          {topic.chapter ? ` · ${topic.chapter}` : ''}
        </p>
      )}

      {headings.length > 1 && (
        <nav className="toc" aria-label="Table of contents">
          <span className="toc-title">Contents</span>
          <ul>
            {headings.map((h) => (
              <li key={h.slug} className={`toc-item toc-depth-${h.depth}`}>
                <button type="button" className="toc-link" onClick={() => scrollToSection(h.slug)}>
                  {h.text}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      )}

      <section className="notes">
        <Markdown>{topic.notes}</Markdown>
      </section>

      {topic.viz && (
        <section className="topic-viz">
          <h2>Interactive</h2>
          <VizHost id={topic.viz} />
        </section>
      )}

      {topic.problems.length > 0 && (
        <section className="problems">
          <h2>Problems</h2>
          {topic.problems.map((p, i) => (
            <ProblemCard key={p.id} problem={p} index={i} />
          ))}
        </section>
      )}

      {related.length > 0 && (
        <section className="related">
          <h2>Related topics</h2>
          <ul className="related-list">
            {related.map((t) => (
              <li key={t.id} className="related-item">
                <Link to={`/topic/${t.id}`} className="related-link">
                  {t.title}
                </Link>
                {t.summary && <span className="related-summary">{t.summary}</span>}
              </li>
            ))}
          </ul>
        </section>
      )}

      {(prev || next) && (
        <nav className="topic-nav" aria-label="Topic navigation">
          {prev ? (
            <Link to={`/topic/${prev.id}`} className="topic-nav-link topic-nav-prev">
              <span className="topic-nav-dir">← Previous</span>
              <span className="topic-nav-title">{prev.title}</span>
            </Link>
          ) : (
            <span className="topic-nav-spacer" />
          )}
          {next ? (
            <Link to={`/topic/${next.id}`} className="topic-nav-link topic-nav-next">
              <span className="topic-nav-dir">Next →</span>
              <span className="topic-nav-title">{next.title}</span>
            </Link>
          ) : (
            <span className="topic-nav-spacer" />
          )}
        </nav>
      )}
    </article>
  );
}
