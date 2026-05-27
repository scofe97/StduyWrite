import { ReactNode } from 'react';
import {
  Workflow,
  Image,
  Video,
  Layout as LayoutIcon,
  Layers,
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
  activeMenu?: 'workflow' | 'image' | 'video' | 'template' | 'batch';
}

export default function Layout({ children, activeMenu = 'workflow' }: LayoutProps) {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* 상단 네비게이션 - 항상 표시 */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-gray-800 bg-gray-900/95 backdrop-blur-sm">
        <div className="max-w-full mx-auto px-4">
          <div className="flex items-center justify-between h-14">
            {/* 로고 및 메뉴 */}
            <div className="flex items-center gap-8">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                  <Workflow className="w-5 h-5 text-white" />
                </div>
                <span className="text-lg font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  IRIS
                </span>
              </div>

              <div className="flex items-center gap-1">
                <NavItem
                  icon={<Workflow className="w-4 h-4" />}
                  label="워크플로우"
                  active={activeMenu === 'workflow'}
                />
                <NavItem
                  icon={<Image className="w-4 h-4" />}
                  label="이미지"
                  active={activeMenu === 'image'}
                />
                <NavItem
                  icon={<Video className="w-4 h-4" />}
                  label="비디오"
                  active={activeMenu === 'video'}
                />
                <NavItem
                  icon={<LayoutIcon className="w-4 h-4" />}
                  label="템플릿"
                  active={activeMenu === 'template'}
                />
                <NavItem
                  icon={<Layers className="w-4 h-4" />}
                  label="일괄 작업"
                  active={activeMenu === 'batch'}
                />
              </div>
            </div>

            {/* 우측 영역 */}
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-red-500 cursor-pointer hover:ring-2 hover:ring-purple-500 transition-all" />
            </div>
          </div>
        </div>
      </nav>

      {/* 메인 콘텐츠 (네비게이션 높이만큼 패딩) */}
      <main className="pt-14">{children}</main>
    </div>
  );
}

// 네비게이션 아이템 컴포넌트
function NavItem({ icon, label, active }: { icon: ReactNode; label: string; active?: boolean }) {
  return (
    <button
      className={`flex items-center gap-2 px-3 py-2 text-sm rounded-lg transition-colors ${
        active ? 'bg-gray-800 text-white' : 'text-gray-400 hover:text-white hover:bg-gray-800/50'
      }`}
    >
      {icon}
      <span>{label}</span>
    </button>
  );
}

