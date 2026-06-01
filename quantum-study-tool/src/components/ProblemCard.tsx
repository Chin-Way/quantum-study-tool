import { useState } from 'react';
import type { Problem } from '../types';
import Markdown from './Markdown';

export default function ProblemCard({ problem, index }: { problem: Problem; index: number }) {
  const [showSolution, setShowSolution] = useState(false);

  return (
    <div className="problem">
      <div className="problem-header">
        <span className="problem-number">Problem {index + 1}</span>
        {problem.difficulty && (
          <span className={`badge badge-${problem.difficulty}`}>{problem.difficulty}</span>
        )}
        {problem.source && <span className="problem-source">{problem.source}</span>}
      </div>

      <div className="problem-prompt">
        <Markdown>{problem.prompt}</Markdown>
      </div>

      <button
        type="button"
        className="toggle"
        aria-expanded={showSolution}
        onClick={() => setShowSolution((s) => !s)}
      >
        {showSolution ? 'Hide solution' : 'Show solution'}
      </button>

      {showSolution && (
        <div className="solution">
          <Markdown>{problem.solution}</Markdown>
        </div>
      )}
    </div>
  );
}
