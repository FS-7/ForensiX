import { useEffect, useState } from "react";
import { Sidebar } from "@/components/Sidebar";
import { DeviceOverview } from "@/components/sections/DeviceOverview";
import { CallLogs } from "@/components/sections/CallLogs";
import { Messages } from "@/components/sections/Messages";
import { Contacts } from "@/components/sections/Contacts";
import { Files } from "@/components/sections/Files";
import { Photos } from "@/components/sections/Photos";
import { Navigation } from "@/components/Navigation";
import { useParams } from "react-router-dom";
import NotFound from "./NotFound";

type Section = 'overview' | 'calls' | 'messages' | 'contacts' | 'files' | 'photos';
const BACKEND = "http://localhost:5000"
const Report = () => {
  const [report, setReport] = useState([]);

  const { id } = useParams();


  useEffect(() => {
    fetch(BACKEND + '/internal/report/' + id,

    )
      .then(
        (res) => {
          if (res.status == 200)
            res.json().then((x) => { setReport(x) })
        }
      )
      .catch(
        (res) => {
          console.log(res)
        }
      )
  }, [])

  console.log(report)

  const [activeSection, setActiveSection] = useState<Section>('overview');

  const renderSection = () => {
    switch (activeSection) {
      case 'overview':
        return <DeviceOverview report={report} />;
      case 'calls':
        return <CallLogs report={report} />;
      case 'messages':
        return <Messages report={report} />;
      case 'contacts':
        return <Contacts report={report} />;
      case 'files':
        return <Files report={report} />;
      case 'photos':
        return <Photos report={report} />;
      default:
        return <DeviceOverview report={report} />;
    }
  };

  if (report.length < 1)
    return (
      <NotFound />
    )
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
