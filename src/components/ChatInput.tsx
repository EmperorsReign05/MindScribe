import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSendMessage, disabled = false }: ChatInputProps) {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message.trim());
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);

    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  };

  useEffect(() => {
    if (textareaRef.current && !disabled) {
      textareaRef.current.focus();
    }
  }, [disabled]);

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="relative flex items-end gap-2 p-2 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-xl shadow-slate-200/50 dark:shadow-slate-900/50 transition-all duration-300 focus-within:border-teal-300 dark:focus-within:border-teal-500 focus-within:shadow-teal-100/50 dark:focus-within:shadow-teal-900/30">
        {/* Text input */}
        <textarea
          ref={textareaRef}
          value={message}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Share what's on your mind..."
          disabled={disabled}
          className="flex-1 resize-none bg-transparent px-3 py-2.5 text-[15px] text-slate-800 dark:text-slate-100 placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
          style={{
            minHeight: '44px',
            maxHeight: '150px',
            lineHeight: '1.5'
          }}
          rows={1}
        />

        {/* Action buttons */}
        <div className="flex items-center gap-1 pb-0.5">
          {/* Send button */}
          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className={`p-2.5 rounded-xl transition-all duration-200 ${message.trim() && !disabled
              ? 'bg-teal-500 hover:bg-teal-600 text-white shadow-lg shadow-teal-500/30 hover:shadow-teal-500/40 scale-100 hover:scale-105'
              : 'bg-slate-100 dark:bg-slate-700 text-slate-400 dark:text-slate-500 cursor-not-allowed'
              }`}
          >
            <Send className={`w-4 h-4 transition-transform duration-200 ${message.trim() ? '-rotate-45' : ''}`} />
            <span className="sr-only">Send message</span>
          </button>
        </div>
      </div>

      {/* Helper text */}
      <p className="text-xs text-center text-slate-400 dark:text-slate-500 mt-2">
        Press <kbd className="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded text-[10px] font-medium">Enter</kbd> to send, <kbd className="px-1.5 py-0.5 bg-slate-100 dark:bg-slate-800 rounded text-[10px] font-medium">Shift+Enter</kbd> for new line
      </p>
    </form>
  );
}