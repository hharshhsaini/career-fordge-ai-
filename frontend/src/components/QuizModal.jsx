import { useState } from 'react';
import { X, CheckCircle2, XCircle, Trophy, RotateCcw, Loader2, ChevronRight, Eye } from 'lucide-react';

export default function QuizModal({ isOpen, onClose, stepName, topic, onQuizComplete }) {
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showReview, setShowReview] = useState(false);

  const fetchQuiz = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // Use localhost for development, Render for production
      const apiUrl = window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : 'https://career-fordge-ai.onrender.com';
      
      const response = await fetch(`${apiUrl}/generate-quiz`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, step_name: stepName }),
      });
      if (!response.ok) throw new Error('Failed to generate quiz');
      const data = await response.json();
      setQuestions(data.questions || []);
      setCurrentQuestion(0);
      setSelectedAnswers({});
      setShowResults(false);
      setShowReview(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStart = () => {
    fetchQuiz();
  };

  const handleAnswer = (questionId, answer) => {
    setSelectedAnswers(prev => ({ ...prev, [questionId]: answer }));
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    } else {
      setShowResults(true);
    }
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach(q => {
      if (selectedAnswers[q.id] === q.correct) correct++;
    });
    return { correct, total: questions.length, percentage: Math.round((correct / questions.length) * 100) };
  };

  const handleRetry = () => {
    setSelectedAnswers({});
    setCurrentQuestion(0);
    setShowResults(false);
    setShowReview(false);
  };

  const handleComplete = () => {
    const score = calculateScore();
    if (score.percentage >= 80) {
      onQuizComplete(true);
      onClose();
    }
  };

  if (!isOpen) return null;

  const score = showResults ? calculateScore() : null;
  const passed = score?.percentage >= 80;
  const currentQ = questions[currentQuestion];

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto border border-purple-500/30">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-purple-500/20">
          <div>
            <h2 className="text-xl font-bold text-white">Knowledge Quiz</h2>
            <p className="text-purple-300 text-sm">{stepName}</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-lg transition-all">
            <X className="w-5 h-5 text-purple-300" />
          </button>
        </div>

        <div className="p-6">
          {/* Initial State - Start Quiz */}
          {questions.length === 0 && !isLoading && !error && (
            <div className="text-center py-8">
              <div className="w-20 h-20 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Trophy className="w-10 h-10 text-purple-400" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">Ready to Test Your Knowledge?</h3>
              <p className="text-purple-300 mb-2">Complete this quiz to verify your understanding of:</p>
              <p className="text-white font-medium mb-4">{stepName}</p>
              <div className="bg-purple-500/10 rounded-lg p-4 mb-6 text-left">
                <p className="text-purple-200 text-sm mb-2">📝 15 technical questions (coding & concepts)</p>
                <p className="text-purple-200 text-sm mb-2">✅ Pass mark: 80% (12/15 correct)</p>
                <p className="text-purple-200 text-sm mb-2">⏱️ Mix of easy, medium & hard questions</p>
                <p className="text-purple-200 text-sm">📖 Review answers with explanations after</p>
              </div>
              <button
                onClick={handleStart}
                className="px-8 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all"
              >
                Start Quiz
              </button>
            </div>
          )}

          {/* Loading */}
          {isLoading && (
            <div className="text-center py-12">
              <Loader2 className="w-12 h-12 text-purple-400 animate-spin mx-auto mb-4" />
              <p className="text-purple-300">Generating your personalized quiz...</p>
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="text-center py-8">
              <XCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
              <p className="text-red-300 mb-4">{error}</p>
              <button onClick={handleStart} className="px-6 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg">
                Try Again
              </button>
            </div>
          )}

          {/* Quiz Questions */}
          {questions.length > 0 && !showResults && !showReview && currentQ && (
            <div>
              {/* Progress */}
              <div className="mb-6">
                <div className="flex justify-between text-sm text-purple-300 mb-2">
                  <span>Question {currentQuestion + 1} of {questions.length}</span>
                  <span className={`px-2 py-0.5 rounded text-xs ${
                    currentQ.difficulty === 'easy' ? 'bg-green-500/20 text-green-300' :
                    currentQ.difficulty === 'medium' ? 'bg-yellow-500/20 text-yellow-300' :
                    'bg-red-500/20 text-red-300'
                  }`}>{currentQ.difficulty}</span>
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-purple-500 to-indigo-500 h-2 rounded-full transition-all"
                    style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* Question */}
              <h3 className="text-lg font-medium text-white mb-4">{currentQ.question}</h3>

              {/* Options */}
              <div className="space-y-3 mb-6">
                {Object.entries(currentQ.options).map(([key, value]) => (
                  <button
                    key={key}
                    onClick={() => handleAnswer(currentQ.id, key)}
                    className={`w-full p-4 rounded-xl text-left transition-all border ${
                      selectedAnswers[currentQ.id] === key
                        ? 'bg-purple-600/30 border-purple-500 text-white'
                        : 'bg-white/5 border-purple-500/20 text-purple-200 hover:bg-white/10'
                    }`}
                  >
                    <span className="font-semibold mr-3">{key}.</span>
                    {value}
                  </button>
                ))}
              </div>

              {/* Next Button */}
              <button
                onClick={handleNext}
                disabled={!selectedAnswers[currentQ.id]}
                className="w-full py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl font-semibold transition-all flex items-center justify-center gap-2"
              >
                {currentQuestion < questions.length - 1 ? 'Next Question' : 'See Results'}
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          )}

          {/* Results */}
          {showResults && !showReview && score && (
            <div className="text-center py-6">
              <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-4 ${
                passed ? 'bg-green-500/20' : 'bg-red-500/20'
              }`}>
                {passed ? (
                  <Trophy className="w-12 h-12 text-green-400" />
                ) : (
                  <XCircle className="w-12 h-12 text-red-400" />
                )}
              </div>
              
              <h3 className={`text-3xl font-bold mb-2 ${passed ? 'text-green-400' : 'text-red-400'}`}>
                {score.percentage}%
              </h3>
              <p className="text-white text-lg mb-1">
                {score.correct} out of {score.total} correct
              </p>
              <p className={`text-sm mb-6 ${passed ? 'text-green-300' : 'text-red-300'}`}>
                {passed ? '🎉 Congratulations! You passed!' : '😔 You need 80% to pass. Try again!'}
              </p>

              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <button
                  onClick={() => setShowReview(true)}
                  className="px-6 py-3 bg-white/10 hover:bg-white/20 text-white rounded-xl font-medium transition-all flex items-center justify-center gap-2"
                >
                  <Eye className="w-5 h-5" />
                  Review Answers
                </button>
                {passed ? (
                  <button
                    onClick={handleComplete}
                    className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-xl font-semibold transition-all flex items-center justify-center gap-2"
                  >
                    <CheckCircle2 className="w-5 h-5" />
                    Mark Step Complete
                  </button>
                ) : (
                  <button
                    onClick={handleRetry}
                    className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all flex items-center justify-center gap-2"
                  >
                    <RotateCcw className="w-5 h-5" />
                    Try Again
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Review Answers */}
          {showReview && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-white">Answer Review</h3>
                <button
                  onClick={() => setShowReview(false)}
                  className="text-purple-300 hover:text-white text-sm"
                >
                  Back to Results
                </button>
              </div>
              <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
                {questions.map((q, idx) => {
                  const userAnswer = selectedAnswers[q.id];
                  const isCorrect = userAnswer === q.correct;
                  return (
                    <div key={q.id} className={`p-4 rounded-xl border ${
                      isCorrect ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'
                    }`}>
                      <div className="flex items-start gap-2 mb-2">
                        {isCorrect ? (
                          <CheckCircle2 className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                        ) : (
                          <XCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                        )}
                        <p className="text-white font-medium">{idx + 1}. {q.question}</p>
                      </div>
                      <div className="ml-7 space-y-1 text-sm">
                        <p className="text-purple-300">
                          Your answer: <span className={isCorrect ? 'text-green-400' : 'text-red-400'}>{userAnswer}. {q.options[userAnswer]}</span>
                        </p>
                        {!isCorrect && (
                          <p className="text-green-400">
                            Correct: {q.correct}. {q.options[q.correct]}
                          </p>
                        )}
                        <p className="text-purple-400 mt-2 italic">💡 {q.explanation}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
              <div className="mt-4 pt-4 border-t border-purple-500/20 flex justify-center gap-3">
                {passed ? (
                  <button
                    onClick={handleComplete}
                    className="px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-xl font-semibold transition-all"
                  >
                    Mark Step Complete
                  </button>
                ) : (
                  <button
                    onClick={handleRetry}
                    className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white rounded-xl font-semibold transition-all"
                  >
                    Try Again
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
