import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { getBookSections } from '../content/loader';
import { filterOptions, searchTopics } from '../content/search';

export default function TopicList() {
  const [query, setQuery] = useState('');
  const [book, setBook] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [tag, setTag] = useState('');

  const options = useMemo(() => filterOptions(), []);
  const isFiltering = query.trim() !== '' || book !== '' || difficulty !== '' || tag !== '';

  const matchIds = useMemo(
    () => searchTopics({ query, book, difficulty, tag }),
    [query, book, difficulty, tag],
  );

  // Keep the book-sectioned layout, but drop non-matching topics and empty books.
  const sections = useMemo(
    () =>
      getBookSections()
        .map((s) => ({ ...s, topics: s.topics.filter((t) => matchIds.has(t.id)) }))
        .filter((s) => s.topics.length > 0),
    [matchIds],
  );
  const total = sections.reduce((n, s) => n + s.topics.length, 0);

  const clear = () => {
    setQuery('');
    setBook('');
    setDifficulty('');
    setTag('');
  };

  return (
    <div>
      <h1>Quantum Mechanics</h1>
      <p className="subtitle">A personal study tool. Pick a topic to begin.</p>

      <div className="search">
        <input
          type="search"
          className="search-input"
          placeholder="Search topics and problems…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Search topics and problems"
        />
        <div className="search-filters">
          <select value={book} onChange={(e) => setBook(e.target.value)} aria-label="Filter by book">
            <option value="">All books</option>
            {options.books.map((b) => (
              <option key={b} value={b}>{b}</option>
            ))}
          </select>
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            aria-label="Filter by difficulty"
          >
            <option value="">Any difficulty</option>
            {options.difficulties.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
          <select value={tag} onChange={(e) => setTag(e.target.value)} aria-label="Filter by tag">
            <option value="">Any tag</option>
            {options.tags.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
          {isFiltering && (
            <button type="button" className="search-clear" onClick={clear}>
              Clear
            </button>
          )}
        </div>
        {isFiltering && (
          <p className="search-count">
            {total} topic{total === 1 ? '' : 's'} match
          </p>
        )}
      </div>

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
        <p className="empty">
          {isFiltering ? (
            'No topics match your search.'
          ) : (
            <>No topics yet. Add one under <code>content/</code>.</>
          )}
        </p>
      )}
    </div>
  );
}
