import { Link } from 'react-router-dom';
import { getBookSections } from '../content/loader';

export default function TopicList() {
  const sections = getBookSections();

  return (
    <div>
      <h1>Quantum Mechanics</h1>
      <p className="subtitle">A personal study tool. Pick a topic to begin.</p>

      {sections.map((section) => (
        <section key={section.book} className="book-section">
          <header className="book-header">
            <h2 className="book-title">{section.book}</h2>
            {section.levels.length > 0 && (
              <span className="book-level">{section.levels.join(' · ')}</span>
            )}
          </header>

          <ul className="topic-list">
            {section.topics.map((t) => (
              <li key={t.id} className="topic-card">
                <Link to={`/topic/${t.id}`} className="topic-card-link">
                  <span className="topic-title">{t.title}</span>
                  {t.chapter && <span className="topic-book">{t.chapter}</span>}
                </Link>
                {t.summary && <p className="topic-summary">{t.summary}</p>}
              </li>
            ))}
          </ul>
        </section>
      ))}

      {sections.length === 0 && (
        <p className="empty">No topics yet. Add one under <code>content/</code>.</p>
      )}
    </div>
  );
}
