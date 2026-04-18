import { NavLink, useLocation } from "react-router-dom"
import {
  RepoIcon,
  WorkflowIcon,
  IssueOpenedIcon,
  GearIcon,
  PlugIcon,
} from "@primer/octicons-react"
import { GitBranch, Layers } from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
} from "@/components/ui/sidebar"
import { Badge } from "@/components/ui/badge"

const menuItems = [
  {
    title: "Connections",
    url: "/connections",
    icon: PlugIcon,
  },
  {
    title: "Repositories",
    url: "/repositories",
    icon: RepoIcon,
  },
  {
    title: "CI/CD",
    url: "/cicd",
    icon: GitBranch,
    badge: "3",
  },
  {
    title: "Workflows",
    url: "/workflows",
    icon: WorkflowIcon,
  },
  {
    title: "Tickets",
    url: "/tickets",
    icon: IssueOpenedIcon,
    badge: "5",
  },
]

export function AppSidebar() {
  const location = useLocation()

  return (
    <Sidebar>
      <SidebarHeader className="border-b px-4 py-3">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Layers className="h-4 w-4" />
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold">Multi Provider</span>
            <span className="text-xs text-muted-foreground">Repository Manager</span>
          </div>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menuItems.map((item) => {
                const isActive = location.pathname.startsWith(item.url)
                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      asChild
                      isActive={isActive}
                      tooltip={item.title}
                    >
                      <NavLink to={item.url}>
                        <item.icon size={16} />
                        <span>{item.title}</span>
                        {item.badge && (
                          <Badge
                            variant="secondary"
                            className="ml-auto h-5 min-w-5 justify-center rounded-full px-1 text-xs"
                          >
                            {item.badge}
                          </Badge>
                        )}
                      </NavLink>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                )
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="border-t">
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              isActive={location.pathname.startsWith("/settings")}
              tooltip="Settings"
            >
              <NavLink to="/settings">
                <GearIcon size={16} />
                <span>Settings</span>
              </NavLink>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  )
}
