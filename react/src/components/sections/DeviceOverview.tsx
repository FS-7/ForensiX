import { deviceMetadata } from "@/data/mockData";
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

export function DeviceOverview({report}) {
  const storagePercent = (deviceMetadata.storage.used / deviceMetadata.storage.total) * 100;
  const ramPercent = (deviceMetadata.ram.used / deviceMetadata.ram.total) * 100;
  
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-2">Device Overview</h2>
        <p className="text-muted-foreground">Comprehensive information about your device</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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
        <StatCard 
          label="Battery Level" 
          value={`${deviceMetadata.battery}%`}
          subValue={deviceMetadata.battery > 50 ? "Good condition" : "Consider charging"}
          icon={Battery}
          variant={deviceMetadata.battery > 50 ? "success" : "warning"}
        />
        <StatCard 
          label="Last Sync" 
          value={formatDate(deviceMetadata.lastSync)}
          icon={Clock}
        />
      </div>

      {/* Storage & RAM */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

        <div className="card-gradient rounded-lg border border-border p-6 animate-fade-in">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg bg-accent/10 flex items-center justify-center">
              <Cpu className="w-5 h-5 text-accent" />
            </div>
            <div>
              <h3 className="font-semibold text-foreground">RAM</h3>
              <p className="text-sm text-muted-foreground">Memory usage</p>
            </div>
          </div>
          <Progress value={ramPercent} className="h-3 mb-3" />
          <div className="flex justify-between text-sm">
            <span className="text-muted-foreground">
              {deviceMetadata.ram.used} GB used
            </span>
            <span className="font-mono text-foreground">
              {deviceMetadata.ram.total} GB total
            </span>
          </div>
        </div>
      </div>

      {/* Technical Details */}
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
