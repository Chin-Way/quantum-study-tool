import { useState } from 'react';
import type { Problem } from '../types';
import Markdown from './Markdown';
import VizHost from '../viz/VizHost';
import { toggleSolved, useSolved } from '../progress';

export default function ProblemCard({ problem, index }: { problem: Problem; index: number }) {
  const [showSolution, setShowSolution] = useState(false);
  const solved = useSolved();
  const isSolved = solved.has(problem.id);

  return (
    <div className={isSolved ? 'problem problem-solved' : 'problem'}>
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

      {problem.viz && <VizHost id={problem.viz} />}

      <div className="problem-actions">
        <button
          type="button"
          className="toggle"
          aria-expanded={showSolution}
          onClick={() => setShowSolution((s) => !s)}
        >
          {showSolution ? 'Hide solution' : 'Show solution'}
        </button>
        <button
          type="button"
          className="solved-toggle"
          aria-pressed={isSolved}
          onClick={() => toggleSolved(problem.id)}
        >
          {isSolved ? '✓ Solved' : 'Mark solved'}
        </button>
      </div>

      {showSolution && (
        <div className="solution">
          <Markdown>{problem.solution}</Markdown>
        </div>
      )}
    </div>
  );
}
