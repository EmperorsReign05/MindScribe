import { useState } from "react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { Send } from "lucide-react";

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled = false }: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3 items-end p-4 bg-card border-t border-border">
      <Textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Share what's on your mind..."
        className="flex-1 min-h-[48px] max-h-32 resize-none bg-input-background border border-border rounded-xl px-4 py-3 focus:ring-2 focus:ring-ring focus:border-transparent"
        disabled={disabled}
      />
      <Button
        type="submit"
        size="icon"
        className="w-12 h-12 rounded-full bg-primary hover:bg-primary/90 text-primary-foreground flex-shrink-0"
        disabled={disabled || !message.trim()}
      >
        <Send className="w-4 h-4" />
      </Button>
    </form>
  );
}