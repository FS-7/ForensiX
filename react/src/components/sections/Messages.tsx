import { useState, useMemo } from "react";
import { textMessages } from "@/data/mockData";
import { FilterBar } from "@/components/FilterBar";
import { cn } from "@/lib/utils";
import { MessageCircle, Send, Circle } from "lucide-react";

export function Messages() {
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState("all");
  const [readFilter, setReadFilter] = useState("all");

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
      const matchesSearch = 
        msg.contactName.toLowerCase().includes(search.toLowerCase()) ||
        msg.message.toLowerCase().includes(search.toLowerCase()) ||
        msg.phoneNumber.includes(search);
      
      const matchesType = typeFilter === "all" || msg.type === typeFilter;
      const matchesRead = readFilter === "all" || 
        (readFilter === "read" && msg.read) || 
        (readFilter === "unread" && !msg.read);
      
      return matchesSearch && matchesType && matchesRead;
    });
  }, [search, typeFilter, readFilter]);

  const hasActiveFilters = search !== "" || typeFilter !== "all" || readFilter !== "all";

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
          setReadFilter("all");
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
          {
            id: "read",
            label: "Status",
            value: readFilter,
            onChange: setReadFilter,
            options: [
              { value: "all", label: "All Status" },
              { value: "read", label: "Read" },
              { value: "unread", label: "Unread" },
            ],
          },
        ]}
      />

      <div className="space-y-3">
        {filteredMessages.map((msg) => (
          <div 
            key={msg.id} 
            className={cn(
              "card-gradient rounded-lg border border-border p-4 animate-fade-in",
              "hover:border-primary/30 transition-colors",
              !msg.read && "border-l-4 border-l-primary"
            )}
          >
            <div className="flex items-start gap-4">
              <div className={cn(
                "w-10 h-10 rounded-full flex items-center justify-center shrink-0",
                msg.type === "sent" ? "bg-primary/10" : "bg-secondary"
              )}>
                {msg.type === "sent" ? (
                  <Send className="w-4 h-4 text-primary" />
                ) : (
                  <MessageCircle className="w-4 h-4 text-muted-foreground" />
                )}
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-foreground">{msg.contactName}</span>
                    {!msg.read && (
                      <Circle className="w-2 h-2 fill-primary text-primary" />
                    )}
                  </div>
                  <span className="text-xs text-muted-foreground shrink-0">
                    {formatDate(msg.timestamp)}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground font-mono mb-2">{msg.phoneNumber}</p>
                <p className="text-sm text-foreground">{msg.message}</p>
              </div>
            </div>
          </div>
        ))}
        
        {filteredMessages.length === 0 && (
          <div className="card-gradient rounded-lg border border-border p-8 text-center text-muted-foreground animate-fade-in">
            No messages found matching your filters.
          </div>
        )}
      </div>
    </div>
  );
}
