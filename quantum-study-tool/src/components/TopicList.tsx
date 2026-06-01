import { Link } from 'react-router-dom';
import { topics } from '../content/loader';

export default function TopicList() {
  return (
    <div>
      <h1>Quantum Mechanics</h1>
      <p className="subtitle">A personal study tool. Pick a topic to begin.</p>

      <ul className="topic-list">
        {topics.map((t) => (
          <li key={t.id} className="topic-card">
            <Link to={`/topic/${t.id}`} className="topic-card-link">
              <span className="topic-title">{t.title}</span>
              {t.book && (
                <span className="topic-book">
                  {t.book}
                  {t.chapter ? ` · ${t.chapter}` : ''}
                </span>
              )}
            </Link>
            {t.summary && <p className="topic-summary">{t.summary}</p>}
          </li>
        ))}
      </ul>

      {topics.length === 0 && (
        <p className="empty">No topics yet. Add one under <code>content/</code>.</p>
      )}
    </div>
  );
}
