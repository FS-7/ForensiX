import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2, Send, MessageCircle, ArrowLeft } from "lucide-react";
import { Navigation } from "@/components/Navigation";
import { Link } from "react-router-dom";

interface Message {
    role: "user" | "assistant";
    content: string;
}

const BACKEND = import.meta.env.VITE_BACKEND;

export const CaseNLPChat = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = { role: "user", content: input };

        fetch(BACKEND + 'internal/nlp', {
            method: 'POST',
            body: new URLSearchParams({
                query: input,
            })
        })
            .then((res) => {
                res.text().then(r => {
                    const botMessage: Message = { role: "assistant", content: r };
                    setMessages(prev => [...prev, botMessage]);
                    setIsLoading(false);
                })
                
            })
            .catch((res) => {
                console.log(res);
                setIsLoading(false);
            })
        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setIsLoading(true);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="min-h-screen bg-background">
            <Navigation />
            <main className="container mx-auto px-4 py-8">
                <div className="mb-6">
                    <Link to="/">
                        <Button variant="ghost" className="gap-2 mb-4">
                            <ArrowLeft className="h-4 w-4" />
                            Back to Cases
                        </Button>
                    </Link>
                </div>

                <Card className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2 mb-4">
                            <MessageCircle className="h-5 w-5 text-primary" />
                            <h2 className="text-xl font-semibold">AI Case Assistant</h2>

                        </div>
                    </div>
                    <ScrollArea className="h-[400px] mb-4 pr-4">
                        {messages.length === 0 ? (
                            <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground">
                                <MessageCircle className="h-12 w-12 mb-2 opacity-50" />
                                <p>Ask questions about the cases</p>
                                <p className="text-sm mt-1">Try asking about evidence, timeline, or next steps</p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {messages.map((msg, idx) => (
                                    <div
                                        key={idx}
                                        className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                                    >
                                        <div
                                            className={`max-w-[80%] rounded-lg p-3 ${msg.role === "user"
                                                ? "bg-primary text-primary-foreground"
                                                : "bg-muted text-foreground"
                                                }`}
                                        >
                                            <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                                        </div>
                                    </div>
                                ))}
                                {isLoading && (
                                    <div className="flex justify-start">
                                        <div className="bg-muted rounded-lg p-3">
                                            <Loader2 className="h-4 w-4 animate-spin" />
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </ScrollArea>

                    <div className="flex gap-2 items-center">
                        <Textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask about this case..."
                            className="resize-none"
                            rows={2}
                            disabled={isLoading}
                        />
                        <Button onClick={sendMessage} disabled={isLoading || !input.trim()} size="lg" className="">
                            {isLoading ? (
                                <Loader2 className="aspect-square h-4 w-4 animate-spin" />
                            ) : (
                                <Send className="aspect-square h-4 w-4" />
                            )}
                        </Button>
                    </div>
                </Card>
            </main>
        </div>
    );
};
