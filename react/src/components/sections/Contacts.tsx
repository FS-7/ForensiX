import { useState, useMemo } from "react";
import { contacts } from "@/data/mockData";
import { FilterBar } from "@/components/FilterBar";
import { Mail, Phone } from "lucide-react";

export interface Contact {
  id: string;
  Name: string;
  Number: string;
  Email: string;
}

export function Contacts({ report }) {
  const [contacts, setContacts] = useState(report[0]["Contacts"] || [])
  const [search, setSearch] = useState("");

  const filteredContacts = useMemo(() => {
    return contacts.filter((contact) => {
      console.log("{}", contact.Contacts)
      const matchesSearch =
        contact.Contacts[0].Name.toLowerCase().includes(search.toLowerCase()) ||
        contact.Contacts[0].Email.toLowerCase().includes(search.toLowerCase()) ||
        contact.Contacts[0].Number.includes(search)

      return matchesSearch;
    });
  }, [search]);

  const hasActiveFilters = search !== "";

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
        }}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredContacts.map((contact, i) => (
          <div
            key={i}
            className="card-gradient rounded-lg border border-border p-5 animate-fade-in hover:border-primary/30 transition-colors"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
                  <span className="text-lg font-semibold text-primary">
                    {contact.Contacts[0].Name.charAt(0)}
                  </span>
                </div>
                <div>
                  <h3 className="font-medium text-foreground">{contact.Contacts[0].Name}</h3>
                </div>
              </div>
            </div>
            {
              contact.Contacts.map((cont, i) => (

                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <Phone className="w-4 h-4 text-muted-foreground" />
                    <span className="font-mono text-foreground">{cont.Number}</span>
                  </div>
                  {contact.Contacts[0].Email && (
                    <div className="flex items-center gap-2 text-sm">
                      <Mail className="w-4 h-4 text-muted-foreground" />
                      <span className="text-muted-foreground truncate">{cont.Email}</span>
                    </div>
                  )}
                </div>

              ))
            }
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
