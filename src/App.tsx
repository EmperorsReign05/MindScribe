import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "./components/ChatMessage.tsx";
import { ChatInput } from "./components/ChatInput.tsx";
import { AuthModal } from "./components/AuthModal.tsx";
import { Button } from "./components/ui/button.tsx";
import { ScrollArea } from "./components/ui/scroll-area.tsx";
import { Heart, LogOut, Save, FileText, Settings } from "lucide-react";
import { supabase } from './utils/supabase/client.tsx';
import { projectId } from './utils/supabase/info.tsx';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
  sources?: Array<{ source: string }>;
}

interface User {
  id:string;
  email: string;
  user_metadata: {
    name?: string;
  };
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
 
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Function to format timestamp
  const formatTimestamp = () => new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });

  // Scroll to bottom of chat
  useEffect(() => {
    // A slight delay to allow the DOM to update before scrolling
    setTimeout(() => {
      const scrollViewport = scrollAreaRef.current?.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollViewport) {
        scrollViewport.scrollTop = scrollViewport.scrollHeight;
      }
    }, 100);
  }, [messages]);
  

  // Check for existing session on mount
  useEffect(() => {
    checkSession();
  }, []);

  const checkSession = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession();
      if (session?.access_token && session?.user) {
        setAccessToken(session.access_token);
        setUser(session.user as User);
        loadConversations(session.access_token);
      } else {
        setMessages([
          {
            id: "welcome",
            text: "Hello! I'm your AI companion here to listen and support you. To save your conversations and access them later, please sign in or create an account.",
            isUser: false,
            timestamp: formatTimestamp()
          }
        ]);
      }
    } catch (error) {
      console.error('Session check error:', error);
    }
  };

  const loadConversations = async (token: string) => {
    try {
      const response = await fetch(`https://${projectId}.supabase.co/functions/v1/make-server-16d07a57/conversations`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const { conversations } = await response.json();
        if (conversations && conversations.length > 0) {
          const latestConversation = conversations[0];
          setMessages(latestConversation.messages);
          setCurrentConversationId(latestConversation.id);
        } else {
          setMessages([
            {
              id: "welcome-auth",
              text: `Welcome back! I'm here to listen and support you. Feel free to share what's on your mind today.`,
              isUser: false,
              timestamp: formatTimestamp()
            }
          ]);
        }
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
    }
  };

  const handleAuthSuccess = (token: string, userData: any) => {
    setAccessToken(token);
    setUser(userData);
    setShowAuthModal(false);
    loadConversations(token);
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
    setUser(null);
    setAccessToken(null);
    setCurrentConversationId(null);
    setMessages([
      {
        id: "goodbye",
        text: "You've been signed out. Take care!",
        isUser: false,
        timestamp: formatTimestamp()
      }
    ]);
  };

  const saveConversation = async (msgs: Message[]) => {
    if (!accessToken || !user || msgs.length === 0) return;

    setIsSaving(true);
    try {
      const url = currentConversationId 
        ? `https://${projectId}.supabase.co/functions/v1/make-server-16d07a57/conversations/${currentConversationId}`
        : `https://${projectId}.supabase.co/functions/v1/make-server-16d07a57/conversations`;
      const method = currentConversationId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({ messages: msgs })
      });

      if (response.ok) {
        const result = await response.json();
        if (!currentConversationId && result.conversationId) {
          setCurrentConversationId(result.conversationId);
        }
      }
    } catch (error) {
      console.error('Error saving conversation:', error);
    } finally {
      setIsSaving(false);
    }
  };

  const handleSendMessage = async (text: string) => {
    const newUserMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser: true,
      timestamp: formatTimestamp(),
    };

    // Add user's message and placeholder for the AI's response
    setMessages(prevMessages => [
      ...prevMessages,
      newUserMessage,
      {
        id: (Date.now() + 1).toString(),
        text: "",
        isUser: false,
        timestamp: formatTimestamp(),
        sources: [],
      },
    ]);
    setIsTyping(false);

    try {
      const response = await fetch(`http://127.0.0.1:8000/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (!response.body) {
        throw new Error("Response body is null");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let fullResponse = "";

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        const chunk = decoder.decode(value, { stream: true });
        fullResponse += chunk;

        // Check if we've reached the sources separator
        const sourceSeparator = "\n\n---SOURCES---\n\n";
        if (fullResponse.includes(sourceSeparator)) {
          const parts = fullResponse.split(sourceSeparator);
          const content = parts[0];
          const sourcesJson = parts[1];

          if (sourcesJson) {
            try {
              const sources = JSON.parse(sourcesJson);
              setMessages(prev =>
                prev.map((msg, index) =>
                  index === prev.length - 1 ? { ...msg, text: content.trim(), sources: sources } : msg
                )
              );
            } catch (e) {
              setMessages(prev =>
                prev.map((msg, index) =>
                  index === prev.length - 1 ? { ...msg, text: content.trim() } : msg
                )
              );
            }
          }
          break;
        }

        // Update the last message's text with the new chunk
        setMessages(prev =>
          prev.map((msg, index) =>
            index === prev.length - 1 ? { ...msg, text: fullResponse } : msg
          )
        );
      }
    } catch (error) {
      console.error("Chat error:", error);
      setMessages(prev =>
        prev.map((msg, index) =>
          index === prev.length - 1 ? { ...msg, text: "Sorry, I'm having trouble connecting right now. Please try again later." } : msg
        )
      );
    }
  };

  const startNewConversation = () => {
    setCurrentConversationId(null);
    setMessages([
      {
        id: "new-conversation",
        text: "New chat started. What's on your mind?",
        isUser: false,
        timestamp: formatTimestamp()
      }
    ]);
  };

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-lg border-b border-slate-200/60 px-4 sm:px-6 py-4 shadow-sm">
        <div className="flex items-center justify-between max-w-6xl mx-auto">
          {/* Logo and Title */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
              <Heart className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-800">MindScribe</h1>
              <p className="text-slate-600 text-sm">
                {user ? `Welcome back, ${user.user_metadata?.name || 'Friend'}` : 'Your AI wellness companion'}
              </p>
            </div>
          </div>
          
          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            {user ? (
              <>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={startNewConversation} 
                  className="hidden sm:flex text-slate-600 hover:text-slate-800 hover:bg-slate-100"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  New Chat
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => saveConversation(messages)} 
                  disabled={isSaving || messages.length === 0}
                  className="text-slate-600 hover:text-slate-800 hover:bg-slate-100"
                >
                  <Save className="w-4 h-4 mr-2" />
                  {isSaving ? 'Saving...' : 'Save'}
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={handleSignOut}
                  className="text-slate-600 hover:text-slate-800 hover:bg-slate-100"
                >
                  <LogOut className="w-4 h-4 mr-2" />
                  Sign Out
                </Button>
              </>
            ) : (
              <Button 
                variant="default" 
                size="sm" 
                onClick={() => setShowAuthModal(true)}
                className="bg-blue-500 hover:bg-blue-600 text-white shadow-lg"
              >
                Sign In
              </Button>
            )}
            
            <Button 
              variant="ghost" 
              size="sm" 
              className="p-2 text-slate-600 hover:text-slate-800 hover:bg-slate-100"
            >
              <Settings className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col min-h-0">
        <ScrollArea className="flex-1 px-4 sm:px-6" ref={scrollAreaRef}>
          <div className="py-6 max-w-4xl mx-auto">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message.text}
                isUser={message.isUser}
                timestamp={message.timestamp}
              />
            ))}
            
            {isTyping && (
              <div className="flex gap-3 mb-6">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1 shadow-lg">
                  <span className="text-white text-xs font-medium">AI</span>
                </div>
                <div className="bg-white rounded-2xl rounded-bl-sm px-4 py-3 shadow-lg border border-slate-200">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Chat Input */}
        <div className="border-t border-slate-200/60 bg-white/80 backdrop-blur-lg px-4 sm:px-6 py-4">
          <div className="max-w-4xl mx-auto">
            <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
          </div>
        </div>
      </div>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </div>
  );
}