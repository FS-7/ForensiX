import { useState, useMemo } from "react";
import { contacts } from "@/data/mockData";
import { FilterBar } from "@/components/FilterBar";
import { cn } from "@/lib/utils";
import { Star, Mail, Building2, Phone } from "lucide-react";

export function Contacts() {
  const [search, setSearch] = useState("");
  const [favoriteFilter, setFavoriteFilter] = useState("all");

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const filteredContacts = useMemo(() => {
    return contacts.filter((contact) => {
      const matchesSearch = 
        contact.name.toLowerCase().includes(search.toLowerCase()) ||
        contact.email.toLowerCase().includes(search.toLowerCase()) ||
        contact.phoneNumber.includes(search) ||
        contact.company.toLowerCase().includes(search.toLowerCase());
      
      const matchesFavorite = favoriteFilter === "all" || 
        (favoriteFilter === "favorites" && contact.favorite) ||
        (favoriteFilter === "regular" && !contact.favorite);
      
      return matchesSearch && matchesFavorite;
    });
  }, [search, favoriteFilter]);

  const hasActiveFilters = search !== "" || favoriteFilter !== "all";

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Contacts</h2>
        <p className="text-muted-foreground">Manage and search your contacts</p>
      </div>

      <FilterBar
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search contacts..."
        hasActiveFilters={hasActiveFilters}
        onClearFilters={() => {
          setSearch("");
          setFavoriteFilter("all");
        }}
        filters={[
          {
            id: "favorite",
            label: "Filter",
            value: favoriteFilter,
            onChange: setFavoriteFilter,
            options: [
              { value: "all", label: "All Contacts" },
              { value: "favorites", label: "Favorites" },
              { value: "regular", label: "Regular" },
            ],
          },
        ]}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredContacts.map((contact) => (
          <div 
            key={contact.id} 
            className="card-gradient rounded-lg border border-border p-5 animate-fade-in hover:border-primary/30 transition-colors"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
                  <span className="text-lg font-semibold text-primary">
                    {contact.name.charAt(0)}
                  </span>
                </div>
                <div>
                  <h3 className="font-medium text-foreground">{contact.name}</h3>
                  {contact.company && (
                    <div className="flex items-center gap-1 text-xs text-muted-foreground">
                      <Building2 className="w-3 h-3" />
                      {contact.company}
                    </div>
                  )}
                </div>
              </div>
              {contact.favorite && (
                <Star className="w-5 h-5 fill-warning text-warning" />
              )}
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm">
                <Phone className="w-4 h-4 text-muted-foreground" />
                <span className="font-mono text-foreground">{contact.phoneNumber}</span>
              </div>
              {contact.email && (
                <div className="flex items-center gap-2 text-sm">
                  <Mail className="w-4 h-4 text-muted-foreground" />
                  <span className="text-muted-foreground truncate">{contact.email}</span>
                </div>
              )}
            </div>
            
            <div className="mt-4 pt-3 border-t border-border">
              <p className="text-xs text-muted-foreground">
                Last contacted: {formatDate(contact.lastContacted)}
              </p>
            </div>
          </div>
        ))}
      </div>
      
      {filteredContacts.length === 0 && (
        <div className="card-gradient rounded-lg border border-border p-8 text-center text-muted-foreground animate-fade-in">
          No contacts found matching your filters.
        </div>
      )}
    </div>
  );
}
