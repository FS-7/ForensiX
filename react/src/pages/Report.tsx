import { useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { DeviceOverview } from "@/components/sections/DeviceOverview";
import { CallLogs } from "@/components/sections/CallLogs";
import { Messages } from "@/components/sections/Messages";
import { Contacts } from "@/components/sections/Contacts";
import { Files } from "@/components/sections/Files";
import { Photos } from "@/components/sections/Photos";
import { Navigation } from "@/components/Navigation";

type Section = 'overview' | 'calls' | 'messages' | 'contacts' | 'files' | 'photos';

const Report = () => {
  const [activeSection, setActiveSection] = useState<Section>('overview');

  const renderSection = () => {
    switch (activeSection) {
      case 'overview':
        return <DeviceOverview />;
      case 'calls':
        return <CallLogs />;
      case 'messages':
        return <Messages />;
      case 'contacts':
        return <Contacts />;
      case 'files':
        return <Files />;
      case 'photos':
        return <Photos />;
      default:
        return <DeviceOverview />;
    }
  };

  return (
    <div className="min-h-screen bg-background h-full">
      <Navigation />
      <div className="flex flex-row justify-center h-full">
        <Sidebar activeSection={activeSection} onSectionChange={setActiveSection} />
        <main className="p-8">
          <div className="max-w-6xl">
            {renderSection()}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Report;
