import { useState } from 'react';
import { Compass, Loader2, Sparkles, TrendingUp, Clock, Download, RefreshCw } from 'lucide-react';
import RoadmapCard from './components/RoadmapCard';

const POPULAR_CAREERS = [
  { label: "Data Analyst", query: "I want to become a Data Analyst. I know basic Excel and am learning Python." },
  { label: "Frontend Dev", query: "I'm interested in web development, know HTML/CSS basics and want to learn React." },
  { label: "AI/ML Engineer", query: "I'm passionate about AI and machine learning. I know Python and basic math." },
  { label: "Full Stack Dev", query: "I want to be a Full Stack Developer. I know some JavaScript and databases." },
  { label: "Cloud Engineer", query: "I'm interested in cloud computing and DevOps. I know Linux basics." },
  { label: "Cybersecurity", query: "I want to work in cybersecurity. I understand networking fundamentals." },
];

function App() {
  const [description, setDescription] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (customQuery = null) => {
    const query = customQuery || description;
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('https://career-fordge-ai.onrender.com/generate-path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: query }),
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

  const handlePopularClick = (query) => {
    setDescription(query);
    handleSubmit(query);
  };

  const handleReset = () => {
    setResult(null);
    setDescription('');
    setError(null);
  };

  const totalWeeks = result?.roadmap?.length ? result.roadmap.length * 4 : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <header className="text-center mb-10">
          <div className="flex items-center justify-center gap-3 mb-3">
            <div className="relative">
              <Compass className="w-12 h-12 text-purple-400" />
              <Sparkles className="w-5 h-5 text-yellow-400 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white">Career Forge</h1>
          </div>
          <p className="text-purple-200 text-lg">AI-powered career guidance with curated learning resources</p>
          <div className="flex items-center justify-center gap-2 mt-2 text-purple-300 text-sm">
            <TrendingUp className="w-4 h-4" />
            <span>Trusted by 1000+ students</span>
          </div>
        </header>

        {!result ? (
          <>
            {/* Input Section */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 mb-6 border border-purple-500/20">
              <label className="block text-purple-200 mb-3 font-medium text-lg">
                Tell me about your background and career interests...
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="e.g., I am a BCA student with knowledge of Python, basic web development, and I'm interested in data science and AI..."
                className="w-full p-4 bg-white/5 border border-purple-500/30 rounded-xl text-white placeholder-purple-300/50 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none transition-all"
                rows={4}
                disabled={isLoading}
              />
              <button
                onClick={() => handleSubmit()}
                disabled={isLoading || !description.trim()}
                className="mt-4 w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 disabled:from-purple-600/50 disabled:to-indigo-600/50 disabled:cursor-not-allowed text-white py-4 px-6 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 text-lg shadow-lg shadow-purple-500/25"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Crafting your personalized roadmap...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Generate My Career Path
                  </>
                )}
              </button>
            </div>

            {/* Popular Careers */}
            <div className="mb-8">
              <p className="text-purple-300 text-sm mb-3 text-center">Or explore popular career paths:</p>
              <div className="flex flex-wrap justify-center gap-2">
                {POPULAR_CAREERS.map((career, idx) => (
                  <button
                    key={idx}
                    onClick={() => handlePopularClick(career.query)}
                    disabled={isLoading}
                    className="px-4 py-2 bg-white/5 hover:bg-white/10 border border-purple-500/30 hover:border-purple-400 rounded-full text-purple-200 text-sm transition-all disabled:opacity-50"
                  >
                    {career.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Features */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-white/5 rounded-xl p-4 border border-purple-500/20 text-center">
                <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                  <Compass className="w-5 h-5 text-blue-400" />
                </div>
                <h3 className="text-white font-medium mb-1">AI-Powered Analysis</h3>
                <p className="text-purple-300 text-sm">Personalized career recommendations based on your skills</p>
              </div>
              <div className="bg-white/5 rounded-xl p-4 border border-purple-500/20 text-center">
                <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                  <TrendingUp className="w-5 h-5 text-green-400" />
                </div>
                <h3 className="text-white font-medium mb-1">Curated Resources</h3>
                <p className="text-purple-300 text-sm">Official docs, top courses & quality YouTube tutorials</p>
              </div>
              <div className="bg-white/5 rounded-xl p-4 border border-purple-500/20 text-center">
                <div className="w-10 h-10 bg-orange-500/20 rounded-full flex items-center justify-center mx-auto mb-2">
                  <Clock className="w-5 h-5 text-orange-400" />
                </div>
                <h3 className="text-white font-medium mb-1">Step-by-Step Path</h3>
                <p className="text-purple-300 text-sm">Clear roadmap from beginner to job-ready</p>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Results Section */}
            <div className="space-y-6">
              {/* Career Summary Card */}
              <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-6 text-white relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
                <div className="relative">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-purple-200 text-sm mb-1">Recommended Career</p>
                      <h2 className="text-3xl font-bold mb-3">{result.career_role}</h2>
                      <p className="text-purple-100 max-w-xl">{result.summary}</p>
                    </div>
                  </div>
                  
                  {/* Stats */}
                  <div className="flex flex-wrap gap-4 mt-4 pt-4 border-t border-white/20">
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4 text-purple-200" />
                      <span className="text-sm">~{totalWeeks} weeks to complete</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-purple-200" />
                      <span className="text-sm">6 learning milestones</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                <button
                  onClick={handleReset}
                  className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-all"
                >
                  <RefreshCw className="w-4 h-4" />
                  New Search
                </button>
              </div>

              {/* Progress Overview */}
              <div className="bg-white/5 rounded-xl p-4 border border-purple-500/20">
                <p className="text-purple-300 text-sm mb-3">Your Learning Journey</p>
                <div className="flex items-center gap-1">
                  {result.roadmap?.map((_, idx) => (
                    <div key={idx} className="flex-1">
                      <div className={`h-2 rounded-full ${idx < 2 ? 'bg-green-500' : idx < 4 ? 'bg-yellow-500' : 'bg-red-500'}`}></div>
                      <p className="text-xs text-purple-400 mt-1 text-center">
                        {idx < 2 ? 'Beginner' : idx < 4 ? 'Intermediate' : 'Advanced'}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Roadmap Steps */}
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-white flex items-center gap-2">
                  <Compass className="w-5 h-5 text-purple-400" />
                  Your Learning Roadmap
                </h3>
                {result.roadmap?.map((step, index) => (
                  <RoadmapCard key={index} step={step} index={index} />
                ))}
              </div>
            </div>
          </>
        )}

        {/* Error Display */}
        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-red-200 px-4 py-3 rounded-xl mb-6 flex items-center gap-2">
            <span>⚠️</span>
            {error}
          </div>
        )}

        {/* Footer */}
        <footer className="text-center mt-12 pt-8 border-t border-purple-500/20">
          <p className="text-purple-400 text-sm">
            Made by Harsh Saini © 2026
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
