import { useState, useEffect, useRef } from "react";
import { ChatMessage } from "./components/ChatMessage.tsx";
import { ChatInput } from "./components/ChatInput.tsx";
import { AuthModal } from "./components/AuthModal.tsx";
import { Button } from "./components/ui/button.tsx";
import { ScrollArea } from "./components/ui/scroll-area.tsx";
import { Heart, LogOut, Save, FileText, Menu, X, Clock, Trash2 } from "lucide-react";
import { supabase } from './utils/supabase/client.tsx';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
  sources?: Array<{ source: string }>;
}

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
  history: Message[]; // Changed from messages to history to match your schema
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoadingConversations, setIsLoadingConversations] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  // Function to format timestamp
  const formatTimestamp = () => new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });

  // Function to generate conversation title from first message
  const generateConversationTitle = (messages: Message[]) => {
  const firstUserMessage = messages.find(msg => msg.isUser);
  if (!firstUserMessage) return "New Conversation";
  
  let text = firstUserMessage.text.trim();
  
  // Remove common greetings and get to the actual content
  text = text.replace(/^(hi|hello|hey|good morning|good afternoon|good evening)[,.\s]*/i, '');
  
  // If it's still a short greeting, use a generic title
  if (text.length < 10 || /^(how are you|what's up|wassup|yo)[\s.!?]*$/i.test(text)) {
    // Look for the second user message with more substance
    const secondUserMessage = messages.find((msg, index) => 
      msg.isUser && index > 0 && msg.text.trim().length > 15
    );
    
    if (secondUserMessage) {
      text = secondUserMessage.text.trim();
    } else {
      return "General Chat";
    }
  }
  
  // Truncate and clean up
  const title = text.length > 35 ? text.substring(0, 35) + "..." : text;
  return title.charAt(0).toUpperCase() + title.slice(1);
};
  const generateConversationTitleWithLLM = async (messages: Message[]): Promise<string> => {
  // Only generate title if we have enough context (at least 2-3 exchanges)
  if (messages.length < 4) {
    return generateConversationTitle(messages); // Fallback to existing method
  }

  try {
    // Get the first few messages for context
    const contextMessages = messages.slice(0, 6); // First 3 exchanges
    const conversation = contextMessages
      .map(msg => `${msg.isUser ? 'User' : 'AI'}: ${msg.text}`)
      .join('\n');

    const response = await fetch(`https://mindscribe-8dar.onrender.com/chat`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'text/plain'
      },
      body: JSON.stringify({ 
        message: `Based on this conversation, generate a short, descriptive title (3-6 words max) that captures the main topic or concern. Don't use quotes or say "Title:". Just respond with the title only.\n\nConversation:\n${conversation}`,
        user_id: user ? user.id : null
      }),
      signal: AbortSignal.timeout(10000) // 10 second timeout
    });

    if (!response.ok) {
      throw new Error('Failed to generate title');
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let title = '';
    
    if (reader) {
      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          title += decoder.decode(value, { stream: true });
        }
      }
    }

    // Clean up the title
    const cleanTitle = title
      .replace(/---SOURCES---[\s\S]*$/g, '') // Remove sources section
      .replace(/^(Title:|Chat:|Conversation:)\s*/i, '') // Remove prefixes
      .replace(/["\n\r]/g, '') // Remove quotes and newlines
      .trim();

    // Validate the title
    if (cleanTitle && cleanTitle.length > 3 && cleanTitle.length < 60) {
      return cleanTitle;
    } else {
      throw new Error('Generated title not suitable');
    }

  } catch (error) {
    console.error('Error generating LLM title:', error);
    // Fallback to existing method
    return generateConversationTitle(messages);
  }
};


  // Scroll to bottom of chat
  useEffect(() => {
    setTimeout(() => {
      const scrollViewport = scrollAreaRef.current?.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollViewport) {
        scrollViewport.scrollTop = scrollViewport.scrollHeight;
      }
    }, 100);
  }, [messages]);

  // Enhanced session management
  useEffect(() => {
    const initializeApp = async () => {
      setIsInitializing(true);
      
      // Check for stored session data
      const storedUser = localStorage.getItem('mindscribe_user');
      const storedToken = localStorage.getItem('mindscribe_token');
      
      if (storedUser && storedToken) {
        try {
          const userData = JSON.parse(storedUser);
          setUser(userData);
          setAccessToken(storedToken);
          await loadConversations(storedToken);
        } catch (error) {
          console.error('Error parsing stored user data:', error);
          localStorage.removeItem('mindscribe_user');
          localStorage.removeItem('mindscribe_token');
          setDefaultWelcomeMessage();
        }
      } else {
        // Check Supabase session
        try {
          const { data: { session }, error } = await supabase.auth.getSession();
          if (error) throw error;

          if (session?.access_token && session?.user) {
            const userData = session.user as User;
            setAccessToken(session.access_token);
            setUser(userData);
            
            localStorage.setItem('mindscribe_user', JSON.stringify(userData));
            localStorage.setItem('mindscribe_token', session.access_token);
            
            await loadConversations(session.access_token);
          } else {
            setDefaultWelcomeMessage();
          }
        } catch (error: any) {
          console.error('Session check error:', error);
          setDefaultWelcomeMessage();
        }
      }
      
      setIsInitializing(false);
    };

    const setDefaultWelcomeMessage = () => {
      setMessages([
        {
          id: "welcome",
          text: "Hello! I'm your AI companion here to listen and support you. To save your conversations and access them later, please sign in or create an account.",
          isUser: false,
          timestamp: formatTimestamp()
        }
      ]);
    };

    initializeApp();

    // Listen for auth state changes - OPTIMIZED
    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      console.log('Auth state changed:', event);
      
      if (event === 'SIGNED_IN' && session) {
        const userData = session.user as User;
        setAccessToken(session.access_token);
        setUser(userData);
        
        localStorage.setItem('mindscribe_user', JSON.stringify(userData));
        localStorage.setItem('mindscribe_token', session.access_token);
        
        // Load conversations without blocking UI
        setTimeout(() => loadConversations(session.access_token), 100);
      } else if (event === 'SIGNED_OUT') {
        // Fast sign out - don't wait for anything
        setUser(null);
        setAccessToken(null);
        setCurrentConversationId(null);
        setConversations([]);
        localStorage.removeItem('mindscribe_user');
        localStorage.removeItem('mindscribe_token');
        setMessages([
          {
            id: "goodbye",
            text: "You've been signed out. Take care!",
            isUser: false,
            timestamp: formatTimestamp()
          }
        ]);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const loadConversations = async (_token: string) => {
    if (isLoadingConversations || !user) return; // Prevent multiple calls and ensure user exists
    
    setIsLoadingConversations(true);
    try {
      console.log('Loading conversations for user:', user.id);
      
      // Add timeout to prevent hanging
      const queryPromise = supabase
        .from('conversation')
        .select('*')
        .eq('user_id', user.id)
        .order('updated_at', { ascending: false });
        
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Load conversations timeout')), 8000)
      );

      const result = await Promise.race([queryPromise, timeoutPromise]) as { data: Conversation[] | null, error: any };
      const { data: conversationList, error } = result;

      if (error) {
        console.error('Supabase error:', error);
        throw error;
      }

      console.log('Loaded conversations:', conversationList);
      setConversations(conversationList || []);
      
      // Only set welcome message if no current conversation and no messages
      if (messages.length === 0 && !currentConversationId) {
        if (conversationList && conversationList.length > 0) {
          const latestConversation = conversationList[0];
          setMessages(latestConversation.history || []);
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
    } catch (error: any) {
      console.error('Error loading conversations:', error);
      // Set fallback message on timeout
      if (messages.length === 0) {
        setMessages([
          {
            id: "welcome-fallback",
            text: `Welcome! I'm here to listen and support you. Feel free to share what's on your mind today.`,
            isUser: false,
            timestamp: formatTimestamp()
          }
        ]);
      }
    } finally {
      setIsLoadingConversations(false);
    }
  };

  const loadConversation = async (conversationId: string) => {
    if (!accessToken || !user) return;
    
    try {
      console.log('Loading conversation:', conversationId);
      
      const { data: conversation, error } = await supabase
        .from('conversation')
        .select('*')
        .eq('id', conversationId)
        .eq('user_id', user.id)
        .single();

      if (error) {
        console.error('Error loading conversation:', error);
        throw error;
      }

      if (conversation) {
        console.log('Loaded conversation data:', conversation);
        setMessages(conversation.history || []);
        setCurrentConversationId(conversationId);
        setShowSidebar(false); // Close sidebar on mobile
      }
    } catch (error: any) {
      console.error('Error loading conversation:', error);
    }
  };

  const deleteConversation = async (conversationId: string) => {
    if (!accessToken || !user) return;
    
    // Immediately update UI for fast feedback
    setConversations(prev => prev.filter(conv => conv.id !== conversationId));
    
    // If we deleted the current conversation, start a new one immediately
    if (currentConversationId === conversationId) {
      startNewConversation();
    }

    // Delete in background with timeout
    try {
      console.log('Deleting conversation:', conversationId);
      
      const deletePromise = supabase
        .from('conversation')
        .delete()
        .eq('id', conversationId)
        .eq('user_id', user.id);
        
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Delete timeout')), 5000)
      );
      
      const result = await Promise.race([deletePromise, timeoutPromise]) as { error: any };
      const { error } = result;

      if (error) {
        console.error('Error deleting conversation:', error);
        // Revert UI changes on error
        loadConversations(accessToken);
      } else {
        console.log('Conversation deleted successfully');
      }
    } catch (error: any) {
      console.error('Error deleting conversation:', error);
      // Revert UI changes on timeout/error
      loadConversations(accessToken);
    }
  };

  const handleAuthSuccess = (token: string, userData: any) => {
    setAccessToken(token);
    setUser(userData);
    setShowAuthModal(false);
    
    localStorage.setItem('mindscribe_user', JSON.stringify(userData));
    localStorage.setItem('mindscribe_token', token);
    
    loadConversations(token);
  };

  const handleSignOut = async () => {
    // update UI
    setUser(null);
    setAccessToken(null);
    setCurrentConversationId(null);
    setConversations([]);
    localStorage.removeItem('mindscribe_user');
    localStorage.removeItem('mindscribe_token');
    setMessages([
      {
        id: "goodbye",
        text: "You've been signed out. Take care!",
        isUser: false,
        timestamp: formatTimestamp()
      }
    ]);

    
    try {
      const signOutPromise = supabase.auth.signOut();
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Sign out timeout')), 3000)
      );
      
      await Promise.race([signOutPromise, timeoutPromise]);
    } catch (error: any) {
      console.warn('Sign out completed with delay or error:', error.message);
    
    }
  };

  const saveConversation = async (msgs: Message[]) => {
  if (!accessToken || !user || msgs.length === 0 || isSaving) return;

  setIsSaving(true);
  try {
    
    const conversationTitle = await generateConversationTitleWithLLM(msgs);
    
    console.log('Manual save:', { currentConversationId, msgCount: msgs.length, title: conversationTitle });
    
    if (currentConversationId) {
      // Update existing conversation
      const { error } = await supabase
        .from('conversation')
        .update({ 
          history: msgs,
          title: conversationTitle,
          updated_at: new Date().toISOString()
        })
        .eq('id', currentConversationId)
        .eq('user_id', user.id);

      if (error) {
        console.error('Error updating conversation:', error);
        throw error;
      }
      console.log('Conversation updated successfully with title:', conversationTitle);
      
      // Refresh the conversations list to show updated data
      setTimeout(() => loadConversations(''), 500);
    } else {
      // Create new conversation
      const { data, error } = await supabase
        .from('conversation')
        .insert({ 
          user_id: user.id,
          history: msgs,
          title: conversationTitle,
          updated_at: new Date().toISOString()
        })
        .select()
        .single();

      if (error) {
        console.error('Error creating conversation:', error);
        throw error;
      }
      
      if (data) {
        console.log('New conversation created with title:', conversationTitle);
        setCurrentConversationId(data.id);
        
        // Refresh the conversations list to show new conversation
        setTimeout(() => loadConversations(''), 500);
      }
    }
  } catch (error: any) {
    console.error('Error saving conversation:', error);
    alert('Failed to save conversation. Please try again.');
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

    // Add user message immediately
    const updatedMessages = [...messages, newUserMessage];
    setMessages(updatedMessages);
    setIsTyping(true);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);
const backendUrl = import.meta.env.VITE_BACKEND_URL || 'https://mindscribe-8dar.onrender.com';
const response = await fetch(`${backendUrl}/chat`,{
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'text/plain'
        },
        body: JSON.stringify({ 
          message: text,
          user_id: user ? user.id : null
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

      // Add AI message placeholder
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

      // Auto-save disabled - user must manually save

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
    setShowSidebar(false);
  };

  // Show loading state while initializing
  if (isInitializing) {
    return (
      <div className="h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="text-center">
          <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-lg mx-auto mb-4">
            <Heart className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-xl font-bold text-slate-800 mb-2">MindScribe</h2>
          <p className="text-slate-600">Loading your wellness companion...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Sidebar */}
      {user && (
        <>
          {/* Overlay for mobile */}
          {showSidebar && (
            <div 
              className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
              onClick={() => setShowSidebar(false)}
            />
          )}
          
          {/* Sidebar */}
          <div className={`fixed lg:relative inset-y-0 left-0 z-30 w-80 bg-white/90 backdrop-blur-lg border-r border-slate-200/60 transform transition-transform duration-300 ease-in-out ${showSidebar ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
            <div className="flex flex-col h-full">
              {/* Sidebar Header */}
              <div className="flex items-center justify-between p-4 border-b border-slate-200/60">
                <h2 className="text-lg font-semibold text-slate-800">Chat History</h2>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setShowSidebar(false)}
                  className="lg:hidden"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
              
              {/* New Chat Button */}
              <div className="p-4">
                <Button 
                  onClick={startNewConversation}
                  className="w-full bg-blue-500 hover:bg-blue-600 text-white"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  New Chat
                </Button>
              </div>

              {/* Conversations List */}
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
                        className={`group relative p-3 rounded-lg cursor-pointer transition-colors ${
                          currentConversationId === conversation.id
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

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-0">
        {/* Header */}
        <header className="bg-white/80 backdrop-blur-lg border-b border-slate-200/60 px-4 sm:px-6 py-4 shadow-sm">
          <div className="flex items-center justify-between max-w-6xl mx-auto">
            {/* Logo and Title */}
            <div className="flex items-center gap-3">
              {user && (
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setShowSidebar(true)}
                  className="lg:hidden mr-2"
                >
                  <Menu className="w-4 h-4" />
                </Button>
              )}
              
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
                    onClick={() => saveConversation(messages)} 
                    disabled={isSaving || messages.length === 0}
                    className="text-slate-600 hover:text-slate-800 hover:bg-slate-100"
                  >
                    <Save className="w-4 h-4 mr-2" />
                    {isSaving ? 'Saving...' : 'Save Chat'}
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
      </div>

      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </div>
  );
}