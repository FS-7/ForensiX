import { Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ContactCard } from "./ContactCard";

interface Contact {
  number: string;
}

interface RecentContactsProps {
  contacts: string[][];
  className?: string;
}

export const RecentContacts = ({ contacts, className }: RecentContactsProps) => {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5 text-primary" />
          Recently Contacted
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {contacts.length === 0 ? (
          <p className="text-center text-muted-foreground py-8">
            No recent contacts
          </p>
        ) : (
          contacts.map((contact, i) => (
            <div key={i} className="space-y-1">
              <ContactCard
                number={contact}
              />
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
};
