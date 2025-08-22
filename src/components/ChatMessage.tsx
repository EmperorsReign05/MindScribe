import { Avatar, AvatarFallback } from "./ui/avatar";
import { Badge } from "./ui/badge";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: string;
  sources?: Array<{ source: string }>;
}

export function ChatMessage({ message, isUser, timestamp, sources }: ChatMessageProps) {
  // Render a thinking animation if the message is from the AI and is empty
  if (!isUser && !message) {
    return (
      <div className="flex gap-3 mb-6 flex-row">
        <Avatar className="w-8 h-8 mt-1 flex-shrink-0">
          <AvatarFallback className="text-sm bg-secondary text-secondary-foreground">
            AI
          </AvatarFallback>
        </Avatar>
        <div className="flex flex-col max-w-[80%] items-start">
          <div className="bg-secondary text-secondary-foreground px-4 py-3 rounded-2xl rounded-bl-sm">
            <div className="flex gap-1.5 items-center">
              <span className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse-dot"></span>
              <span className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse-dot"></span>
              <span className="w-2 h-2 rounded-full bg-muted-foreground animate-pulse-dot"></span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex gap-3 mb-6 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <Avatar className="w-8 h-8 mt-1 flex-shrink-0">
        <AvatarFallback className={`text-sm ${isUser ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
          {isUser ? 'You' : 'AI'}
        </AvatarFallback>
      </Avatar>
      
      <div className={`flex flex-col max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div 
          className={`px-4 py-3 rounded-2xl ${
            isUser 
              ? 'bg-card text-card-foreground border border-border rounded-br-sm' 
              : 'bg-secondary text-secondary-foreground rounded-bl-sm'
          }`}
        >
          <p className="whitespace-pre-wrap">{message}</p>
        </div>
        <div className="flex items-center gap-2 mt-1 px-1">
          <span className="text-muted-foreground text-sm">
            {timestamp}
          </span>
          {sources && sources.length > 0 && (
            <div className="flex gap-1 flex-wrap">
              {sources.map((s, index) => (
                <Badge key={index} variant="outline">{s.source}</Badge>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}