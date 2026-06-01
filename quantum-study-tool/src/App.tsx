import { HashRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import TopicList from './components/TopicList';
import TopicPage from './components/TopicPage';

// HashRouter (URLs like #/topic/...) is used so the app works when opened from a
// plain file or hosted on GitHub Pages without any server-side routing config.
export default function App() {
  return (
    <HashRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<TopicList />} />
          <Route path="/topic/:id" element={<TopicPage />} />
        </Routes>
      </Layout>
    </HashRouter>
  );
}
