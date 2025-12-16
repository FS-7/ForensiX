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

export interface CallLog {
  id: string;
  contactName: string;
  phoneNumber: string;
  type: 'incoming' | 'outgoing' | 'missed';
  duration: number;
  timestamp: string;
}

export interface TextMessage {
  id: string;
  contactName: string;
  phoneNumber: string;
  message: string;
  type: 'sent' | 'received';
  timestamp: string;
  read: boolean;
}

export interface Contact {
  id: string;
  name: string;
  phoneNumber: string;
  email: string;
  company: string;
  favorite: boolean;
  lastContacted: string;
}

export interface DeviceFile {
  id: string;
  name: string;
  type: 'image' | 'video' | 'audio' | 'document' | 'archive' | 'other';
  size: number;
  path: string;
  modified: string;
}

export interface Photo {
  id: string;
  name: string;
  url: string;
  dateTaken: string;
  faces: string[];
  location?: string;
}

export interface FaceGroup {
  id: string;
  name: string;
  photoCount: number;
}

export interface DateGroup {
  date: string;
  photos: Photo[];
}

export const deviceMetadata: DeviceMetadata = {
  model: "Galaxy S24 Ultra",
  manufacturer: "Samsung",
  os: "Android",
  osVersion: "14.0",
  serialNumber: "RF8N90X1ABC",
  imei: "353456789012345",
  storage: { used: 178.5, total: 256 },
  ram: { used: 6.2, total: 12 },
  battery: 78,
  lastSync: "2024-12-08T10:30:00Z",
  ipAddress: "192.168.1.105",
  macAddress: "A4:83:E7:2B:9F:01",
};

export const callLogs: CallLog[] = [
  { id: "1", contactName: "John Smith", phoneNumber: "+1 555-0101", type: "incoming", duration: 245, timestamp: "2024-12-08T09:30:00Z" },
  { id: "2", contactName: "Sarah Johnson", phoneNumber: "+1 555-0102", type: "outgoing", duration: 180, timestamp: "2024-12-08T08:15:00Z" },
  { id: "3", contactName: "Unknown", phoneNumber: "+1 555-0199", type: "missed", duration: 0, timestamp: "2024-12-07T22:45:00Z" },
  { id: "4", contactName: "Mom", phoneNumber: "+1 555-0103", type: "outgoing", duration: 720, timestamp: "2024-12-07T18:00:00Z" },
  { id: "5", contactName: "Tech Support", phoneNumber: "+1 800-555-0000", type: "incoming", duration: 1200, timestamp: "2024-12-07T14:30:00Z" },
  { id: "6", contactName: "Alex Chen", phoneNumber: "+1 555-0104", type: "missed", duration: 0, timestamp: "2024-12-06T11:20:00Z" },
  { id: "7", contactName: "Pizza Place", phoneNumber: "+1 555-7777", type: "outgoing", duration: 60, timestamp: "2024-12-06T19:00:00Z" },
  { id: "8", contactName: "Work - Manager", phoneNumber: "+1 555-0200", type: "incoming", duration: 540, timestamp: "2024-12-05T09:00:00Z" },
];

export const textMessages: TextMessage[] = [
  { id: "1", contactName: "John Smith", phoneNumber: "+1 555-0101", message: "Hey, are we still meeting for lunch tomorrow?", type: "received", timestamp: "2024-12-08T10:15:00Z", read: true },
  { id: "2", contactName: "John Smith", phoneNumber: "+1 555-0101", message: "Yes! Let's meet at noon at the usual place.", type: "sent", timestamp: "2024-12-08T10:18:00Z", read: true },
  { id: "3", contactName: "Sarah Johnson", phoneNumber: "+1 555-0102", message: "Thanks for the call earlier. I'll send you the documents.", type: "received", timestamp: "2024-12-08T08:45:00Z", read: true },
  { id: "4", contactName: "Mom", phoneNumber: "+1 555-0103", message: "Don't forget about dinner on Sunday! 🍝", type: "received", timestamp: "2024-12-07T20:00:00Z", read: false },
  { id: "5", contactName: "Alex Chen", phoneNumber: "+1 555-0104", message: "Check out this link - it's the project we discussed", type: "received", timestamp: "2024-12-07T15:30:00Z", read: true },
  { id: "6", contactName: "Work - Manager", phoneNumber: "+1 555-0200", message: "Report submitted. Let me know if you need changes.", type: "sent", timestamp: "2024-12-06T17:00:00Z", read: true },
  { id: "7", contactName: "Bank Alert", phoneNumber: "BANK", message: "Your payment of $150.00 was processed successfully.", type: "received", timestamp: "2024-12-06T10:00:00Z", read: true },
];

export const contacts: Contact[] = [
  { id: "1", name: "John Smith", phoneNumber: "+1 555-0101", email: "john.smith@email.com", company: "Tech Corp", favorite: true, lastContacted: "2024-12-08T10:18:00Z" },
  { id: "2", name: "Sarah Johnson", phoneNumber: "+1 555-0102", email: "sarah.j@email.com", company: "Design Studio", favorite: true, lastContacted: "2024-12-08T08:45:00Z" },
  { id: "3", name: "Mom", phoneNumber: "+1 555-0103", email: "mom@family.com", company: "", favorite: true, lastContacted: "2024-12-07T20:00:00Z" },
  { id: "4", name: "Alex Chen", phoneNumber: "+1 555-0104", email: "alex.chen@startup.io", company: "StartupIO", favorite: false, lastContacted: "2024-12-07T15:30:00Z" },
  { id: "5", name: "Work - Manager", phoneNumber: "+1 555-0200", email: "manager@work.com", company: "Current Job Inc", favorite: false, lastContacted: "2024-12-06T17:00:00Z" },
  { id: "6", name: "Pizza Place", phoneNumber: "+1 555-7777", email: "", company: "Best Pizza", favorite: false, lastContacted: "2024-12-06T19:00:00Z" },
  { id: "7", name: "Dr. Williams", phoneNumber: "+1 555-0300", email: "drwilliams@clinic.com", company: "City Clinic", favorite: false, lastContacted: "2024-11-20T11:00:00Z" },
  { id: "8", name: "Gym", phoneNumber: "+1 555-4444", email: "info@fitnesscenter.com", company: "Fitness Center", favorite: false, lastContacted: "2024-11-15T07:00:00Z" },
];

export const deviceFiles: DeviceFile[] = [
  { id: "1", name: "vacation_photo_001.jpg", type: "image", size: 4.2, path: "/DCIM/Camera", modified: "2024-12-05T14:30:00Z" },
  { id: "2", name: "vacation_photo_002.jpg", type: "image", size: 3.8, path: "/DCIM/Camera", modified: "2024-12-05T14:32:00Z" },
  { id: "3", name: "meeting_recording.mp4", type: "video", size: 156.7, path: "/Movies", modified: "2024-12-04T10:00:00Z" },
  { id: "4", name: "project_proposal.pdf", type: "document", size: 2.1, path: "/Documents", modified: "2024-12-03T16:45:00Z" },
  { id: "5", name: "budget_2024.xlsx", type: "document", size: 0.5, path: "/Documents/Work", modified: "2024-12-02T09:00:00Z" },
  { id: "6", name: "podcast_episode_42.mp3", type: "audio", size: 45.3, path: "/Music/Podcasts", modified: "2024-12-01T08:00:00Z" },
  { id: "7", name: "backup_nov_2024.zip", type: "archive", size: 890.2, path: "/Backups", modified: "2024-11-30T23:00:00Z" },
  { id: "8", name: "screenshot_2024.png", type: "image", size: 1.2, path: "/Pictures/Screenshots", modified: "2024-11-28T15:20:00Z" },
  { id: "9", name: "notes.txt", type: "document", size: 0.01, path: "/Documents", modified: "2024-11-25T12:00:00Z" },
  { id: "10", name: "app_installer.apk", type: "other", size: 78.5, path: "/Downloads", modified: "2024-11-20T10:00:00Z" },
];

export const faceGroups: FaceGroup[] = [
  { id: "face-1", name: "John Smith", photoCount: 24 },
  { id: "face-2", name: "Sarah Johnson", photoCount: 18 },
  { id: "face-3", name: "Mom", photoCount: 42 },
  { id: "face-4", name: "Alex Chen", photoCount: 12 },
  { id: "face-5", name: "Unknown Person 1", photoCount: 8 },
];

export const photos: Photo[] = [
  { id: "p1", name: "beach_sunset.jpg", url: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400", dateTaken: "2024-12-05T14:30:00Z", faces: ["face-1", "face-2"], location: "Miami Beach" },
  { id: "p2", name: "family_dinner.jpg", url: "https://images.unsplash.com/photo-1529543544277-750e1a0f8c98?w=400", dateTaken: "2024-12-05T19:00:00Z", faces: ["face-3", "face-1"], location: "Home" },
  { id: "p3", name: "office_meeting.jpg", url: "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=400", dateTaken: "2024-12-04T10:15:00Z", faces: ["face-4", "face-2"], location: "Office" },
  { id: "p4", name: "coffee_shop.jpg", url: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400", dateTaken: "2024-12-04T08:30:00Z", faces: ["face-1"], location: "Downtown Cafe" },
  { id: "p5", name: "park_walk.jpg", url: "https://images.unsplash.com/photo-1476231682828-37e571bc172f?w=400", dateTaken: "2024-12-03T16:00:00Z", faces: ["face-3"], location: "Central Park" },
  { id: "p6", name: "birthday_party.jpg", url: "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=400", dateTaken: "2024-12-03T20:00:00Z", faces: ["face-1", "face-2", "face-3", "face-4"], location: "Home" },
  { id: "p7", name: "gym_selfie.jpg", url: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400", dateTaken: "2024-12-02T07:00:00Z", faces: ["face-1"], location: "Fitness Center" },
  { id: "p8", name: "sunset_drive.jpg", url: "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=400", dateTaken: "2024-12-02T18:30:00Z", faces: ["face-2"], location: "Highway 1" },
  { id: "p9", name: "lunch_date.jpg", url: "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400", dateTaken: "2024-12-01T12:30:00Z", faces: ["face-1", "face-4"], location: "Italian Restaurant" },
  { id: "p10", name: "night_city.jpg", url: "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=400", dateTaken: "2024-12-01T21:00:00Z", faces: ["face-5"], location: "Downtown" },
  { id: "p11", name: "morning_coffee.jpg", url: "https://images.unsplash.com/photo-1442512595331-e89e73853f31?w=400", dateTaken: "2024-11-30T08:00:00Z", faces: ["face-3"], location: "Home" },
  { id: "p12", name: "hiking_trail.jpg", url: "https://images.unsplash.com/photo-1551632811-561732d1e306?w=400", dateTaken: "2024-11-30T11:00:00Z", faces: ["face-1", "face-2", "face-4"], location: "Mountain Trail" },
];
