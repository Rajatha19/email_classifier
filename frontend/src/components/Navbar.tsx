"use client";

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center items-center h-24">
          <div className="flex items-center">
            <img
              src="/logo-autou.webp"
              alt="AutoU"
              className="h-16 w-auto"
              onError={(e) => {
                const target = e.currentTarget as HTMLImageElement;
                target.onerror = null;
                target.src = "/logo-autou.webp";
              }}
            />
            <span className="text-4xl font-bold hidden ml-2">
              <span className="text-orange-500">Auto</span>
              <span className="text-orange-400">U</span>
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
}
