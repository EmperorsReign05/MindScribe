import { useState, useEffect } from 'react';
import { Leaf, MessageCircle, Brain, Heart, Shield, ArrowRight, Sparkle } from 'lucide-react';
import { ThemeToggle } from './ThemeToggle';

interface LandingPageProps {
    onStartChat: () => void;
}

// Animated gradient orb component
function GlowOrb({ className }: { className?: string }) {
    return (
        <div className={`absolute rounded-full blur-3xl opacity-20 animate-pulse ${className}`} />
    );
}

// Feature card component  
function FeatureCard({ icon: Icon, title, description, delay }: {
    icon: React.ElementType;
    title: string;
    description: string;
    delay: number;
}) {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setIsVisible(true), delay);
        return () => clearTimeout(timer);
    }, [delay]);

    return (
        <div
            className={`group relative p-6 rounded-2xl bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm border border-slate-200/50 dark:border-slate-700/50 hover:border-teal-300 dark:hover:border-teal-600 transition-all duration-500 hover:shadow-xl hover:shadow-teal-500/10 hover:-translate-y-1 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
                }`}
        >
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-600 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <Icon className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-foreground mb-2">{title}</h3>
            <p className="text-muted-foreground text-sm leading-relaxed">{description}</p>
        </div>
    );
}

export function LandingPage({ onStartChat }: LandingPageProps) {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseMove = (e: MouseEvent) => {
            setMousePosition({ x: e.clientX, y: e.clientY });
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    const features = [
        {
            icon: Brain,
            title: "RAG-Powered Insights",
            description: "Advanced retrieval-augmented generation provides evidence-based therapeutic techniques from our curated knowledge base."
        },
        {
            icon: Heart,
            title: "Empathetic Support",
            description: "Trained on therapeutic approaches including CBT, mindfulness, and emotional regulation strategies."
        },
        {
            icon: Shield,
            title: "Safe & Private",
            description: "Your conversations are private. We prioritize your mental wellness journey in a secure environment."
        },
        {
            icon: MessageCircle,
            title: "Always Available",
            description: "Get support whenever you need it. MindScribe is here 24/7 to listen and guide you."
        }
    ];

    return (
        <div className="min-h-screen gradient-mesh overflow-hidden">
            {/* Animated background orbs */}
            <GlowOrb className="w-96 h-96 bg-teal-500 -top-48 -left-48" />
            <GlowOrb className="w-80 h-80 bg-emerald-500 top-1/4 right-0" />
            <GlowOrb className="w-64 h-64 bg-cyan-500 bottom-1/4 left-1/4" />

            {/* Interactive cursor glow */}
            <div
                className="fixed w-64 h-64 rounded-full bg-teal-500/10 blur-3xl pointer-events-none transition-transform duration-300 ease-out"
                style={{
                    left: mousePosition.x - 128,
                    top: mousePosition.y - 128,
                }}
            />

            {/* Header */}
            <header className="fixed top-0 left-0 right-0 z-50 glass border-b border-border">
                <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-teal-500/25">
                            <Leaf className="w-5 h-5 text-white" />
                        </div>
                        <span className="text-xl font-bold text-foreground">MindScribe</span>
                    </div>

                    <div className="flex items-center gap-3">
                        <ThemeToggle />
                        <button
                            onClick={onStartChat}
                            className="px-5 py-2.5 bg-teal-500 hover:bg-teal-600 text-white rounded-xl font-medium transition-all duration-200 hover:shadow-lg hover:shadow-teal-500/25 hover:scale-105"
                        >
                            Start Chatting
                        </button>
                    </div>
                </div>
            </header>

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 px-6">
                <div className="max-w-4xl mx-auto text-center">
                    {/* Badge */}
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-600 dark:text-teal-400 text-sm font-medium mb-8 animate-fade-in">
                        <Sparkle className="w-4 h-4" />
                        AI-Powered Therapeutic Support
                    </div>

                    {/* Main Heading */}
                    <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-foreground mb-6 leading-tight">
                        Your Personal
                        <span className="block bg-gradient-to-r from-teal-500 via-emerald-500 to-cyan-500 bg-clip-text text-transparent">
                            Wellness Companion
                        </span>
                    </h1>

                    {/* Subtitle */}
                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed">
                        MindScribe uses advanced RAG technology to provide evidence-based therapeutic guidance.
                        Get personalized mental wellness support through compassionate AI conversations.
                    </p>

                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <button
                            onClick={onStartChat}
                            className="group flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-600 hover:to-emerald-700 text-white rounded-2xl font-semibold text-lg transition-all duration-300 hover:shadow-2xl hover:shadow-teal-500/30 hover:scale-105"
                        >
                            Start Your Journey
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </button>
                        <span className="text-sm text-muted-foreground">No signup required</span>
                    </div>
                </div>

                {/* Floating Chat Preview */}
                <div className="max-w-2xl mx-auto mt-16 relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-teal-500 to-emerald-600 rounded-3xl blur-2xl opacity-20" />
                    <div className="relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl border border-slate-200/50 dark:border-slate-700/50 shadow-2xl shadow-slate-200/50 dark:shadow-slate-900/50 overflow-hidden">
                        {/* Chat Header */}
                        <div className="px-6 py-4 border-b border-slate-200/50 dark:border-slate-700/50 flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-xl flex items-center justify-center">
                                <Leaf className="w-5 h-5 text-white" />
                            </div>
                            <div>
                                <h3 className="font-semibold text-foreground">MindScribe</h3>
                                <p className="text-xs text-emerald-500 flex items-center gap-1">
                                    <span className="w-2 h-2 bg-emerald-500 rounded-full" />
                                    Online
                                </p>
                            </div>
                        </div>

                        {/* Sample Messages */}
                        <div className="p-6 space-y-4">
                            <div className="flex gap-3">
                                <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center flex-shrink-0">
                                    <Leaf className="w-4 h-4 text-white" />
                                </div>
                                <div className="bg-slate-100 dark:bg-slate-700/50 rounded-2xl rounded-tl-sm px-4 py-3 max-w-md">
                                    <p className="text-sm text-foreground">
                                        Hello! I'm here to support you. How are you feeling today? What's on your mind?
                                    </p>
                                </div>
                            </div>

                            <div className="flex gap-3 justify-end">
                                <div className="bg-teal-500 text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-md">
                                    <p className="text-sm">
                                        I've been feeling anxious about work lately...
                                    </p>
                                </div>
                            </div>

                            <div className="flex gap-3">
                                <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center flex-shrink-0">
                                    <Leaf className="w-4 h-4 text-white" />
                                </div>
                                <div className="bg-slate-100 dark:bg-slate-700/50 rounded-2xl rounded-tl-sm px-4 py-3 max-w-md">
                                    <p className="text-sm text-foreground">
                                        I understand, and it's completely valid to feel that way. Let's explore some techniques that can help you manage work-related anxiety...
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 px-6">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
                            Why Choose MindScribe?
                        </h2>
                        <p className="text-muted-foreground max-w-2xl mx-auto">
                            Powered by cutting-edge AI and evidence-based therapeutic practices
                        </p>
                    </div>

                    <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                        {features.map((feature, index) => (
                            <FeatureCard
                                key={feature.title}
                                icon={feature.icon}
                                title={feature.title}
                                description={feature.description}
                                delay={index * 150}
                            />
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 px-6">
                <div className="max-w-4xl mx-auto text-center">
                    <div className="relative">
                        <div className="absolute inset-0 bg-gradient-to-r from-teal-500 to-emerald-600 rounded-3xl blur-2xl opacity-20" />
                        <div className="relative bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl border border-slate-200/50 dark:border-slate-700/50 p-12">
                            <h2 className="text-3xl sm:text-4xl font-bold text-foreground mb-4">
                                Ready to Start Your Wellness Journey?
                            </h2>
                            <p className="text-muted-foreground mb-8 max-w-xl mx-auto">
                                Begin your conversation with MindScribe now. No signup required – just start chatting.
                            </p>
                            <button
                                onClick={onStartChat}
                                className="group flex items-center gap-2 px-8 py-4 bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-600 hover:to-emerald-700 text-white rounded-2xl font-semibold text-lg transition-all duration-300 hover:shadow-2xl hover:shadow-teal-500/30 hover:scale-105 mx-auto"
                            >
                                Start Chatting Now
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-8 px-6 border-t border-border">
                <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-emerald-600 rounded-lg flex items-center justify-center">
                            <Leaf className="w-4 h-4 text-white" />
                        </div>
                        <span className="font-semibold text-foreground">MindScribe</span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                        © 2024 MindScribe. AI-powered therapeutic support.
                    </p>
                </div>
            </footer>
        </div>
    );
}
