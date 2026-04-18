import { useSearchParams } from "react-router-dom"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { GeneralSettings } from "@/features/settings/components/GeneralSettings"
import { ProvidersSettings } from "@/features/settings/components/ProvidersSettings"

export function SettingsPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const tab = searchParams.get("tab") || "general"

  const handleTabChange = (value: string) => {
    setSearchParams({ tab: value })
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Settings</h1>
        <p className="text-muted-foreground">
          Manage your application settings and provider connections.
        </p>
      </div>

      <Tabs value={tab} onValueChange={handleTabChange}>
        <TabsList>
          <TabsTrigger value="general">General</TabsTrigger>
          <TabsTrigger value="providers">Providers</TabsTrigger>
        </TabsList>
        <TabsContent value="general" className="mt-6">
          <GeneralSettings />
        </TabsContent>
        <TabsContent value="providers" className="mt-6">
          <ProvidersSettings />
        </TabsContent>
      </Tabs>
    </div>
  )
}
