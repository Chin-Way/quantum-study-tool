import { Link, useParams } from 'react-router-dom';
import { getTopic } from '../content/loader';
import Markdown from './Markdown';
import ProblemCard from './ProblemCard';
import VizHost from '../viz/VizHost';

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
    </article>
  );
}
