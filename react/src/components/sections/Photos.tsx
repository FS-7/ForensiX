import { useState, useMemo } from "react";
import { photos, faceGroups } from "@/data/mockData";
import { FilterBar } from "@/components/FilterBar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Users, Calendar, MapPin } from "lucide-react";
import { format, parseISO } from "date-fns";

export function Photos() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedFace, setSelectedFace] = useState<string>("all");

  const filteredPhotos = useMemo(() => {
    return photos.filter((photo) => {
      const matchesSearch = photo.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        photo.location?.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesFace = selectedFace === "all" || photo.faces.includes(selectedFace);
      return matchesSearch && matchesFace;
    });
  }, [searchTerm, selectedFace]);

  // Group photos by date
  const photosByDate = useMemo(() => {
    const groups: Record<string, typeof photos> = {};
    filteredPhotos.forEach((photo) => {
      const date = format(parseISO(photo.dateTaken), "yyyy-MM-dd");
      if (!groups[date]) groups[date] = [];
      groups[date].push(photo);
    });
    return Object.entries(groups)
      .sort(([a], [b]) => b.localeCompare(a))
      .map(([date, photos]) => ({ date, photos }));
  }, [filteredPhotos]);

  // Group photos by face
  const photosByFace = useMemo(() => {
    return faceGroups.map((face) => ({
      ...face,
      photos: filteredPhotos.filter((photo) => photo.faces.includes(face.id)),
    })).filter(group => group.photos.length > 0);
  }, [filteredPhotos]);

  const getFaceName = (faceId: string) => {
    return faceGroups.find((f) => f.id === faceId)?.name || "Unknown";
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h2 className="text-2xl font-semibold text-foreground">Photos</h2>
        <p className="text-muted-foreground mt-1">Browse photos grouped by faces and dates</p>
      </div>

      <FilterBar
        searchValue={searchTerm}
        searchPlaceholder="Search photos..."
        onSearchChange={setSearchTerm}
        filters={[
          {
            id: "person",
            label: "Person",
            value: selectedFace,
            options: [
              { value: "all", label: "All People" },
              ...faceGroups.map((face) => ({ value: face.id, label: face.name })),
            ],
            onChange: setSelectedFace,
          },
        ]}
      />

      <Tabs defaultValue="faces" className="w-full">
        <TabsList className="mb-6">
          <TabsTrigger value="faces" className="gap-2">
            <Users className="w-4 h-4" />
            By Person
          </TabsTrigger>
          <TabsTrigger value="dates" className="gap-2">
            <Calendar className="w-4 h-4" />
            By Date
          </TabsTrigger>
        </TabsList>

        <TabsContent value="faces" className="space-y-6">
          {photosByFace.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                No photos found matching your filters.
              </CardContent>
            </Card>
          ) : (
            photosByFace.map((group) => (
              <Card key={group.id}>
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-3 text-lg">
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                      <Users className="w-5 h-5 text-primary" />
                    </div>
                    {group.name}
                    <Badge variant="secondary" className="ml-auto">
                      {group.photos.length} photos
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                    {group.photos.map((photo) => (
                      <div
                        key={photo.id}
                        className="group relative aspect-square rounded-lg overflow-hidden bg-secondary cursor-pointer"
                      >
                        <img
                          src={photo.url}
                          alt={photo.name}
                          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                          <div className="absolute bottom-2 left-2 right-2">
                            <p className="text-xs font-medium text-foreground truncate">{photo.name}</p>
                            {photo.location && (
                              <p className="text-xs text-muted-foreground flex items-center gap-1 mt-0.5">
                                <MapPin className="w-3 h-3" />
                                {photo.location}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </TabsContent>

        <TabsContent value="dates" className="space-y-6">
          {photosByDate.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                No photos found matching your filters.
              </CardContent>
            </Card>
          ) : (
            photosByDate.map((group) => (
              <Card key={group.date}>
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-3 text-lg">
                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                      <Calendar className="w-5 h-5 text-primary" />
                    </div>
                    {format(parseISO(group.date), "EEEE, MMMM d, yyyy")}
                    <Badge variant="secondary" className="ml-auto">
                      {group.photos.length} photos
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
                    {group.photos.map((photo) => (
                      <div
                        key={photo.id}
                        className="group relative aspect-square rounded-lg overflow-hidden bg-secondary cursor-pointer"
                      >
                        <img
                          src={photo.url}
                          alt={photo.name}
                          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                          <div className="absolute bottom-2 left-2 right-2">
                            <p className="text-xs font-medium text-foreground truncate">{photo.name}</p>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {photo.faces.slice(0, 2).map((faceId) => (
                                <Badge key={faceId} variant="outline" className="text-[10px] px-1.5 py-0">
                                  {getFaceName(faceId)}
                                </Badge>
                              ))}
                              {photo.faces.length > 2 && (
                                <Badge variant="outline" className="text-[10px] px-1.5 py-0">
                                  +{photo.faces.length - 2}
                                </Badge>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
