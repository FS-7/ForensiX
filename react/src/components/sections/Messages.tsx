import { useState, useMemo } from "react";
import { FilterBar } from "@/components/FilterBar";
import { cn } from "@/lib/utils";
import { MessageCircle, Send, User } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

export interface TextMessage {
  Name: string;
  Number: string;
  Messages: {
    Content: string;
    Type: 'sent' | 'received';
    DateSent: string;
    DateReceived: string;
  }
  Tags: [];
}

export function Messages({report}) {
  //let textMessages = report[0]["Messages"]

  const [textMessages, setTextMessages] = useState(report[0]["Messages"] || [])
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    if (diffDays === 1) return 'Yesterday';
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const filteredMessages = useMemo(() => {
    return textMessages.filter((msg) => {
      console.log(msg)
      const matchesSearch = 
        (msg.Name && msg.Name.toLowerCase().includes(search.toLowerCase())) ||
        msg.Messages.filter((con) => { return con.Content.toLowerCase().includes(search.toLowerCase()) }) ||
        msg.Number.includes(search);
      
      const matchesType = typeFilter === "all" || typeFilter === msg.Messages.Content.Type.toLowerCase();
      
      return matchesSearch && matchesType;
    }); 
  }, [search, typeFilter]);

  const hasActiveFilters = search !== "" || typeFilter !== "all" ;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Text Messages</h2>
        <p className="text-muted-foreground">Browse and search your messages</p>
      </div>

      <FilterBar
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search messages..."
        hasActiveFilters={hasActiveFilters}
        onClearFilters={() => {
          setSearch("");
          setTypeFilter("all");
        }}
        filters={[
          {
            id: "type",
            label: "Direction",
            value: typeFilter,
            onChange: setTypeFilter,
            options: [
              { value: "all", label: "All Messages" },
              { value: "sent", label: "Sent" },
              { value: "received", label: "Received" },
            ],
          },
        ]}
      />

      <div className="card-gradient rounded-lg border border-border overflow-hidden animate-fade-in">
        {filteredMessages.length > 0 ? (
          <Accordion type="multiple" className="w-full">
            {filteredMessages.map((message) => (
              <AccordionItem key={message.Number} value={message.Number} className="border-border">
                <AccordionTrigger className="px-4 py-3 hover:bg-secondary/50 hover:no-underline">
                  <div className="flex items-center gap-4 w-full">
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                      <User className="w-4 h-4 text-primary" />
                    </div>
                    <div className="flex-1 text-left">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-foreground">{message.Name}</p>
                      </div>
                      <p className="text-sm font-mono text-muted-foreground">{message.Number}</p>
                    </div>
                    <div className="flex items-center gap-2 mr-4">
                      <Badge variant="secondary">
                        {message.Messages.length} message{message.Messages.length !== 1 ? 's' : ''}
                      </Badge>
                    </div>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="px-4 pb-3">
                  <div className="space-y-2 mt-2">
                    {message.Messages.map((msg, i) => (
                      <div
                        key={i}
                        className={cn(
                          "p-3 rounded-lg border border-border/50",
                          msg.Type === "sent" ? "bg-primary/5 ml-8" : "bg-secondary/30 mr-8",
                        )}
                      >
                        <div className="flex items-center justify-between gap-2 mb-2">
                          <div className="flex items-center gap-2">
                            {msg.Type.toLowerCase() === "sent" ? (
                              <Send className="w-3 h-3 text-primary" />
                            ) : (
                              <MessageCircle className="w-3 h-3 text-muted-foreground" />
                            )}
                            <span className="text-xs text-muted-foreground capitalize">{msg.Type}</span>
                            
                          </div>
                          <span className="text-xs text-muted-foreground">
                            {formatDate(msg.DateSent)}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {formatDate(msg.DateReceived)}
                          </span>
                        </div>
                        <p className="text-sm text-foreground">{msg.Content}</p>
                      </div>
                    ))}
                  </div>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        ) : (
          <div className="p-8 text-center text-muted-foreground">
            No messages found matching your filters.
          </div>
        )}
      </div>
    </div>
  );
}
