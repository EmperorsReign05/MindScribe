import { useState, useEffect, useRef } from "react";
import { ChatMessage, TypingIndicator } from "./components/ChatMessage.tsx";
import { ChatInput } from "./components/ChatInput.tsx";
// import { AuthModal } from "./components/AuthModal.tsx"; // Auth disabled
import { LandingPage } from "./components/LandingPage.tsx";
import { ThemeToggle } from "./components/ThemeToggle.tsx";
import { Button } from "./components/ui/button.tsx";
import { ScrollArea } from "./components/ui/scroll-area.tsx";
import { Leaf, Home } from "lucide-react";
// import { supabase } from './utils/supabase/client.tsx'; // Auth disabled

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
  sources?: Array<{ source: string }>;
}

/* Unused interfaces disabled
interface User {
  id: string;
  email: string;
  user_metadata: {
    name?: string;
  };
}

interface Conversation {
  id: string;
  title: string;
  updated_at: string;
  history: Message[];
}
*/

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  // const [user, setUser] = useState<User | null>(null); // Auth disabled
  // const [accessToken, setAccessToken] = useState<string | null>(null); // Auth disabled
  // const [showAuthModal, setShowAuthModal] = useState(false); // Auth disabled
  // const [isSaving, setIsSaving] = useState(false); // Auth disabled
  // const [currentConversationId, setCurrentConversationId] = useState<string | null>(null); // Auth disabled
  // const [conversations, setConversations] = useState<Conversation[]>([]); // Auth disabled
  // const [isLoadingConversations, setIsLoadingConversations] = useState(false); // Auth disabled
  // const [showSidebar, setShowSidebar] = useState(false); // Auth disabled
  const [isInitializing, setIsInitializing] = useState(true);
  const [showLandingPage, setShowLandingPage] = useState(true);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Function to format timestamp
  const formatTimestamp = () => new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });

  // Function to generate conversation title from first message
  /* Unused title generation
    const generateConversationTitle = (messages: Message[]) => { ... }
  */
  /* Unused LLM title generation
    const generateConversationTitleWithLLM = async (messages: Message[]): Promise<string> => { ... }
  */


  // Scroll to bottom of chat
  useEffect(() => {
    setTimeout(() => {
      const scrollViewport = scrollAreaRef.current?.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollViewport) {
        scrollViewport.scrollTop = scrollViewport.scrollHeight;
      }
    }, 100);
  }, [messages]);

  // Simple initialization - auth disabled
  useEffect(() => {
    setMessages([
      {
        id: "welcome",
        text: "Hello! I'm your AI companion here to listen and support you. The first response may take some time.",
        isUser: false,
        timestamp: formatTimestamp()
      }
    ]);
    setIsInitializing(false);
  }, []);

  /* Auth functions disabled
  const loadConversations = async (_token: string) => { ... }
  const loadConversation = async (conversationId: string) => { ... }
  const deleteConversation = async (conversationId: string) => { ... }
  const handleAuthSuccess = (token: string, userData: any) => { ... }
  const handleSignOut = async () => { ... }
  const saveConversation = async (msgs: Message[]) => { ... }
  */

  const handleSendMessage = async (text: string) => {
    const newUserMessage: Message = {
      id: Date.now().toString(),
      text,
      isUser: true,
      timestamp: formatTimestamp(),
    };

    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);
    setIsTyping(true);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'https://mindscribe-8dar.onrender.com';
      const response = await fetch(`${backendUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/plain'
        },
        body: JSON.stringify({
          message: text,
          user_id: null
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      if (!response.body) {
        throw new Error("Response body is null");
      }

      setIsTyping(false);

      const aiMessageId = (Date.now() + 1).toString();
      const aiMessage: Message = {
        id: aiMessageId,
        text: "",
        isUser: false,
        timestamp: formatTimestamp(),
        sources: [],
      };

      setMessages(prev => [...prev, aiMessage]);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;
      let fullResponse = "";

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        const chunk = decoder.decode(value, { stream: true });
        fullResponse += chunk;

        const sourceSeparator = "\n\n---SOURCES---\n\n";
        let content = fullResponse;
        let sources: Array<{ source: string }> = [];

        if (fullResponse.includes(sourceSeparator)) {
          const parts = fullResponse.split(sourceSeparator);
          content = parts[0];
          try {
            sources = JSON.parse(parts[1] || "[]");
          } catch (e) {
            console.warn('Error parsing sources:', e);
          }
        }

        setMessages(prev =>
          prev.map(msg =>
            msg.id === aiMessageId ? { ...msg, text: content, sources: sources } : msg
          )
        );
      }


    } catch (error: any) {
      console.error("Chat error:", error);

      let errorText = "Sorry, I'm having trouble connecting right now. Please try again later.";

      if (error.name === 'AbortError') {
        errorText = "Request timed out. Please try again with a shorter message.";
      } else if (error.message.includes('Failed to fetch')) {
        errorText = "Unable to connect to the server. Please check if the backend is running and try again.";
      }

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: errorText,
        isUser: false,
        timestamp: formatTimestamp(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  /* Unused startNewConversation
    const startNewConversation = () => { ... }
  */

  // Show loading state while initializing
  if (isInitializing) {
    return (
      <div className="h-screen flex items-center justify-center bg-background gradient-mesh">
        <div className="text-center animate-fade-in">
          <div className="w-14 h-14 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-xl shadow-teal-500/30 mx-auto mb-4">
            <Leaf className="w-7 h-7 text-white" />
          </div>
          <h2 className="text-xl font-bold text-foreground mb-2">MindScribe</h2>
          <p className="text-muted-foreground">Loading your wellness companion...</p>
        </div>
      </div>
    );
  }

  // Show landing page
  if (showLandingPage) {
    return <LandingPage onStartChat={() => setShowLandingPage(false)} />;
  }

  return (
    <div className="h-screen flex bg-background gradient-mesh">
      {/* Sidebar */}
      {/* Sidebar - disabled
      {user && (
        <>
          {showSidebar && (
            <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-20 lg:hidden"
              onClick={() => setShowSidebar(false)}
            />
          )}

          <div className={`fixed lg:relative inset-y-0 left-0 z-30 w-80 bg-card/95 backdrop-blur-xl border-r border-border transform transition-transform duration-300 ease-out ${showSidebar ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
            <div className="flex flex-col h-full">
              <div className="flex items-center justify-between p-4 border-b border-border">
                <h2 className="text-lg font-semibold text-foreground">Chat History</h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowSidebar(false)}
                  className="lg:hidden"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              <div className="p-4">
                <Button
                  onClick={startNewConversation}
                  className="w-full bg-teal-500 hover:bg-teal-600 text-white"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  New Chat
                </Button>
              </div>

              <ScrollArea className="flex-1 px-4">
                {isLoadingConversations ? (
                  <div className="text-center py-8 text-slate-500">
                    Loading conversations...
                  </div>
                ) : conversations.length === 0 ? (
                  <div className="text-center py-8 text-slate-500">
                    No conversations yet.<br />
                    Start chatting to see your history here.
                  </div>
                ) : (
                  <div className="space-y-2 pb-4">
                    {conversations.map((conversation) => (
                      <div
                        key={conversation.id}
                        className={`group relative p-3 rounded-lg cursor-pointer transition-colors ${currentConversationId === conversation.id
                          ? 'bg-blue-50 border border-blue-200'
                          : 'hover:bg-slate-50'
                          }`}
                        onClick={() => loadConversation(conversation.id)}
                      >
                        <div className="pr-8">
                          <h3 className="font-medium text-slate-800 text-sm mb-1 truncate">
                            {conversation.title || generateConversationTitle(conversation.history)}
                          </h3>
                          <div className="flex items-center text-xs text-slate-500">
                            <Clock className="w-3 h-3 mr-1" />
                            {new Date(conversation.updated_at).toLocaleDateString()}
                          </div>
                        </div>

                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteConversation(conversation.id);
                          }}
                          className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity p-1 h-auto text-slate-400 hover:text-red-500"
                        >
                          <Trash2 className="w-3 h-3" />
                        </Button>
                      </div>
                    ))}
                  </div>
                )}
              </ScrollArea>
            </div>
          </div>
        </>
      )}
      */}

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-0 h-screen">
        {/* Header */}
        <header className="glass border-b border-border px-4 sm:px-6 py-4">
          <div className="flex items-center justify-between max-w-6xl mx-auto">
            {/* Logo and Title */}
            <div className="flex items-center gap-3">
              {/* Mobile Menu - disabled
              {user && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowSidebar(true)}
                  className="lg:hidden mr-2 btn-icon"
                >
                  <Menu className="w-5 h-5" />
                </Button>
              )}
              */}

              <div className="w-11 h-11 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-teal-500/25">
                <Leaf className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">MindScribe</h1>
                <p className="text-muted-foreground text-sm">
                  Your AI wellness companion
                </p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2">
              {/* Home Button */}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowLandingPage(true)}
                className="btn-icon"
                title="Back to Home"
              >
                <Home className="w-5 h-5" />
              </Button>

              {/* Theme Toggle */}
              <ThemeToggle />

              {/* Auth buttons - disabled
              {user ? (
                <>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => saveConversation(messages)}
                    disabled={isSaving || messages.length === 0}
                    className="btn-ghost hidden sm:flex"
                  >
                    <Save className="w-4 h-4 mr-2" />
                    {isSaving ? 'Saving...' : 'Save Chat'}
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleSignOut}
                    className="btn-ghost"
                  >
                    <LogOut className="w-4 h-4 sm:mr-2" />
                    <span className="hidden sm:inline">Sign Out</span>
                  </Button>
                </>
              ) : (
                <Button
                  variant="default"
                  size="sm"
                  onClick={() => setShowAuthModal(true)}
                  className="btn-primary"
                >
                  Sign In
                </Button>
              )}
              */}
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

              {isTyping && <TypingIndicator />}
            </div>
          </ScrollArea>

          {/* Chat Input */}
          <div className="border-t border-border glass px-4 sm:px-6 py-4">
            <div className="max-w-4xl mx-auto">
              <ChatInput onSendMessage={handleSendMessage} disabled={isTyping} />
            </div>
          </div>
        </div>
      </div>

      {/* Auth Modal - disabled
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuthSuccess={handleAuthSuccess}
      />
      */}
    </div>
  );
}
