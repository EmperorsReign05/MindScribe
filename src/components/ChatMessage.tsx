import { User, Bot } from 'lucide-react';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: string;
  sources?: Array<{ source: string }>;
}

export function ChatMessage({ message, isUser, timestamp, sources }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1 shadow-lg">
          <Bot className="w-4 h-4 text-white" />
        </div>
      )}
      
      <div className={`flex flex-col max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div
          className={`px-4 py-3 rounded-2xl shadow-lg border ${
            isUser
              ? 'bg-blue-500 text-white rounded-br-sm border-blue-600'
              : 'bg-white text-slate-800 rounded-bl-sm border-slate-200'
          }`}
        >
          <div className="text-sm leading-relaxed whitespace-pre-wrap">
            {message}
          </div>
        </div>
        
        <div className={`text-xs text-slate-500 mt-1 px-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {timestamp}
        </div>
        
        {sources && sources.length > 0 && !isUser && (
          <div className="mt-2 text-xs">
            <details className="cursor-pointer">
              <summary className="text-slate-500 hover:text-slate-700">
                Sources ({sources.length})
              </summary>
              <div className="mt-1 space-y-1">
                {sources.map((source, index) => (
                  <div key={index} className="text-slate-600 truncate">
                    {source.source}
                  </div>
                ))}
              </div>
            </details>
          </div>
        )}
      </div>
      
      {isUser && (
        <div className="w-8 h-8 bg-gradient-to-br from-slate-600 to-slate-700 rounded-full flex items-center justify-center flex-shrink-0 mt-1 shadow-lg">
          <User className="w-4 h-4 text-white" />
        </div>
      )}
    </div>
  );
}