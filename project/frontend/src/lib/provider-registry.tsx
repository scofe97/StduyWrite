import { MarkGithubIcon } from "@primer/octicons-react"
import type { ProviderMeta, AuthType } from "@/types/provider"

interface IconProps {
  size?: number
  className?: string
}

// GitLab icon (inline SVG component)
function GitLabIcon({ size = 16, className }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      className={className}
    >
      <path d="M22.65 14.39L12 22.13 1.35 14.39a.84.84 0 01-.3-.94l1.22-3.78 2.44-7.51A.42.42 0 014.82 2a.43.43 0 01.58 0 .42.42 0 01.11.18l2.44 7.49h8.1l2.44-7.51A.42.42 0 0118.6 2a.43.43 0 01.58 0 .42.42 0 01.11.18l2.44 7.51L23 13.45a.84.84 0 01-.35.94z" />
    </svg>
  )
}

// Bitbucket icon (inline SVG component)
function BitbucketIcon({ size = 16, className }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      className={className}
    >
      <path d="M.778 1.211a.768.768 0 00-.768.892l3.263 19.81c.084.5.515.868 1.022.873H19.95a.772.772 0 00.77-.646l3.27-20.03a.768.768 0 00-.768-.891zM14.52 15.53H9.522L8.17 8.466h7.561z" />
    </svg>
  )
}

// GitHub wrapper to match our icon interface
function GitHubIcon({ size = 16, className }: IconProps) {
  return <MarkGithubIcon size={size} className={className} />
}

export interface ProviderRegistryEntry extends ProviderMeta {
  icon: React.ComponentType<IconProps>
}

export const PROVIDER_REGISTRY: Record<string, ProviderRegistryEntry> = {
  github: {
    type: "github",
    label: "GitHub",
    color: "#24292f",
    defaultBaseUrl: "https://api.github.com",
    supportedAuthTypes: ["token", "oauth", "app"] as AuthType[],
    icon: GitHubIcon,
  },
  gitlab: {
    type: "gitlab",
    label: "GitLab",
    color: "#FC6D26",
    defaultBaseUrl: "https://gitlab.com/api/v4",
    supportedAuthTypes: ["token", "oauth"] as AuthType[],
    icon: GitLabIcon,
  },
  bitbucket: {
    type: "bitbucket",
    label: "Bitbucket",
    color: "#0052CC",
    defaultBaseUrl: "https://api.bitbucket.org/2.0",
    supportedAuthTypes: ["token", "oauth", "app"] as AuthType[],
    icon: BitbucketIcon,
  },
}

export function getProviderMeta(type: string): ProviderRegistryEntry | undefined {
  return PROVIDER_REGISTRY[type]
}

export function getProviderIcon(type: string): React.ComponentType<IconProps> {
  return PROVIDER_REGISTRY[type]?.icon ?? GitHubIcon
}

export function getProviderLabel(type: string): string {
  return PROVIDER_REGISTRY[type]?.label ?? type
}

export function getProviderColor(type: string): string {
  return PROVIDER_REGISTRY[type]?.color ?? "#6b7280"
}

export function getAllProviders(): ProviderRegistryEntry[] {
  return Object.values(PROVIDER_REGISTRY)
}
