import { useState, useEffect, useRef } from 'react';
import { Compass, Sparkles, TrendingUp, Clock, Download, RefreshCw, BarChart3 } from 'lucide-react';
import RoadmapCard from './components/RoadmapCard';
import ProgressChart from './components/ProgressChart';
import LoadingAnimation from './components/LoadingAnimation';
import jsPDF from 'jspdf';

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
  const [completedSteps, setCompletedSteps] = useState({});
  const [showProgress, setShowProgress] = useState(false);
  const roadmapRef = useRef(null);

  // Load saved progress from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('careerforge_progress');
    if (saved) {
      setCompletedSteps(JSON.parse(saved));
    }
  }, []);

  // Save progress to localStorage
  useEffect(() => {
    if (Object.keys(completedSteps).length > 0) {
      localStorage.setItem('careerforge_progress', JSON.stringify(completedSteps));
    }
  }, [completedSteps]);

  const handleSubmit = async (customQuery = null) => {
    const query = customQuery || description;
    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      // Use localhost for development, Render for production
      const apiUrl = window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : 'https://career-fordge-ai.onrender.com';
      
      const response = await fetch(`${apiUrl}/generate-path`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: query }),
      });

      if (!response.ok) {
        throw new Error('Failed to generate career path');
      }

      const data = await response.json();
      setResult(data);
      
      // Initialize progress for this career
      const careerKey = data.career_role?.replace(/\s+/g, '_').toLowerCase();
      if (careerKey && !completedSteps[careerKey]) {
        setCompletedSteps(prev => ({ ...prev, [careerKey]: [] }));
      }
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStepComplete = (stepIndex, isComplete) => {
    if (!result) return;
    const careerKey = result.career_role?.replace(/\s+/g, '_').toLowerCase();
    
    setCompletedSteps(prev => {
      const current = prev[careerKey] || [];
      if (isComplete) {
        return { ...prev, [careerKey]: [...new Set([...current, stepIndex])] };
      } else {
        return { ...prev, [careerKey]: current.filter(i => i !== stepIndex) };
      }
    });
  };

  const getCompletedCount = () => {
    if (!result) return 0;
    const careerKey = result.career_role?.replace(/\s+/g, '_').toLowerCase();
    return completedSteps[careerKey]?.length || 0;
  };

  const handlePopularClick = (query) => {
    setDescription(query);
    handleSubmit(query);
  };

  const handleReset = () => {
    setResult(null);
    setDescription('');
    setError(null);
    setShowProgress(false);
  };

  const handleDownloadPDF = () => {
    if (!result) return;
    
    try {
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      let yPos = 20;
      
      // Title
      pdf.setFontSize(24);
      pdf.setTextColor(88, 28, 135); // Purple
      pdf.text('Career Forge - Learning Roadmap', pageWidth / 2, yPos, { align: 'center' });
      yPos += 15;
      
      // Career Role
      pdf.setFontSize(18);
      pdf.setTextColor(0, 0, 0);
      pdf.text(`Career: ${result.career_role}`, 15, yPos);
      yPos += 10;
      
      // Summary
      pdf.setFontSize(11);
      pdf.setTextColor(80, 80, 80);
      const summaryLines = pdf.splitTextToSize(result.summary || '', pageWidth - 30);
      pdf.text(summaryLines, 15, yPos);
      yPos += summaryLines.length * 6 + 10;
      
      // Roadmap Steps
      pdf.setFontSize(14);
      pdf.setTextColor(88, 28, 135);
      pdf.text('Learning Roadmap:', 15, yPos);
      yPos += 10;
      
      result.roadmap?.forEach((step, index) => {
        // Check if we need a new page
        if (yPos > 260) {
          pdf.addPage();
          yPos = 20;
        }
        
        // Step header
        pdf.setFontSize(12);
        pdf.setTextColor(0, 0, 0);
        pdf.text(`${index + 1}. ${step.step_name}`, 15, yPos);
        yPos += 7;
        
        // Official docs
        if (step.official_docs_url) {
          pdf.setFontSize(10);
          pdf.setTextColor(59, 130, 246); // Blue
          pdf.text(`   📚 Docs: ${step.official_docs_url}`, 15, yPos);
          yPos += 6;
        }
        
        // Paid course
        if (step.paid_course_recommendation) {
          pdf.setFontSize(10);
          pdf.setTextColor(34, 197, 94); // Green
          const courseLines = pdf.splitTextToSize(`   🎓 Course: ${step.paid_course_recommendation}`, pageWidth - 35);
          pdf.text(courseLines, 15, yPos);
          yPos += courseLines.length * 5;
        }
        
        // YouTube videos
        if (step.video_results?.length > 0) {
          pdf.setFontSize(10);
          pdf.setTextColor(239, 68, 68); // Red
          step.video_results.forEach(video => {
            const videoLines = pdf.splitTextToSize(`   ▶️ ${video.title}`, pageWidth - 35);
            pdf.text(videoLines, 15, yPos);
            yPos += videoLines.length * 5;
            pdf.setTextColor(100, 100, 100);
            pdf.text(`      ${video.url}`, 15, yPos);
            yPos += 5;
          });
        }
        
        yPos += 8;
      });
      
      // Footer
      pdf.setFontSize(9);
      pdf.setTextColor(150, 150, 150);
      pdf.text('Generated by Career Forge - Made by Harsh Saini', pageWidth / 2, 285, { align: 'center' });
      
      pdf.save(`${result.career_role?.replace(/\s+/g, '_') || 'career'}_roadmap.pdf`);
    } catch (err) {
      console.error('PDF generation failed:', err);
      alert('Failed to generate PDF. Please try again.');
    }
  };

  const totalWeeks = result?.roadmap?.length ? result.roadmap.length * 4 : 0;
  const progressPercent = result?.roadmap ? Math.round((getCompletedCount() / result.roadmap.length) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Full Screen Loading Animation */}
      {isLoading && <LoadingAnimation />}
      
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
                <Sparkles className="w-5 h-5" />
                Generate My Career Path
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
                  <BarChart3 className="w-5 h-5 text-orange-400" />
                </div>
                <h3 className="text-white font-medium mb-1">Track Progress</h3>
                <p className="text-purple-300 text-sm">Mark completed steps and visualize your learning journey</p>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Results Section */}
            <div className="space-y-6" ref={roadmapRef}>
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
                    <div className="flex items-center gap-2">
                      <BarChart3 className="w-4 h-4 text-purple-200" />
                      <span className="text-sm">{progressPercent}% completed</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={handleReset}
                  className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-white transition-all"
                >
                  <RefreshCw className="w-4 h-4" />
                  New Search
                </button>
                <button
                  onClick={handleDownloadPDF}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 rounded-lg text-white transition-all"
                >
                  <Download className="w-4 h-4" />
                  Download PDF
                </button>
                <button
                  onClick={() => setShowProgress(!showProgress)}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white transition-all"
                >
                  <BarChart3 className="w-4 h-4" />
                  {showProgress ? 'Hide' : 'Show'} Progress
                </button>
              </div>

              {/* Progress Chart */}
              {showProgress && (
                <ProgressChart 
                  totalSteps={result.roadmap?.length || 6} 
                  completedSteps={getCompletedCount()}
                  careerRole={result.career_role}
                />
              )}

              {/* Progress Overview Bar */}
              <div className="bg-white/5 rounded-xl p-4 border border-purple-500/20">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-purple-300 text-sm">Your Learning Progress</p>
                  <p className="text-white font-medium">{getCompletedCount()}/{result.roadmap?.length || 6} steps</p>
                </div>
                <div className="w-full bg-white/10 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${progressPercent}%` }}
                  ></div>
                </div>
                <div className="flex justify-between mt-2">
                  {result.roadmap?.map((_, idx) => (
                    <div key={idx} className="flex flex-col items-center">
                      <div className={`w-3 h-3 rounded-full ${
                        completedSteps[result.career_role?.replace(/\s+/g, '_').toLowerCase()]?.includes(idx) 
                          ? 'bg-green-500' 
                          : 'bg-white/20'
                      }`}></div>
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
                  <RoadmapCard 
                    key={index} 
                    step={step} 
                    index={index}
                    isCompleted={completedSteps[result.career_role?.replace(/\s+/g, '_').toLowerCase()]?.includes(index)}
                    onToggleComplete={(isComplete) => handleStepComplete(index, isComplete)}
                  />
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
