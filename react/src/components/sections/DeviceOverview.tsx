import { StatCard } from "@/components/StatCard";
import {
  Smartphone,
  HardDrive,
  Cpu,
  Battery,
  Wifi,
  Clock,
  Hash,
  Server
} from "lucide-react";
import { Progress } from "@/components/ui/progress";

export interface DeviceMetadata {
  model: string;
  manufacturer: string;
  os: string;
  osVersion: string;
  serialNumber: string;
  imei: string;
  storage: { used: number; total: number };
  ram: { used: number; total: number };
  battery: number;
  lastSync: string;
  ipAddress: string;
  macAddress: string;
}

const deviceMetadata: DeviceMetadata = {
  model: "Samsung S25",
  manufacturer: "Samsung",
  os: "Android",
  osVersion: "14",
  serialNumber: "FSDJKHKSDJUHV2165",
  imei: "5652121654654",
  battery: 100,
  lastSync: "18 Jan 2026",
  ipAddress: "192.168.1.1",
  macAddress: "2A:5C:44:4D",
  ram: {
    used: 100,
    total: 100,
  },

  storage: {
    used: 50,
    total: 100,
  },
}

export function DeviceOverview({ report }) {
  const storagePercent = (deviceMetadata.storage.used / deviceMetadata.storage.total) * 100;
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Device Overview</h2>
        <p className="text-muted-foreground">Comprehensive information about your device</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <StatCard
          label="Device Model"
          value={deviceMetadata.model}
          subValue={deviceMetadata.manufacturer}
          icon={Smartphone}
          variant="primary"
        />
        <StatCard
          label="Operating System"
          value={deviceMetadata.os}
          subValue={`Version ${deviceMetadata.osVersion}`}
          icon={Server}
        />
        <div className="card-gradient rounded-lg border border-border p-6 animate-fade-in">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <HardDrive className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h3 className="font-semibold text-foreground">Storage</h3>
              <p className="text-sm text-muted-foreground">Internal storage usage</p>
            </div>
          </div>
          <Progress value={storagePercent} className="h-3 mb-3" />
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">
              {deviceMetadata.storage.used} GB used
            </span>
            <span className="font-mono text-foreground">
              {deviceMetadata.storage.total} GB total
            </span>
          </div>
        </div>
      </div>

      <div className="card-gradient rounded-lg border border-border p-6 animate-fade-in">
        <h3 className="font-semibold text-foreground mb-4">Technical Details</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            { icon: Hash, label: "Serial Number", value: deviceMetadata.serialNumber },
            { icon: Smartphone, label: "IMEI", value: deviceMetadata.imei },
            { icon: Wifi, label: "IP Address", value: deviceMetadata.ipAddress },
            { icon: Server, label: "MAC Address", value: deviceMetadata.macAddress },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-3 p-3 rounded-lg bg-secondary/50">
              <item.icon className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">{item.label}</p>
                <p className="font-mono text-sm text-foreground">{item.value}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
