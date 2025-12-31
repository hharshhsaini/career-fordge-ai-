import { useState } from 'react';
import { Compass, Loader2 } from 'lucide-react';
import RoadmapCard from './components/RoadmapCard';

function App() {
  const [description, setDescription] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!description.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('https://career-fordge-ai.onrender.com/generate-path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate career path');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <header className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Compass className="w-10 h-10 text-purple-400" />
            <h1 className="text-4xl font-bold text-white">Career Forge</h1>
          </div>
          <p className="text-purple-200">AI-powered career guidance with curated learning resources</p>
        </header>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 mb-8">
          <label className="block text-purple-200 mb-3 font-medium">
            Tell me about your studies and skills...
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="e.g., I am a BCA student with knowledge of Python, basic web development, and I'm interested in data and AI..."
            className="w-full p-4 bg-white/5 border border-purple-500/30 rounded-xl text-white placeholder-purple-300/50 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
            rows={4}
            disabled={isLoading}
          />
          <button
            onClick={handleSubmit}
            disabled={isLoading || !description.trim()}
            className="mt-4 w-full bg-purple-600 hover:bg-purple-700 disabled:bg-purple-600/50 disabled:cursor-not-allowed text-white py-3 px-6 rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Generating your career path...
              </>
            ) : (
              'Generate Career Path'
            )}
          </button>
        </div>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        {result && (
          <div className="space-y-6">
            {/* Career Summary */}
            <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-6 text-white">
              <h2 className="text-2xl font-bold mb-2">{result.career_role}</h2>
              <p className="text-purple-100">{result.summary}</p>
            </div>

            {/* Roadmap Steps */}
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white">Your Learning Roadmap</h3>
              {result.roadmap?.map((step, index) => (
                <RoadmapCard key={index} step={step} index={index} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
