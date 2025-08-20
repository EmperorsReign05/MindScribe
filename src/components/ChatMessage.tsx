import { Avatar, AvatarFallback } from "./ui/avatar";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp: string;
}

export function ChatMessage({ message, isUser, timestamp }: ChatMessageProps) {
  return (
    <div className={`flex gap-3 mb-6 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <Avatar className="w-8 h-8 mt-1 flex-shrink-0">
        <AvatarFallback className={`text-sm ${isUser ? 'bg-primary text-primary-foreground' : 'bg-secondary text-secondary-foreground'}`}>
          {isUser ? 'U' : 'AI'}
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
        <span className="text-muted-foreground text-sm mt-1 px-1">
          {timestamp}
        </span>
      </div>
    </div>
  );
}