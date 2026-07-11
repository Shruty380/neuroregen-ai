export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 bg-gray-950/90 backdrop-blur-sm border-b border-gray-800">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center text-black font-bold text-sm">NR</div>
          <span className="font-bold text-white text-lg">NeuroRegen AI</span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm text-gray-400">
          <a href="#diseases" className="hover:text-emerald-400 transition-colors">Diseases</a>
          <a href="#tools" className="hover:text-emerald-400 transition-colors">Tools</a>
          <a href="#roadmap" className="hover:text-emerald-400 transition-colors">Roadmap</a>
          <a href="https://github.com/Shruty380/neuroregen-ai" target="_blank" rel="noreferrer" className="bg-emerald-500 text-black px-4 py-2 rounded-lg font-medium hover:bg-emerald-400 transition-colors">GitHub</a>
        </div>
      </div>
    </nav>
  );
}