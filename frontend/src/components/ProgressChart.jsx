import { TrendingUp, Target, Award } from 'lucide-react';

export default function ProgressChart({ totalSteps, completedSteps, careerRole }) {
  const percentage = Math.round((completedSteps / totalSteps) * 100);
  
  // Calculate circle progress
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const getMotivationalMessage = () => {
    if (percentage === 0) return "Start your journey today! 🚀";
    if (percentage < 25) return "Great start! Keep going! 💪";
    if (percentage < 50) return "You're making progress! 🌟";
    if (percentage < 75) return "Halfway there! Amazing! 🔥";
    if (percentage < 100) return "Almost done! You got this! ⭐";
    return "Congratulations! You did it! 🎉";
  };

  return (
    <div className="bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-2xl p-6 border border-purple-500/30">
      <h3 className="text-white font-bold text-lg mb-4 flex items-center gap-2">
        <TrendingUp className="w-5 h-5 text-purple-400" />
        Progress Dashboard
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Circular Progress */}
        <div className="flex flex-col items-center">
          <div className="relative">
            <svg className="w-36 h-36 transform -rotate-90">
              {/* Background circle */}
              <circle
                cx="72"
                cy="72"
                r={radius}
                stroke="rgba(255,255,255,0.1)"
                strokeWidth="12"
                fill="none"
              />
              {/* Progress circle */}
              <circle
                cx="72"
                cy="72"
                r={radius}
                stroke="url(#gradient)"
                strokeWidth="12"
                fill="none"
                strokeLinecap="round"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                className="transition-all duration-1000 ease-out"
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#22c55e" />
                  <stop offset="100%" stopColor="#10b981" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold text-white">{percentage}%</span>
              <span className="text-purple-300 text-xs">Complete</span>
            </div>
          </div>
          <p className="text-purple-200 text-sm mt-2 text-center">{getMotivationalMessage()}</p>
        </div>

        {/* Stats */}
        <div className="space-y-4">
          <div className="bg-white/5 rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center">
                <Target className="w-5 h-5 text-green-400" />
              </div>
              <div>
                <p className="text-purple-300 text-xs">Steps Completed</p>
                <p className="text-white text-xl font-bold">{completedSteps} / {totalSteps}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white/5 rounded-xl p-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center">
                <Award className="w-5 h-5 text-blue-400" />
              </div>
              <div>
                <p className="text-purple-300 text-xs">Career Goal</p>
                <p className="text-white text-sm font-medium truncate">{careerRole}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Step Progress Bars */}
        <div className="space-y-2">
          <p className="text-purple-300 text-xs mb-2">Step-by-Step Progress</p>
          {Array.from({ length: totalSteps }).map((_, idx) => {
            const isComplete = idx < completedSteps;
            const level = idx < 2 ? 'Beginner' : idx < 4 ? 'Intermediate' : 'Advanced';
            const color = idx < 2 ? 'bg-green-500' : idx < 4 ? 'bg-yellow-500' : 'bg-red-500';
            
            return (
              <div key={idx} className="flex items-center gap-2">
                <span className="text-purple-400 text-xs w-6">S{idx + 1}</span>
                <div className="flex-1 bg-white/10 rounded-full h-2">
                  <div 
                    className={`h-2 rounded-full transition-all duration-500 ${isComplete ? color : 'bg-transparent'}`}
                    style={{ width: isComplete ? '100%' : '0%' }}
                  ></div>
                </div>
                <span className={`text-xs ${isComplete ? 'text-green-400' : 'text-purple-400'}`}>
                  {isComplete ? '✓' : '○'}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
