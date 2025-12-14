import { cn } from "@/lib/utils";
import { 
  Smartphone, 
  Phone, 
  MessageSquare, 
  Users, 
  FolderOpen,
  Activity,
  Images
} from "lucide-react";

type Section = 'overview' | 'calls' | 'messages' | 'contacts' | 'files' | 'photos';

interface SidebarProps {
  activeSection: Section;
  onSectionChange: (section: Section) => void;
}

const navItems = [
  { id: 'overview' as Section, label: 'Device Overview', icon: Smartphone },
  { id: 'calls' as Section, label: 'Call Logs', icon: Phone },
  { id: 'messages' as Section, label: 'Messages', icon: MessageSquare },
  { id: 'contacts' as Section, label: 'Contacts', icon: Users },
  { id: 'files' as Section, label: 'Files', icon: FolderOpen },
  { id: 'photos' as Section, label: 'Photos', icon: Images },
];

export function Sidebar({ activeSection, onSectionChange }: SidebarProps) {
  return (
    <aside className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col justify-between">
      <nav className="flex-1 p-4">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeSection === item.id;
            
            return (
              <li key={item.id}>
                <button
                  onClick={() => onSectionChange(item.id)}
                  className={cn(
                    "w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200",
                    isActive
                      ? "bg-primary/10 text-secondary glow-primary"
                      : "text-muted-foreground hover:text-foreground hover:bg-secondary"
                  )}
                >
                  <Icon className={cn("w-5 h-5", isActive && "text-primary")} />
                  {item.label}
                </button>
              </li>
            );
          })}
        </ul>
      </nav>
    </aside>
  );
}
