import { User, Leaf } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: string;
  sources?: Array<{ source: string }>;
}

export function ChatMessage({ message, isUser, timestamp, sources }: ChatMessageProps) {
  return (
    <div
      className={`flex gap-3 mb-6 animate-slide-up ${isUser ? 'justify-end' : 'justify-start'}`}
    >
      {/* AI Avatar */}
      {!isUser && (
        <div className="relative flex-shrink-0 mt-1">
          <div className="w-9 h-9 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-teal-500/30">
            <Leaf className="w-4 h-4 text-white" />
          </div>
          {/* Online indicator */}
          <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 rounded-full border-2 border-white dark:border-slate-900" />
        </div>
      )}

      <div className={`flex flex-col max-w-[75%] ${isUser ? 'items-end' : 'items-start'}`}>
        {/* Message bubble */}
        <div
          className={`px-4 py-3 shadow-sm transition-smooth ${isUser
            ? 'message-user'
            : 'message-ai'
            }`}
        >
          <div className="text-[15px] leading-relaxed whitespace-pre-wrap">
            {message}
          </div>
        </div>

        {/* Timestamp */}
        <div className={`text-xs text-slate-400 dark:text-slate-500 mt-1.5 px-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {timestamp}
        </div>

        {/* Sources */}
        {sources && sources.length > 0 && !isUser && (
          <div className="mt-2 text-xs">
            <details className="cursor-pointer group">
              <summary className="text-slate-400 dark:text-slate-500 hover:text-teal-500 dark:hover:text-teal-400 transition-colors">
                <span className="ml-1">Sources ({sources.length})</span>
              </summary>
              <div className="mt-2 p-3 bg-slate-50 dark:bg-slate-800/50 rounded-xl space-y-1 animate-fade-in">
                {sources.map((source, index) => (
                  <div key={index} className="text-slate-500 dark:text-slate-400 truncate text-xs">
                    {source.source}
                  </div>
                ))}
              </div>
            </details>
          </div>
        )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="w-9 h-9 bg-gradient-to-br from-slate-600 to-slate-800 dark:from-slate-500 dark:to-slate-700 rounded-xl flex items-center justify-center flex-shrink-0 mt-1 shadow-lg">
          <User className="w-4 h-4 text-white" />
        </div>
      )}
    </div>
  );
}

// Typing indicator component
export function TypingIndicator() {
  return (
    <div className="flex gap-3 mb-6 animate-fade-in">
      <div className="relative flex-shrink-0">
        <div className="w-9 h-9 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-teal-500/30">
          <Leaf className="w-4 h-4 text-white" />
        </div>
        <div className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-400 rounded-full border-2 border-white dark:border-slate-900" />
      </div>

      <div className="message-ai px-5 py-4 shadow-sm">
        <div className="flex gap-1.5 items-center">
          <div className="w-2 h-2 bg-teal-400 rounded-full typing-dot" />
          <div className="w-2 h-2 bg-teal-400 rounded-full typing-dot" />
          <div className="w-2 h-2 bg-teal-400 rounded-full typing-dot" />
        </div>
      </div>
    </div>
  );
}