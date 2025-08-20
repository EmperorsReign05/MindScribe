import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "./components/ChatMessage.tsx";
import { ChatInput } from "./components/ChatInput.tsx";
import { AuthModal } from "./components/AuthModal.tsx";
import { Button } from "./components/ui/button.tsx";
import { ScrollArea } from "./components/ui/scroll-area.tsx";
import { Heart, LogOut, Save, FileText } from "lucide-react";
import { supabase } from './utils/supabase/client.tsx';
import { projectId } from './utils/supabase/info.tsx';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
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
      // Your existing load conversation logic is good.
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
    // Your existing sign out logic is good.
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

  // --- HIGHLIGHT: RAG Integration ---
  // This is the new, updated function to handle sending messages.
  const handleSendMessage = async (text: string) => {
    const newUserMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser: true,
      timestamp: formatTimestamp()
    };

    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);
    setIsTyping(true);

    try {
      // Call our new backend endpoint for RAG chat
      const response = await fetch(`https://${projectId}.supabase.co/functions/v1/make-server-16d07a57/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Pass the auth token if the user is signed in
          ...(accessToken && { 'Authorization': `Bearer ${accessToken}` })
        },
        body: JSON.stringify({ messages: updatedMessages })
      });

      if (!response.ok) {
        throw new Error('Failed to get AI response.');
      }

      const { reply } = await response.json();

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: reply,
        isUser: false,
        timestamp: formatTimestamp()
      };
      
      const finalMessages = [...updatedMessages, aiMessage];
      setMessages(finalMessages);

      if (user) {
        saveConversation(finalMessages);
      }

    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I'm having trouble connecting right now. Please try again later.",
        isUser: false,
        timestamp: formatTimestamp()
      };
      setMessages([...updatedMessages, errorMessage]);
    } finally {
      setIsTyping(false);
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
    <div className="h-screen flex flex-col">
      <header className="bg-card border-b border-border px-6 py-4 flex items-center justify-between">
        {/* Header content remains the same */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary rounded-full flex items-center justify-center">
            <Heart className="w-5 h-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-xl font-semibold">MindScribe</h1>
            <p className="text-muted-foreground text-sm">
              {user ? `Welcome back, ${user.user_metadata?.name || 'Friend'}` : 'Your AI wellness companion'}
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          {user ? (
            <>
              <Button variant="outline" size="sm" onClick={startNewConversation} className="hidden sm:flex">
                <FileText className="w-4 h-4 mr-2" />New Chat
              </Button>
              <Button variant="outline" size="sm" onClick={() => saveConversation(messages)} disabled={isSaving || messages.length === 0}>
                <Save className="w-4 h-4 mr-2" />{isSaving ? 'Saving...' : 'Save'}
              </Button>
              <Button variant="outline" size="sm" onClick={handleSignOut}>
                <LogOut className="w-4 h-4 mr-2" />Sign Out
              </Button>
            </>
          ) : (
            <Button variant="outline" size="sm" onClick={() => setShowAuthModal(true)}>
              Sign In
            </Button>
          )}
          
          
        </div>
      </header>

      {/* Pass the ref to ScrollArea */}
      <div className="flex-1 flex flex-col min-h-0">
        <ScrollArea className="flex-1 px-6" ref={scrollAreaRef}>
          <div className="py-6">
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
                <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center flex-shrink-0 mt-1"><span className="text-secondary-foreground text-sm">AI</span></div>
                <div className="bg-secondary text-secondary-foreground px-4 py-3 rounded-2xl rounded-bl-sm">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>

        <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
      </div>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </div>
  );
}